import csv

def write_to_csv(filename,row):
    with open(filename, 'a') as file: 
        writer = csv.writer(file)
        writer.writerow(row)

# rai 
def write_swissadme_headers():
    pass

# maskura
def write_pkcsm_headers():
    pass

