from typing import Tuple
from bs4 import BeautifulSoup
from rdkit import Chem
import asyncio

async def navigate_swissadme_site(page, drug_name, canonical_smile, logger):
    logger.write_log("Navigating swissadme site...")
    
    swissadme_url = 'http://www.swissadme.ch/index.php'
    await page.goto(swissadme_url)

    sadme_js_code = f"""
            smilesTextArea = document.getElementById("smiles");
            smilesTextArea.textContent = "{canonical_smile}"
        """
    await page.evaluate(sadme_js_code)

    await page.click("#smiles")
    await page.keyboard.press('ArrowLeft')
    await page.click("#submitButton")
    await asyncio.sleep(10)

    await page.screenshot({'path': 'screen.png', 'fullPage': True})
    swissadme_content = await page.content()
    swissadme_result = scrape_swissadme(swissadme_content, drug_name, canonical_smile)
    
    logger.write_log("Scrapped swissadme site...")

    return swissadme_result

def scrape_swissadme(content, drug_name, smiles) -> Tuple:
    soup = BeautifulSoup(content, "html.parser")

    left_table = soup.select_one("#sib_body > div:nth-child(33) > div:nth-child(3) > div:nth-child(5) > table:nth-child(4) > tbody")
    right_table = soup.select_one("#sib_body > div:nth-child(33) > div:nth-child(3) > div:nth-child(6) > table > tbody")

    left_table_rows = left_table.find_all("tr")
    right_table_rows = right_table.find_all("tr")
    left_table_len = len(left_table_rows)
    right_table_len = len(right_table_rows)

    molecular_weight = left_table_rows[2].find_all("td")[1].text
    mlogp = left_table_rows[left_table_len-3].find_all("td")[1].text
    h_donor = left_table_rows[8].find_all("td")[1].text
    h_acceptor = left_table_rows[7].find_all("td")[1].text
    
    molar_refractivity = left_table_rows[9].find_all("td")[1].text
    total_atoms = left_table_rows[3].find_all("td")[1].text
    ghose_violation = 0 if  "Yes" in right_table_rows[right_table_len-11].find_all("td")[1].text else 1

    rotatable_bond = left_table_rows[6].find_all("td")[1].text
    tpsa = left_table_rows[10].find_all("td")[1].text

    rotatable_bond = left_table_rows[6].find_all("td")[1].text

    # violations
    lipinski_violation = 0 if "Yes" in right_table_rows[right_table_len-12].find_all("td")[1].text else 1
    veber_violation = 0 if  "Yes" in right_table_rows[right_table_len-10].find_all("td")[1].text else 1
    egan_violation = 0 if "Yes" in right_table_rows[right_table_len-9].find_all("td")[1].text else 1
    muegge_violation = 0 if "Yes" in right_table_rows[right_table_len-8].find_all("td")[1].text else 1

    # moles details
    mol = Chem.MolFromSmiles(smiles)
    ring_count = mol.GetRingInfo().NumRings()
    carbon_count = sum(1 for atom in list(mol.GetAtoms()) if atom.GetAtomicNum() == 6)
    heteroatom_count = sum(1 for atom in list(mol.GetAtoms()) 
                        if atom.GetAtomicNum() != 6 and atom.GetAtomicNum() != 1)

    lipinski_cols = (molecular_weight, mlogp, h_donor, h_acceptor, lipinski_violation)
    ghose_cols = (molecular_weight, mlogp, molar_refractivity, total_atoms, ghose_violation)
    veber_col = (rotatable_bond, tpsa, veber_violation)
    egan_col = (mlogp, tpsa, egan_violation)
    muegge_col = (molecular_weight, tpsa, ring_count, carbon_count, heteroatom_count, rotatable_bond, h_acceptor, h_donor, muegge_violation)

    total_row = (drug_name,) + lipinski_cols + ghose_cols + veber_col + egan_col + muegge_col

    return total_row