import asyncio
from pyppeteer import launch
import requests
from swissadme import navigate_swissadme_site
from pkcsm import navigate_pkcsm_site
from csv_io import write_rows_to_csv, write_swissadme_headers, write_pkcsm_headers, write_row_to_csv
import os

async def main():
    current_dir = os.getcwd()
    drug_file_path = os.path.join(current_dir, input("Enter path of Drug names = "))
    output_path = os.path.join(current_dir, "output")
    os.makedirs(output_path, exist_ok=True)
    swissadme_output_path = os.path.join(output_path, "swissadme.csv")
    pkcsm_output_path = os.path.join(output_path, "pkcsm.csv")

    swissadme_details = []
    pkcsm_details = []
    drug_names = []

    with(open(drug_file_path)) as file:
        file_content = file.readlines()
        for line in file_content:
            drug_names.append(line.rstrip())

    #csv headers
    write_swissadme_headers(swissadme_output_path)
    write_pkcsm_headers(pkcsm_output_path)

    # scrape details for each drug
    for drug_name in drug_names:
        drug_details = await get_drug_details(drug_name)
        swissadme_res = drug_details.get("swissadme_result")
        pkcsm_res = drug_details.get("pkcsm_result")
        
        # add to main list
        swissadme_details.append(swissadme_res)
        pkcsm_details.append(pkcsm_res)

        # write to csv
        write_row_to_csv(swissadme_output_path, swissadme_res)
        write_row_to_csv(pkcsm_output_path, pkcsm_res)
        
    
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




    
