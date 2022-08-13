import asyncio
from pyppeteer import launch
import requests
from swissadme import navigate_swissadme_site
from pkcsm import navigate_pkcsm_site
from csv_io import write_rows_to_csv, write_swissadme_headers, write_pkcsm_headers
import os

async def main():
    drug_file_path = input("Enter path of Drug names = ")
    current_dir = os.getcwd()
    if drug_file_path[0] is ".":
        drug_file_path = current_dir + drug_file_path
        print(drug_file_path)
    swissadme_details = []
    pkcsm_details = []

    file = open(drug_file_path)
    file_content = file.readlines()
    drug_names = []
    for line in file_content:
        drug_names.append(line.rstrip())

    for drug_name in drug_names:
        drug_details = await get_drug_details(drug_name)
        swissadme_details.append(drug_details.get("swissadme_result"))
        pkcsm_details.append(drug_details.get("pkcsm_result"))

    #csv headers
    write_swissadme_headers("swissadme.csv")
    write_pkcsm_headers("pkcsm.csv")

    #write details to csv 
    write_rows_to_csv("swissadme.csv", swissadme_details)
    write_rows_to_csv("pkcsm.csv", pkcsm_details)
    
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




    
