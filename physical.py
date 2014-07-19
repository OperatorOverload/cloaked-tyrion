
import glob, logging

from helpers import *
from db import *


def parse(substance, path):
    def step(d, data, file):
        adm = save_data(data, ECHA_PHYSCHEM_ADM,
                        [("SUBST_ID", substance),
                         ("esr", get_esr(d))],
                        make_fields([("reliability", ".reliability:first"),
                                      ("glp", ".GLP_COMPLIANCE_STATEMENT"),
                                      ("org_solvents_stability", ".STABLE"),
                                      ("org_solvents_degrad",
                                       ".DEGRAD_PRODUCTS_INDICATOR")],
                                    ["method_type",
                                     "partcoeff_type",
                                     "testtype",
                                     "testmat_indicator",
                                     "interpretation_results",
                                     "dissociation_indicator",
                                     "distribution_type"]))
        adm = adm[0]

        save_guidelines(data, ECHA_PHYSCHEM_GUIDELINES,
                        ("PHYSCHEM_ID", adm))

        save_refs(data, ECHA_PHYSCHEM_REF,
                  ("PHYSCHEM_ID", adm))


    parse_files(path,
                ["physical and chemical properties", "SSS", "SSS"],
                step)
