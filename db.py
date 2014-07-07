
from pony.orm import *

db = Database('sqlite', 'db.sqlite', create_db=True)
MAX_LENGTH=6000


class Substance(db.Entity):
    DOSSIER_ID = PrimaryKey(unicode)
    CAS = Optional(unicode)
    EC = Optional(unicode)
    PNECS = Set("ECHA_ECOTOX_PNEC")
    TOXICITIES = Set("ECHA_ECOTOX_TOX_ADM")
    DNELS = Set("ECHA_TOX_DNEL")

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
    ORGANISM = Optional(unicode, MAX_LENGTH*3)
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

db.generate_mapping(create_tables=True)



def find_or_create(model, **kwargs):
    obj = model.get(**kwargs)
    if obj == None:
        obj = model(**kwargs)

    return obj
