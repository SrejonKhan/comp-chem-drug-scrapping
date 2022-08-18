from typing import Tuple
from bs4 import BeautifulSoup
import asyncio
import pyppeteer

async def navigate_pkcsm_site(page, drug_name, canonical_smile, logger): 
    logger.write_log("Navigating pkcsm site...")

    pkcsm_url = 'https://biosig.lab.uq.edu.au/pkcsm/prediction'
    await page.goto(pkcsm_url, {"timeout": 100000, "waitUntil": "domcontentloaded"})

    pkcsm_js_code = f"""
        smile_input = document.querySelector(
            `body > div.container > div.row > div.span7.offset1 
            > form > div:nth-child(2) > div:nth-child(3) > div > input`
            );        
        smile_input.value = "{canonical_smile}"
    """
    await page.evaluate(pkcsm_js_code)

    navpromise = asyncio.ensure_future(page.waitForNavigation({"timeout": 60000, "waitUntil": "networkidle0"})) 

    await page.click("body > div.container > div.row > div.span7.offset1 >" + 
            "form > div:nth-child(5) > div > div > div > div:nth-child(2) > button")

    await navpromise

    logger.write_log("Waiting for pkcsm calculation...")
    pkcsm_result =  await wait_till_computation(page, drug_name)

    logger.write_log("Scrapped pkcsm site...")
    
    return pkcsm_result

async def wait_till_computation(page, drug_name) -> Tuple:
    content = await page.content()
    soup = BeautifulSoup(content, "html.parser")
    nextRequest = asyncio.ensure_future(page.waitForNavigation({"timeout": 6000, "waitUntil": "networkidle0"})) 
    
    is_all_loaded = True

    try:
        await nextRequest 
    except pyppeteer.errors.TimeoutError: # we will consider that all of our data is loaded
        pass

    data_table = soup.select_one("body > div.container > div.row.fluid > div.span8 > div.well > table > tbody")
    all_props = data_table.find_all("tr")

    # check if calculation is still running
    for prop in all_props:
        table_data = prop.find_all("td")
        if("Running" in table_data[2].text):
            is_all_loaded = False
    
    if not is_all_loaded: 
        result = await wait_till_computation(page, drug_name) 
        return result
    
    else: 
        return scrape_results(soup, drug_name)
    

def scrape_results(soup, drug_name) -> Tuple:
    data_table = soup.select_one("body > div.container > div.row.fluid > div.span8 > div.well > table > tbody")
    all_props = data_table.find_all("tr")

    water_solubility = all_props[0].find_all("td")[2].text.strip()
    intestinal_absorption = all_props[2].find_all("td")[2].text.strip()
    bbb_permeability = all_props[9].find_all("td")[2].text.strip()
    cns_permeability = all_props[10].find_all("td")[2].text.strip()
    cyp3a4_substrate = all_props[12].find_all("td")[2].text.strip()
    cyp3a4_inhibitor = all_props[17].find_all("td")[2].text.strip()
    total_clearance = all_props[18].find_all("td")[2].text.strip()
    renal_oct2_substrate = all_props[19].find_all("td")[2].text.strip()
    max_tolerated_dose = all_props[21].find_all("td")[2].text.strip()
    oral_rat_acute_toxicity = all_props[24].find_all("td")[2].text.strip()

    absorption_col = (water_solubility, intestinal_absorption)
    distribution_col = (bbb_permeability, cns_permeability)
    metabolism_col = (cyp3a4_substrate, cyp3a4_inhibitor)
    excretion_col = (total_clearance, renal_oct2_substrate)
    toxicity_col = (max_tolerated_dose, oral_rat_acute_toxicity)

    total_row = (drug_name,) + absorption_col + distribution_col + metabolism_col + excretion_col + toxicity_col

    return total_row
    