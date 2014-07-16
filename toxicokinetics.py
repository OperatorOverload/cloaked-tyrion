
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

def dermal(substance, path):
    files = build_path(path,
                       ["toxicological information",
                        "toxicokinetics metabolism and distribution",
                        "dermal absorption",
                        "SSS"])

    for file in glob.glob(files.replace("sss", "*")):
        d = open_file(file)
        data = d("#inner")

        logging.info("Esr, %s" % get_esr(d))
        adm = save_data(data, ECHA_TOX_DA_ADM,
                        [("SUBST_ID", substance),
                         ("esr", get_esr(d))],
                        [("reliability", ".reliability:first"),
                         ("type_invivo_invitro", ".TYPE_INVIVO_INVITRO"),
                         ("glp", ".GLP_COMPLIANCE_STATEMENT"),
                         ("testmat_indicator", ".TESTMAT_INDICATOR"),
                         ("organism", ".ORGANISM"),
                         ("sex", ".SEX"),
                         ("exp_period", ".EXP_PERIOD"),
                         ("vehicle_tox", ".VEHICLE_TOX"),
                         ("doses_concentrations", ".DOSES_CONCENTRATIONS"),
                         ("signs_symptoms_toxicity", ".SIGNS_SYMPTOMS_TOXICITY"),
                         ("dermal_irritation", ".DERMAL_IRRITATION")])
        adm = adm[0]

        logging.info("Guideline")
        save_data(data.find(".set.GUIDELINE"),
                  ECHA_TOX_DA_GUIDELINES,
                  ("TOX_DA_ID", adm),
                  [("guideline", ".GUIDELINE"),
                   ("qualifier", ".QUALIFIER")])

        logging.info("Refs")
        save_refs(data,
                  ECHA_TOX_DA_REF,
                  ("TOX_DA_ID", adm))

        logging.info("Data")
        save_data(data.find(".set.ABSORPTION"),
                  ECHA_TOX_DA_DATA,
                  ("TOX_DA_ID", adm),
                  [("timepoint", ".TIMEPOINT"),
                   ("dose", ".DOSE"),
                   ("loqualifier", ".LOQUALIFIER"),
                   ("remarks", ".REMARKS")])

def acute(substance, path):
    files = build_path(path,
                       ["toxicological information",
                        "acute toxicity",
                        "SSS"])

    for file in glob.glob(files.replace("sss", "*")):
        d = open_file(file)
        data = d("#inner")

        logging.info("Esr, %s" % get_esr(d))
        adm = save_data(data, ECHA_TOX_ACUTE_ADM,
                        [("SUBST_ID", substance),
                         ("esr", get_esr(d))],
                        [("reliability", ".reliability:first"),
                         ("test_type", ".TEST_TYPE_ACUTETOX"),
                         ("glp", ".GLP_COMPLIANCE_STATEMENT"),
                         ("testmat_indicator", ".TESTMAT_INDICATOR"),
                         ("organism", ".ORGANISM"),
                         ("sex", ".SEX"),
                         ("route", ".ROUTE"),
                         ("vehicle_tox", ".VEHICLE_TOX"),
                         ("exp_period_txt", ".EXP_PERIOD"),
                         ("interpret_rs_submitter", ".INTERPRET_RS_SUBMITTER")])
        adm = adm[0]

        logging.info("Guidelines")
        save_guidelines(data,
                        ECHA_TOX_ACUTE_GUIDELINES,
                        ("TOX_ACUTE_ID", adm))

        logging.info("Refs")
        save_refs(data,
                  ECHA_TOX_ACUTE_REF,
                  ("TOX_ACUTE_ID", adm))

        logging.info("Data")
        save_data(data.find(".set.EFFLEVEL"),
                  ECHA_TOX_ACUTE_DATA,
                  ("TOX_ACUTE_ID", adm),
                  [("sex",),
                   ("endpoint",),
                   ("loqualifier",),
                   ("exp_period_value",),
                   ("conf_limits_loqualifier",),
                   ("remarks", ".REM")])
