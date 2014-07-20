
import csv
from pony.orm import *

from db import *

def fix_id(row):
    diss = row[-2]
    ec = row[0]
    cas = row[1]

    substance = Substance.get(DOSSIER_ID=diss)
    if substance:
        substance.CAS = cas
        substance.EC = ec

@db_session
def fix_data():
    with open("disseminated_substances_en.csv", "rb") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            fix_id(row)

if __name__ == "__main__":
    fix_data()
