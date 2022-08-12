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

# maskura
def write_pkcsm_headers():
    pass

