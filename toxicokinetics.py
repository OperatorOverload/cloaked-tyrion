
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
            reliability = value_by_select(data, ".reliability:first"),
            type_invivo_invitro = value_by_select(data, ".TYPE_INVIVO_INVITRO"),
            study_objective = value_by_select(data, ".STUDY_OBJECTIVE"),
            glp = value_by_select(data, ".GLP_COMPLIANCE_STATEMENT"),
            testmat_indicator = value_by_select(data, ".TESTMAT_INDICATOR"),
            datawaiving = value_by_select(data, ".dataWaiving"))

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
        save_data(data.find("#GEN_RESULTS_HD"),
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
                         ("dermal_irritation", ".DERMAL_IRRITATION"),
                         ("datawaiving", ".dataWaiving")])
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
                         ("sex", ".SEX:first"),
                         ("route", ".ROUTE"),
                         ("vehicle_tox", ".VEHICLE_TOX"),
                         ("exp_period_txt", ".EXP_PERIOD"),
                         ("interpret_rs_submitter", ".INTERPRET_RS_SUBMITTER"),
                         ("datawaiving", ".dataWaiving")])
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
                   ("remarks", ".REM"),
                   ("value_loqualifier",)])

def irritation(substance, path):
    files = build_path(path,
                       ["toxicological information",
                        "irritation corrosion",
                        "SSS"])

    for file in glob.glob(files.replace("sss", "*")):
        d = open_file(file)
        data = d("#inner")

        logging.info("Esr, %s" % get_esr(d))
        adm = save_data(data, ECHA_TOX_IC_ADM,
                        [("SUBST_ID", substance),
                         ("esr", get_esr(d))],
                        [("reliability", ".reliability:first"),
                         ("type_invivo_invitro",),
                         ("glp", ".GLP_COMPLIANCE_STATEMENT"),
                         ("testmat_indicator",),
                         ("organism",),
                         ("sex",),
                         ("exp_period",),
                         ("observ_period",),
                         ("vehicle_tox",),
                         ("interpret_rs_submitter",),
                         ("criteria_submitter",),
                         ("response_data",),
                         ("datawaiving", ".dataWaiving")])
        adm = adm[0]

        logging.info("Guidelines")
        save_guidelines(data, ECHA_TOX_IC_GUIDELINES,
                        ("TOX_IC_ID", adm))

        logging.info("Refs")
        save_refs(data, ECHA_TOX_IC_REF,
                  ("TOX_IC_ID", adm))

        logging.info("Data")
        save_data(data.find("#GEN_RESULTS_HD .OVERALL_RS"), ECHA_TOX_IC_DATA,
                            ("TOX_IC_ID", adm),
                            [("parameter",),
                             ("basis",),
                             ("timepoint",),
                             ("score_loqualifier",),
                             ("scale",),
                             ("reversibility",),
                             ("remarks", ".REM")])

def sensitisation(substance, path):
    def step(d, data, file):
        adm = save_data(data, ECHA_TOX_SENS_ADM,
                        [("SUBST_ID", substance),
                         ("esr", get_esr(d))],
                        make_fields(
                            [("reliability", ".reliability:first"),
                             ("glp", ".GLP_COMPLIANCE_STATEMENT"),
                             ("datawaiving", ".dataWaiving")],
                            ["type_invivo_invitro",
                             "testmat_indicator",
                             "organism",
                             "sex",
                             "exp_period",
                             "observ_period",
                             "route_induction",
                             "route_challenge",
                             "vehicle_tox",
                             "doses_concentrations",
                             "interpret_rs_submitter",
                             "criteria_submitter",
                             "response_data"]))
        adm = adm[0]

        save_guidelines(data, ECHA_TOX_SENS_GUIDELINES,
                        ("TOX_SENS_ID", adm))

        save_refs(data, ECHA_TOX_SENS_REF,
                  ("TOX_SENS_ID", adm))

        save_data(data.find("#GEN_RESULTS_HD"), ECHA_TOX_SENS_DATA,
                  ("TOX_SENS_ID", adm),
                  make_fields([("remarks", ".REM")],
                              ["reading",
                               "timepoint",
                               "group",
                               "number_positive",
                               "number_total"]))


    parse_files(path, ["toxicological information", "sensitisation", "SSS"], step)

def repeated_dose(substance, path):
    def step(d, data, file):
        adm = save_data(data, ECHA_TOX_RDT_ADM,
                        [("SUBST_ID", substance),
                         ("esr", get_esr(d))],
                        make_fields([("reliability", ".reliability:first"),
                                     ("glp", ".GLP_COMPLIANCE_STATEMENT"),
                                     ("datawaiving", ".dataWaiving")],
                                    ["testtype_tox",
                                     "testmat_indicator",
                                     "organism",
                                     "sex",
                                     "exp_period",
                                     "frequency",
                                     "route",
                                     "vehicle_tox"]))
        adm = adm[0]

        save_guidelines(data, ECHA_TOX_RDT_GUIDELINES,
                        ("TOX_RDT_ID", adm))

        save_refs(data, ECHA_TOX_RDT_REF,
                  ("TOX_RDT_ID", adm))

        save_data(data.find("#GEN_RESULTS_HD"), ECHA_TOX_RDT_DATA,
                  ("TOX_RDT_ID", adm),
                  make_fields([("remarks", ".REM")],
                              ["endpoint",
                               "loqualifier",
                               "sex",
                               "eff_conc_type"]))

    parse_files(path,
                ["toxicological information", "repeated dose toxicity", "SSS"],
                step)

def genetic(substance, path):
    def step(d, data, file):
        adm = save_data(data, ECHA_TOX_CRM_ADM,
                        [("SUBST_ID", substance),
                         ("esr", get_esr(d))],
                        make_fields([("reliability", ".reliability:first"),
                                     ("glp", ".GLP_COMPLIANCE_STATEMENT"),
                                     ("datawaiving", ".dataWaiving")],
                                    ["genotoxicity_type",
                                     "studytype",
                                     "testtype_tox",
                                     "testmat_indicator",
                                     "organism",
                                     "sex",
                                     "route",
                                     "vehicle_tox",
                                     "exp_period",
                                     "frequency",
                                     "test_period",
                                     "interpret_rs_submitter",
                                     "rs_maternal_tox",
                                     "rs_embryotox_tera"]))
        adm = adm[0]

        save_guidelines(data, ECHA_TOX_CRM_GUIDELINES,
                        ("TOX_CRM_ID", adm))

        save_refs(data, ECHA_TOX_CRM_REF,
                  ("TOX_CRM_ID", adm))

        study_type = "genetic"
        if "carcinogenicity" in file:
            study_type = "carcinogenicity"
        if "toxicity-to-reproduction" in file:
            study_type = "reproduction"

        table = {
            "genetic": ECHA_TOX_CRM_MUTA_DATA,
            "carcinogenicity": ECHA_TOX_CRM_CARC_DATA,
            "reproduction": ECHA_TOX_CRM_REPR_DATA
        }
        fields = {
            "genetic": make_fields([],
                                   ["organism", "met_act_indicator", "testsystem",
                                    "sex", "genotoxicity", "toxicity", "cytotoxicity",
                                    "veh_contr_valid", "neg_contr_valid",
                                    "pos_contr_valid"]),
            "carcinogenicity": make_fields([],
                                           ["endpoint", "effecttype", "loqualifier",
                                            "sex"]),
            "reproduction": make_fields([],
                                        ["endpoint", "effecttype", "generation",
                                         "sex", "loqualifier"])
        }

        save_data(data.find("#GEN_RESULTS_HD"), table[study_type],
                  ("TOX_CRM_ID", adm),
                  fields[study_type])


    map(lambda f: parse_files(path,
                              ["toxicological information", f, "SSS"],
                              step),
        ["genetic toxicity", "carcinogenicity", "toxicity to reproduction"])
