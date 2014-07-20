
import glob, logging
from slugify import slugify

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

        if key(file):
            parser(key(file))(d, data)

    parse_files(path,
                ["physical and chemical properties", "SSS", "SSS"],
                step)

def key(file):
    candidate = [k for k in ["appearance", "melting point", "boiling point", "density",
                             "particle size", "vapour pressure", "partition coefficient",
                             "water solubility", "surface tension", "flash point",
                             "auto flammability", "flammability", "explosiveness",
                             "oxidising properties", "stability in organic solvents",
                             "dissociation constant", "viscosity"]
                 if "__%s" % slugify(k) in file]

    return candidate[0] if candidate else None

def parser(key):
    return {
        "appearance": lambda d, data: None,
        "melting point": lambda d, data: None,
        "boiling point": lambda d, data: None,
        "density": lambda d, data: None,
        "particle size": lambda d, data: None,
        "vapour pressure": lambda d, data: None,
        "partition coefficient": lambda d, data: None,
        "water solubility": lambda d, data: None,
        "surface tension": lambda d, data: None,
        "flash point": lambda d, data: None,
        "auto flammability": lambda d, data: None,
        "flammability": lambda d, data: None,
        "explosiveness": lambda d, data: None,
        "oxidising properties": lambda d, data: None,
        "stability in organic solvents": lambda d, data: None,
        "dissociation constant": lambda d, data: None,
        "viscosity": lambda d, data: None
    }[key]
