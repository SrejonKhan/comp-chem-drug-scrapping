import csv

def write_to_csv(filename,row):
    with open(filename, 'a') as file: 
        writer = csv.writer(file)
        writer.writerow(row)

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
    
    write_to_csv(filename, swissadme_header_row)
    write_to_csv(filename, swissadme_sub_header_row)

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

    write_to_csv(filename, pkcsm_header_row)
    write_to_csv(filename, pkcsm_sub_header_row)

