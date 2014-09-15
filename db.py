
from pony.orm import *

db = Database('sqlite', 'db.sqlite', create_db=True)
MAX_LENGTH=2000

# since all our fields have the same properties anyway we can just make them
# with a function, wish I started using this earlier"
def make_model(parent, id, fields):
    def inner(future_class_name, future_class_parents, future_class_attr):
        for name in fields:
            future_class_attr[name.upper()] = Optional(unicode, MAX_LENGTH)

        name, table = parent
        future_class_attr[name] = Required(table)
        future_class_attr[id] = PrimaryKey(int, auto=True)

        return type(future_class_name, future_class_parents, future_class_attr)

    return inner

def make_ref(parent, id):
    return make_model(parent, id,
                      ["reference_type", "reference_author", "reference_year",
                       "reference_title", "reference_source"])


class Substance(db.Entity):
    DOSSIER_ID = PrimaryKey(unicode)
    CAS = Optional(unicode)
    EC = Optional(unicode)
    PNECS = Set("ECHA_ECOTOX_PNEC")
    TOXICITIES = Set("ECHA_ECOTOX_TOX_ADM")
    DNELS = Set("ECHA_TOX_DNEL")
    TOXIKINETICSES = Set("ECHA_TOX_BTK_ADM")
    DERMALS = Set("ECHA_TOX_DA_ADM")
    ACUTES = Set("ECHA_TOX_ACUTE_ADM")
    ICS = Set("ECHA_TOX_IC_ADM")
    SENSS = Set("ECHA_TOX_SENS_ADM")
    RDTS = Set("ECHA_TOX_RDT_ADM")
    CRMS = Set("ECHA_TOX_CRM_ADM")
    PHYSCHEMS = Set("ECHA_PHYSCHEM_ADM")


class ECHA_ECOTOX_PNEC(db.Entity):
    SUBST_ID = Required(Substance)
    PNEC_ID = PrimaryKey(int, auto=True)
    SOURCE = Optional(unicode, MAX_LENGTH)
    COMPARTMENT = Optional(unicode, MAX_LENGTH)
    TARGET = Optional(unicode, MAX_LENGTH)
    HAC = Optional(unicode, MAX_LENGTH)
    VALUE = Optional(unicode, MAX_LENGTH)
    ASS_FAC = Optional(unicode, MAX_LENGTH)
    EXTR_METH = Optional(unicode, MAX_LENGTH)

class ECHA_ECOTOX_TOX_ADM(db.Entity):
    SUBST_ID = Required(Substance)
    TOX_ID = PrimaryKey(int, auto=True)
    TOX_TYPE = Required(unicode) # AQUATIC, TERRESTRIAL, SEDIMENT
    ESR = Optional(unicode, MAX_LENGTH)
    RELIABILITY = Optional(unicode, MAX_LENGTH)
    GUIDELINE = Optional(unicode, MAX_LENGTH)
    QUALIFIER = Optional(unicode, MAX_LENGTH)
    GLP = Optional(unicode, MAX_LENGTH)
    ORGANISM = Optional(unicode, MAX_LENGTH*3)
    TESTMAT_INDICATOR = Optional(unicode, MAX_LENGTH)
    DATAWAIVING = Optional(unicode, MAX_LENGTH)
    REFS = Set("ECHA_ECOTOX_TOX_REF")
    DATAS = Set("ECHA_ECOTOX_TOX_DATA")

class ECHA_ECOTOX_TOX_REF(db.Entity):
    TOX_ID = Required(ECHA_ECOTOX_TOX_ADM)
    TOX_REF_ID = PrimaryKey(int, auto=True)
    REFERENCE_TYPE = Optional(unicode, MAX_LENGTH)
    REFERENCE_AUTHOR = Optional(unicode, MAX_LENGTH)
    REFERENCE_YEAR = Optional(unicode, MAX_LENGTH)
    REFERENCE_TITLE = Optional(unicode, MAX_LENGTH)
    REFERENCE_SOURCE = Optional(unicode, MAX_LENGTH)

class ECHA_ECOTOX_TOX_DATA(db.Entity):
    TOX_ID = Required(ECHA_ECOTOX_TOX_ADM)
    TOX_DATA_ID = PrimaryKey(int, auto=True)
    ORGANISM = Optional(unicode, MAX_LENGTH)
    EXP_DURATION_VALUE = Optional(unicode, MAX_LENGTH)
    ENDPOINT = Optional(unicode, MAX_LENGTH)
    EFF_CONC = Optional(unicode, MAX_LENGTH)
    BASIS_CONC = Optional(unicode, MAX_LENGTH)
    EFF_CONC_TYPE = Optional(unicode, MAX_LENGTH)
    BASIS_EFFECT = Optional(unicode, MAX_LENGTH)
    REMARKS = Optional(unicode, MAX_LENGTH)


class ECHA_TOX_DNEL(db.Entity):
    SUBST_ID = Required(Substance)
    DNEL_ID = PrimaryKey(int, auto=True)
    SOURCE = Optional(unicode, MAX_LENGTH)
    TARGET = Optional(unicode, MAX_LENGTH)
    EFFECTS = Optional(unicode, MAX_LENGTH)
    EXPOSURE = Optional(unicode, MAX_LENGTH)
    HAC = Optional(unicode, MAX_LENGTH)
    VALUE = Optional(unicode, MAX_LENGTH)
    SENS_ENDP = Optional(unicode, MAX_LENGTH)
    ROUTE = Optional(unicode, MAX_LENGTH)


class ECHA_TOX_BTK_ADM(db.Entity):
    __metaclass__ = make_model(("SUBST_ID", Substance), "TOX_BTK_ID",
                               ["esr", "reliability", "type_invivo_invitro",
                                "study_objective", "glp", "testmat_indicator",
                                "datawaiving"])

    GUIDELINES = Set("ECHA_TOX_BTK_GUIDELINES")
    REFS = Set("ECHA_TOX_BTK_REF")
    DATAS = Set("ECHA_TOX_BTK_DATA")

class ECHA_TOX_BTK_GUIDELINES(db.Entity):
    __metaclass__ = make_model(("TOX_BTK_ID", ECHA_TOX_BTK_ADM), "TOX_BTK_GL_ID",
                               ["guideline", "qualifier"])


class ECHA_TOX_BTK_REF(db.Entity):
    __metaclass__ = make_ref(("TOX_BTK_ID", ECHA_TOX_BTK_ADM), "TOX_BTK_REF_ID")

class ECHA_TOX_BTK_DATA(db.Entity):
    __metaclass__ = make_model(("TOX_BTK_ID", ECHA_TOX_BTK_ADM), "TOX_BTK_DATA_ID",
                               ["organism", "sex", "route", "vehicle_tox", "exp_period",
                                "doses_concentrations", "metabolites",
                                "interpret_rs_submitter", "datawaiving"])

class ECHA_TOX_DA_ADM(db.Entity):
    __metaclass__ = make_model(("SUBST_ID", Substance), "TOX_DA_ID",
                               ["esr", "reliability", "type_invivo_invitro", "glp",
                                "testmat_indicator", "organism", "sex", "exp_period",
                                "vehicle_tox", "doses_concentrations",
                                "signs_symptoms_toxicity", "dermal_irritation",
                                "datawaiving"])

    GUIDELINES = Set("ECHA_TOX_DA_GUIDELINES")
    REFS = Set("ECHA_TOX_DA_REF")
    DATAS = Set("ECHA_TOX_DA_DATA")

class ECHA_TOX_DA_GUIDELINES(db.Entity):
    __metaclass__ = make_model(("TOX_DA_ID", ECHA_TOX_DA_ADM), "TOX_DA_GL_ID",
                                ["guideline", "qualifier"])

class ECHA_TOX_DA_REF(db.Entity):
    __metaclass__ = make_ref(("TOX_DA_ID", ECHA_TOX_DA_ADM), "TOX_DA_REF_ID")

class ECHA_TOX_DA_DATA(db.Entity):
    __metaclass__ = make_model(("TOX_DA_ID", ECHA_TOX_DA_ADM), "TOX_DA_DATA_ID",
                               ["timepoint", "dose", "loqualifier", "remarks"])

class ECHA_TOX_ACUTE_ADM(db.Entity):
    __metaclass__ = make_model(("SUBST_ID", Substance), "TOX_ACUTE_ID",
                               ["esr", "reliability", "test_type", "glp",
                                "testmat_indicator", "organism", "sex", "route",
                                "vehicle_tox", "exp_period_txt",
                                "interpret_rs_submitter", "datawaiving"])

    GUIDELINES = Set("ECHA_TOX_ACUTE_GUIDELINES")
    REFS = Set("ECHA_TOX_ACUTE_REF")
    DATAS = Set("ECHA_TOX_ACUTE_DATA")

class ECHA_TOX_ACUTE_GUIDELINES(db.Entity):
    __metaclass__ = make_model(("TOX_ACUTE_ID", ECHA_TOX_ACUTE_ADM), "TOX_ACUTE_GL_ID",
                               ["guideline", "qualifier"])

class ECHA_TOX_ACUTE_REF(db.Entity):
    __metaclass__ = make_ref(("TOX_ACUTE_ID", ECHA_TOX_ACUTE_ADM), "TOX_ACUTE_REF_ID")

class ECHA_TOX_ACUTE_DATA(db.Entity):
    __metaclass__ = make_model(("TOX_ACUTE_ID", ECHA_TOX_ACUTE_ADM), "TOX_ACUTE_DATA_ID",
                               ["sex", "endpoint", "loqualifier", "exp_period_value",
                                "conf_limits_loqualifier", "remarks",
                                "value_loqualifier"])

class ECHA_TOX_IC_ADM(db.Entity):
    __metaclass__ = make_model(("SUBST_ID", Substance), "TOX_IC_ID",
                               ["esr", "reliability", "type_invivo_invitro", "glp",
                                "testmat_indicator", "organism", "sex", "exp_period",
                                "observ_period", "vehicle_tox", "interpret_rs_submitter",
                                "criteria_submitter", "response_data", "datawaiving"])

    GUIDELINES = Set("ECHA_TOX_IC_GUIDELINES")
    REFS = Set("ECHA_TOX_IC_REF")
    DATAS = Set("ECHA_TOX_IC_DATA")

class ECHA_TOX_IC_GUIDELINES(db.Entity):
    __metaclass__ = make_model(("TOX_IC_ID", ECHA_TOX_IC_ADM), "TOX_IC_GL_ID",
                               ["guideline", "qualifier"])

class ECHA_TOX_IC_REF(db.Entity):
    __metaclass__ = make_ref(("TOX_IC_ID", ECHA_TOX_IC_ADM), "TOX_IC_REF_ID")

class ECHA_TOX_IC_DATA(db.Entity):
    __metaclass__ = make_model(("TOX_IC_ID", ECHA_TOX_IC_ADM), "TOX_IC_DATA_ID",
                               ["parameter", "basis", "timepoint", "score_loqualifier",
                                "scale", "reversibility", "remarks"])

class ECHA_TOX_SENS_ADM(db.Entity):
    __metaclass__ = make_model(("SUBST_ID", Substance), "TOX_SENS_ID",
                               ["esr", "reliability", "type_invivo_invitro", "glp",
                                "testmat_indicator", "organism", "sex", "exp_period",
                                "observ_period", "route_induction", "route_challenge",
                                "vehicle_tox", "doses_concentrations",
                                "interpret_rs_submitter", "criteria_submitter",
                                "response_data", "datawaiving"])

    GUIDELINES = Set("ECHA_TOX_SENS_GUIDELINES")
    REFS = Set("ECHA_TOX_SENS_REF")
    DATAS = Set("ECHA_TOX_SENS_DATA")

class ECHA_TOX_SENS_GUIDELINES(db.Entity):
    __metaclass__ = make_model(("TOX_SENS_ID", ECHA_TOX_SENS_ADM), "TOX_SENS_GL_ID",
                               ["guideline", "qualifier"])

class ECHA_TOX_SENS_REF(db.Entity):
    __metaclass__ = make_ref(("TOX_SENS_ID", ECHA_TOX_SENS_ADM), "TOX_SENS_REF_ID")

class ECHA_TOX_SENS_DATA(db.Entity):
    __metaclass__ = make_model(("TOX_SENS_ID", ECHA_TOX_SENS_ADM), "TOX_SENS_DATA_ID",
                               ["reading", "timepoint", "group", "number_positive",
                                "number_total", "remarks", "clinical_observ"])

class ECHA_TOX_RDT_ADM(db.Entity):
    __metaclass__ = make_model(("SUBST_ID", Substance), "TOX_RDT_ID",
                               ["esr", "reliability", "testtype_tox", "glp",
                                "testmat_indicator", "organism", "sex", "exp_period",
                                "frequency", "route", "vehicle_tox", "datawaiving"])

    GUIDELINES = Set("ECHA_TOX_RDT_GUIDELINES")
    REFS = Set("ECHA_TOX_RDT_REF")
    DATAS = Set("ECHA_TOX_RDT_DATA")

class ECHA_TOX_RDT_GUIDELINES(db.Entity):
    __metaclass__ = make_model(("TOX_RDT_ID", ECHA_TOX_RDT_ADM), "TOX_RDT_GL_ID",
                               ["guideline", "qualifier"])

class ECHA_TOX_RDT_REF(db.Entity):
    __metaclass__ = make_ref(("TOX_RDT_ID", ECHA_TOX_RDT_ADM), "TOX_RDT_REF_ID")

class ECHA_TOX_RDT_DATA(db.Entity):
    __metaclass__ = make_model(("TOX_RDT_ID", ECHA_TOX_RDT_ADM), "TOX_RDT_DATA_ID",
                               ["endpoint", "loqualifier", "sex", "eff_conc_type",
                                "remarks"])


class ECHA_TOX_CRM_ADM(db.Entity):
    __metaclass__ = make_model(("SUBST_ID", Substance), "TOX_CRM_ID",
                               ["esr", "reliability", "genotoxicity_type",
                                "studytype", "testtype_tox", "glp", "testmat_indicator",
                                "organism", "sex", "route", "vehicle_tox", "exp_period",
                                "frequency", "test_period", "interpret_rs_submitter",
                                "rs_maternal_tox", "rs_embryotox_tera", "datawaiving"])

    GUIDELINES = Set("ECHA_TOX_CRM_GUIDELINES")
    REFS = Set("ECHA_TOX_CRM_REF")
    DATAS = Set("ECHA_TOX_CRM_DATA")
    RESULTS = Set("ECHA_TOX_CRM_RESULT")

class ECHA_TOX_CRM_GUIDELINES(db.Entity):
    __metaclass__ = make_model(("TOX_CRM_ID", ECHA_TOX_CRM_ADM), "TOX_CRM_GL_ID",
                               ["guideline", "qualifier"])

class ECHA_TOX_CRM_REF(db.Entity):
    __metaclass__ = make_ref(("TOX_CRM_ID", ECHA_TOX_CRM_ADM), "TOX_CRM_REF_ID")

class ECHA_TOX_CRM_RESULT(db.Entity):
    __metaclass__ = make_model(("TOX_CRM_ID", ECHA_TOX_CRM_ADM), "TOX_CRM_MUTA_DATA_ID",
                               ["organism", "met_act_indicator", "testsystem", "sex",
                                "genotoxicity", "toxicity", "cytotoxicity",
                                "veh_contr_valid", "neg_contr_valid", "pos_contr_valid"])

class ECHA_TOX_CRM_DATA(db.Entity):
    __metaclass__ = make_model(("TOX_CRM_ID", ECHA_TOX_CRM_ADM), "TOX_CRM_CARD_DATA_ID",
                               ["endpoint", "effecttype", "loqualifier", "sex",
                                "generation"])

class ECHA_PHYSCHEM_ADM(db.Entity):
    __metaclass__ = make_model(("SUBST_ID", Substance), "PHYSCHEM_ID",
                               ["esr", "reliability", "method_type", "partcoeff_type",
                                "testtype", "glp", "testmat_indicator",
                                "interpretation_results", "org_solvents_stability",
                                "org_solvents_degrad", "dissociation_indicator",
                                "distribution_type", "datawaiving"])

    GUIDELINES = Set("ECHA_PHYSCHEM_GUIDELINES")
    REFS = Set("ECHA_PHYSCHEM_REF")
    APPEARANCES = Set("ECHA_PHYSCHEM_APPEARANCE")
    MELTINGS = Set("ECHA_PHYSCHEM_MELTING")
    BOILINGS = Set("ECHA_PHYSCHEM_BOILING")
    DENSITIES = Set("ECHA_PHYSCHEM_DENSITY")
    VPRESSURES = Set("ECHA_PHYSCHEM_VPRESSURE")
    PARTCS = Set("ECHA_PHYSCHEM_PARTC")
    WSOLBS = Set("ECHA_PHYSCHEM_WSOLUBILITY")
    STENSIONS = Set("ECHA_PHYSCHEM_STENSION")
    FPOINTS = Set("ECHA_PHYSCHEM_FPOINT")
    AUTOFLAMS = Set("ECHA_PHYSCHEM_AUTOFLAM")
    FLAMS = Set("ECHA_PHYSCHEM_FLAMMABILITY")
    OXIDIZINGS = Set("ECHA_PHYSCHEM_OXIDIZING_PROP")
    SOLDEGRADS = Set("ECHA_PHYSCHEM_ORG_SOL_DEGRADATION")
    DISSCOS = Set("ECHA_PHYSCHEM_DISSCO")
    PHS = Set("ECHA_PHYSCHEM_PH")
    VISCOSITIES = Set("ECHA_PHYSCHEM_VISCOSITY")
    MMDS = Set("ECHA_PHYSCHEM_GRANULOMETRY_MMD")
    PSS = Set("ECHA_PHYSCHEM_GRANULOMETRY_PS")
    DISTS = Set("ECHA_PHYSCHEM_GRANULOMETRY_DIST")

class ECHA_PHYSCHEM_GUIDELINES(db.Entity):
    __metaclass__ = make_model(("PHYSCHEM_ID", ECHA_PHYSCHEM_ADM), "PHYSCHEM_GL_ID",
                               ["guideline", "qualifier"])

class ECHA_PHYSCHEM_REF(db.Entity):
    __metaclass__ = make_ref(("PHYSCHEM_ID", ECHA_PHYSCHEM_ADM), "PHYSCHEM_REF_ID")

class ECHA_PHYSCHEM_APPEARANCE(db.Entity):
    __metaclass__ = make_model(("PHYSCHEM_ID", ECHA_PHYSCHEM_ADM), "PHYSCHEM_APP_ID",
                               ["physical_state", "form", "colour", "odour", "type"])

class ECHA_PHYSCHEM_MELTING(db.Entity):
    __metaclass__ = make_model(("PHYSCHEM_ID", ECHA_PHYSCHEM_ADM), "PHYSCHEM_MELT_ID",
                               ["loqualifier", "pressure", "decomp_indicator",
                                "sublimation_indicator"])

class ECHA_PHYSCHEM_BOILING(db.Entity):
    __metaclass__ = make_model(("PHYSCHEM_ID", ECHA_PHYSCHEM_ADM), "PHYSCHEM_BOILING_ID",
                               ["loqualifier", "pressure", "decomp_indicator",
                                "sublimation_indicator"])

class ECHA_PHYSCHEM_DENSITY(db.Entity):
    __metaclass__ = make_model(("PHYSCHEM_ID", ECHA_PHYSCHEM_ADM), "PHYSCHEM_DENSITY_ID",
                               ["type", "loqualifier", "temp_value"])

class ECHA_PHYSCHEM_VPRESSURE(db.Entity):
    __metaclass__ = make_model(("PHYSCHEM_ID", ECHA_PHYSCHEM_ADM), "PHYSCHEM_VP_ID",
                               ["loqualifier", "temp_value"])

class ECHA_PHYSCHEM_PARTC(db.Entity):
    __metaclass__ = make_model(("PHYSCHEM_ID", ECHA_PHYSCHEM_ADM), "PHYSCHEM_PARTC_ID",
                               ["type", "loqualifier", "temp_value", "ph_loqualifier"])

class ECHA_PHYSCHEM_WSOLUBILITY(db.Entity):
    __metaclass__ = make_model(("PHYSCHEM_ID", ECHA_PHYSCHEM_ADM), "PHYSCHEM_WS_ID",
                               ["loqualifier", "temp_value", "ph_loqualifier"])

class ECHA_PHYSCHEM_STENSION(db.Entity):
    __metaclass__ = make_model(("PHYSCHEM_ID", ECHA_PHYSCHEM_ADM), "PHYSCHEM_ST_ID",
                               ["loqualifier", "temp_value", "conc_value"])

class ECHA_PHYSCHEM_FPOINT(db.Entity):
    __metaclass__ = make_model(("PHYSCHEM_ID", ECHA_PHYSCHEM_ADM), "PHYSCHEM_FPOINT_ID",
                               ["loqualifier", "press_loqualifier"])

class ECHA_PHYSCHEM_AUTOFLAM(db.Entity):
    __metaclass__ = make_model(("PHYSCHEM_ID", ECHA_PHYSCHEM_ADM), "PHYSCHEM_AF_ID",
                               ["loqualifier", "press_loqualifier"])

class ECHA_PHYSCHEM_FLAMMABILITY(db.Entity):
    __metaclass__ = make_model(("PHYSCHEM_ID", ECHA_PHYSCHEM_ADM), "PHYSCHEM_FLAMM_ID",
                               ["pyrophoric_properties", "loexplos_limit",
                                "upexplos_limit", "interpret_results_subm"])

class ECHA_PHYSCHEM_OXIDIZING_PROP(db.Entity):
    __metaclass__ = make_model(("PHYSCHEM_ID", ECHA_PHYSCHEM_ADM), "PHYSCHEM_OXI_ID",
                               ["parameter", "loqualifier", "remarks"])

class ECHA_PHYSCHEM_ORG_SOL_DEGRADATION(db.Entity):
    __metaclass__ = make_model(("PHYSCHEM_ID", ECHA_PHYSCHEM_ADM), "PHYSCHEM_OSD_ID",
                               ["no", "identifier", "identity"])

class ECHA_PHYSCHEM_DISSCO(db.Entity):
    __metaclass__ = make_model(("PHYSCHEM_ID", ECHA_PHYSCHEM_ADM), "PHYSCHEM_DISSCO_ID",
                               ["no", "value_loqualifier", "temp_value", "remarks"])

class ECHA_PHYSCHEM_PH(db.Entity):
    __metaclass__ = make_model(("PHYSCHEM_ID", ECHA_PHYSCHEM_ADM), "PHYSCHEM_PH_ID",
                               ["loqualifier", "temp_value", "conc_loqualifier",
                                "remarks"])

class ECHA_PHYSCHEM_VISCOSITY(db.Entity):
    __metaclass__ = make_model(("PHYSCHEM_ID", ECHA_PHYSCHEM_ADM), "PHYSCHEM_VISCO_ID",
                               ["loqualifier", "temp_value", "remarks"])

class ECHA_PHYSCHEM_GRANULOMETRY_MMD(db.Entity):
    __metaclass__ = make_model(("PHYSCHEM_ID", ECHA_PHYSCHEM_ADM), "PHYSCHEM_GMT_MMD_ID",
                               ["loqualifier", "remarks"])

class ECHA_PHYSCHEM_GRANULOMETRY_PS(db.Entity):
    __metaclass__ = make_model(("PHYSCHEM_ID", ECHA_PHYSCHEM_ADM), "PHYSCHEM_GMT_PS_ID",
                               ["percentile", "loqualifier", "remarks"])

class ECHA_PHYSCHEM_GRANULOMETRY_DIST(db.Entity):
    __metaclass__ = make_model(("PHYSCHEM_ID", ECHA_PHYSCHEM_ADM), "PHYSCHEM_GMT_DIST_ID",
                               ["size_loqualifier", "dist_loqualifier", "remarks"])


db.generate_mapping(create_tables=True)



def find_or_create(model, **kwargs):
    if not any(has_len(value) for k, value in kwargs.items()):
        return None

    kwargs = {key: max_len(value) for key, value in kwargs.items()}
    obj = model.get(**kwargs)
    if obj == None:
        obj = model(**kwargs)

    return obj

def max_len(value):
    return value[:MAX_LENGTH] if type(value) == str and len(value) > MAX_LENGTH else value

def has_len(value):
    return len(value) > 0 if type(value) == str else False
