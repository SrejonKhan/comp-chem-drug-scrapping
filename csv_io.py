import csv

def write_rows_to_csv(filename,rows):
    with open(filename, 'a') as file: 
        writer = csv.writer(file)
        writer.writerows(rows)

def write_swissadme_headers(filename):
    swissadme_header_row = ["Name of drugs", "Lipsinki (04)", "Violation", "Ghose (04)", "Violation", 
        "Veber (02)", "Violation", "Egan", "Violation", "Muegge", "Violation"]
    swissadme_sub_header_row = ["", 
        # Lipinski
        "Molecular Weight", "MLOGP", "No of H Donor", "No of H acceptor", "", 
        # Ghose
        "Molecular Weight", "MLOGP", "Molar Refractivity", "Total Atoms", "", 
        # Veber
        "Rotatable Bond", "TPSA", "", 
        # Egan
        "MLOGP", "TPSA", "", 
        # Muegge
        "Molecular Weight", "TPSA", "Num. of RINGS", "Num. of CARBON", "Num. HETEROATOM", 
        "Num. Rotatable bonds", "H-bond acceptors", "H-bond donors"]
    
    headers = []
    headers.append(swissadme_header_row)
    headers.append(swissadme_sub_header_row)
    write_rows_to_csv(filename, headers)

def write_pkcsm_headers(filename):
    pkcsm_header_row = ["Name of drug", "Absorption", "Distribution", "Metabolism", "Excretion", "Toxicity"]
    pkcsm_sub_header_row = ["",
        # Absorption
        "Water Solubility", "Intestinal absorption (human)",
        # Distribution
        "BBB Permeability", "CNS Permeability", 
        # Metabolism
        "CYP3A4 substrate", "CYP3A4 inhibitor", 
        # Excretion
        "Total Clearance", "Renal OCT2 substrate", 
        # Toxicity
        "Max. Tolerated dose (human)", "Oral Rat Acute Toxicity (LD50)"]

    headers = []
    headers.append(pkcsm_header_row)
    headers.append(pkcsm_sub_header_row)
    write_rows_to_csv(filename,headers)

