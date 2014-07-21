
import csv
from pony.orm import *

from db import *

def fix(row):
    diss = row[-2]
    ec = row[0]
    cas = row[1]

    substance = Substance.get(DOSSIER_ID=diss)
    if substance:
        substance.CAS = cas
        substance.EC = ec

        for adm in substance.PHYSCHEMS:
            for model in adm.SOLDEGRADS:
                model.NO = model.NO.replace("#", "")
            for model in adm.DISSCOS:
                model.NO = model.NO.replace("#", "")

@db_session
def fix_data():
    with open("disseminated_substances_en.csv", "rb") as csvfile:
        reader = csv.reader(csvfile)
        reader.next()

        for row in reader:
            fix(row)

if __name__ == "__main__":
    fix_data()
