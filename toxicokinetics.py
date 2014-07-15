
import glob, logging

from helpers import *
from db import *

def basic(substance, path):
    files = build_path(path,
                       ["toxicological information",
                        "toxicokinetics metabolism and distribution",
                        "basic toxicokinetics",
                        "SSS"])

    for file in glob.glob(files.replace("sss", "*")):
        d = open_file(file)
        data = d("#inner")

        kwargs = dict(
            subst_id = substance,
            esr = d("#page_header h2").text(),
            reliability = value_by_select(data, ".reliability"),
            type_invivo_invitro = value_by_select(data, ".TYPE_INVIVO_INVITRO"),
            study_objective = value_by_select(data, ".STUDY_OBJECTIVE"),
            glp = value_by_select(data, ".GLP_COMPLIANCE_STATEMENT"),
            testmat_indicator = value_by_select(data, ".TESTMAT_INDICATOR"))

        basic = find_or_create(ECHA_TOX_BTK_ADM, **fieldify(kwargs))

        logging.info("Guideline")

        save_data(data.find(".set.GUIDELINE"),
                  ECHA_TOX_BTK_GUIDELINES,
                  ("TOX_BTK_ID", basic),
                  [("guideline", ".GUIDELINE"),
                   ("qualifier", ".QUALIFIER")])

        logging.info("Reference")
        save_refs(data,
                  ECHA_TOX_BTK_REF,
                  ("TOX_BTK_ID", basic))

        logging.info("Data")
        save_data(data,
                  ECHA_TOX_BTK_DATA,
                  ("TOX_BTK_ID", basic),
                  [("organism", ".ORGANISM"),
                   ("sex", ".SEX"),
                   ("route", ".ROUTE"),
                   ("vehicle_tox", ".VEHICLE_TOX"),
                   ("exp_period", ".EXP_PERIOD"),
                   ("doses_concentrations", ".DOSES_CONCENTRATIONS"),
                   ("metabolites", ".METABOLITES"),
                   ("interpret_rs_submitter", ".INTERPRET_RS_SUBMITTER")])
