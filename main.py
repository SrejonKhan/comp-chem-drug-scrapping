import asyncio
import traceback
from pyppeteer import launch
import requests
from scrapper.swissadme import navigate_swissadme_site
from scrapper.pkcsm import navigate_pkcsm_site
from file_io.csv_io import write_swissadme_headers, write_pkcsm_headers, write_row_to_csv
from file_io.log import Logger
import os

async def main():
    for folder, subfolders, files in os.walk('output/'):
        for file in files:
            if file.endswith('.csv'):
                path = os.path.join(folder, file)
                print('Deleted:', path)
                os.remove(path)
            if file.endswith('.txt'):
                path = os.path.join(folder, file)
                print('Deleted:', path)
                os.remove(path)

    current_dir = os.getcwd()
    drug_file_path = os.path.join(current_dir, input("Enter path of Drug names = "))
    output_path = os.path.join(current_dir, "output")
    os.makedirs(output_path, exist_ok=True)
    swissadme_output_path = os.path.join(output_path, "swissadme.csv")
    pkcsm_output_path = os.path.join(output_path, "pkcsm.csv")
    log_output_path = os.path.join(output_path, "log.txt")
    
    logger = Logger(log_output_path)

    swissadme_details = []
    pkcsm_details = []
    drug_names = []

    # read all drug names
    with(open(drug_file_path)) as file:
        file_content = file.readlines()
        for line in file_content:
            drug_names.append(line.rstrip())

    #csv headers
    write_swissadme_headers(swissadme_output_path)
    write_pkcsm_headers(pkcsm_output_path)

    # scrape details for each drug
    for drug_name in drug_names:
        try:
            logger.write_log(f"----Collecting details of {drug_name}----")
            drug_details = await scrape_drug_details(drug_name, logger)

            # Wrong Canonical Smiles
            if drug_details == None: 
                continue

            swissadme_res = drug_details.get("swissadme_result")
            pkcsm_res = drug_details.get("pkcsm_result")
            
            # add to main list
            swissadme_details.append(swissadme_res)
            pkcsm_details.append(pkcsm_res)

            # write to csv
            write_row_to_csv(swissadme_output_path, swissadme_res)
            write_row_to_csv(pkcsm_output_path, pkcsm_res)
            
            logger.write_log("Details has writted to csv. Proceeding to next if there is... \n")

        except Exception as e:
            logger.write_log(f"Something wrong happened when collecting details of {drug_name}.")
            traceback_str = ''.join(traceback.format_tb(e.__traceback__))
            logger.write_log(f"Traceback - ")
            logger.write_log(traceback_str)
            logger.write_log("Proceeding to next if there is...")
            
        
async def scrape_drug_details(drug_name, logger):
    browser = await launch() 
    page = await browser.newPage()

    canonical_smile_response = requests.get(f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{drug_name}" +
        "/property/CanonicalSMILES/TXT")

    canonical_smile = canonical_smile_response.text

    if canonical_smile_response.status_code == 404:
        logger.write_log(f"Canonical smilesnot found for this drug. We are aborting it. \n")
        return None

    canonical_smile = canonical_smile.replace("\n","")
    logger.write_log(canonical_smile)

    if len(canonical_smile) >= 200:
        logger.write_log(f"Canonical smiles exceed 200 character. We are aborting it. \n")
        return None

    #------------SwissADME site------------#
    swissadme_result = await navigate_swissadme_site(page, drug_name, canonical_smile, logger) 
    
    #------------pkCSM site------------#
    pkcsm_result = await navigate_pkcsm_site(page, drug_name, canonical_smile, logger)

    results = {
        "swissadme_result": swissadme_result, 
        "pkcsm_result": pkcsm_result
        }

    logger.write_log("Successfully retrived swissadme result and pkcsm result.")

    await browser.close()
    return results

asyncio.get_event_loop().run_until_complete(main())




    
