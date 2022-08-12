import asyncio
from pyppeteer import launch
import requests
from swissadme import navigate_swissadme_site
from pkcsm import navigate_pkcsm_site
from csv_io import write_to_csv

async def main():
    drug_name = 'Anastrozole'    
    data = await get_drug_details(drug_name)
    print(data)

async def get_drug_details(drug_name):
    browser = await launch() 
    page = await browser.newPage()

    canonical_smile_response = requests.get(f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{drug_name}" +
        "/property/CanonicalSMILES/TXT")

    canonical_smile = canonical_smile_response.text
    canonical_smile = canonical_smile.replace("\n","")
    print(canonical_smile)

    #------------SwissADME site------------#
    swissadme_result = await navigate_swissadme_site(page, drug_name, canonical_smile) 
    
    #------------pkCSM site------------#
    pkcsm_result = await navigate_pkcsm_site(page, drug_name, canonical_smile)

    results = {
        "swissadme_result": swissadme_result, 
        "pkcsm_result": pkcsm_result
        }

    await browser.close()
    return results

asyncio.get_event_loop().run_until_complete(main())




    
