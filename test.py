
from db import *
import scrape_parser as sp
import toxicokinetics as tk

@db_session
def test_aqua_parse():
    substance = select(s for s in Substance
                       if s.DOSSIER_ID == "DISS-9daa7594-c409-0ed0-e044-00144f67d249").limit(1)[0]

    sp.toxicity("data/DISS-9daa7594-c409-0ed0-e044-00144f67d249/ecotoxicological-information__aquatic-toxicity__long-term-toxicity-to-aquatic-invertebrates__exp-ns-long-term-toxicity-to-aquatic-invertebrates-003.html",
                substance,
                "AQUATIC")

@db_session
def test_acute_data():
    substance = select(s for s in Substance
                       if s.DOSSIER_ID == "DISS-9daa7594-c409-0ed0-e044-00144f67d249").limit(1)[0]

    tk.acute(substance, "data/DISS-9daa7594-c409-0ed0-e044-00144f67d249")

@db_session
def test_dermal_data():
    substance = select(s for s in Substance
                       if s.DOSSIER_ID == "DISS-9daa7594-c409-0ed0-e044-00144f67d249").limit(1)[0]

    tk.dermal(substance, "data/DISS-9daa7594-c409-0ed0-e044-00144f67d249")

if __name__ == '__main__':
    #test_aqua_parse()
    #test_acute_data()
    test_dermal_data()
