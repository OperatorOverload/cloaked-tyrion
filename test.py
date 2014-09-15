
from db import *
import scrape_parser as sp

@db_session
def test_aqua_parse():
    substance = select(s for s in Substance
                       if s.DOSSIER_ID == "DISS-9daa7594-c409-0ed0-e044-00144f67d249").limit(1)[0]

    sp.toxicity("data/DISS-9daa7594-c409-0ed0-e044-00144f67d249/ecotoxicological-information__aquatic-toxicity__long-term-toxicity-to-aquatic-invertebrates__exp-ns-long-term-toxicity-to-aquatic-invertebrates-003.html",
                substance,
                "AQUATIC")


if __name__ == '__main__':
    test_aqua_parse()
