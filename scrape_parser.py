
import os, tarfile, glob, re
from pony.orm import *
from slugify import slugify
from pyquery import PyQuery as pq

db = Database('sqlite', 'db.sqlite', create_db=True)

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
    SOURCE = Optional(unicode)
    COMPARTMENT = Optional(unicode)
    TARGET = Optional(unicode)
    HAC = Optional(unicode)
    VALUE = Optional(unicode)
    UNIT = Optional(unicode)
    ASS_FAC = Optional(unicode)
    EXTR_METH = Optional(unicode)

class ECHA_ECOTOX_TOX_ADM(db.Entity):
    SUBST_ID = Required(Substance)
    TOX_ID = PrimaryKey(int, auto=True)
    TOX_TYPE = Required(unicode) # AQUA, TERRESTRIAL, SEDIMENT
    ESR = Optional(unicode)
    RELIABILITY = Optional(unicode)
    GUIDELINE = Optional(unicode)
    QUALIFIER = Optional(unicode)
    GLP = Optional(unicode)
    ORGANISM = Optional(unicode)
    REFS = Set("ECHA_ECOTOX_TOX_REF")
    DATAS = Set("ECHA_ECOTOX_TOX_DATA")

class ECHA_ECOTOX_TOX_REF(db.Entity):
    TOX_ID = Required(ECHA_ECOTOX_TOX_ADM)
    TOX_REF_ID = PrimaryKey(int, auto=True)
    REFERENCE_TYPE = Optional(unicode)
    REFERENCE_AUTHOR = Optional(unicode)
    REFERENCE_YEAR = Optional(unicode)
    REFERENCE_TITLE = Optional(unicode)
    REFERENCE_SOURCE = Optional(unicode)

class ECHA_ECOTOX_TOX_DATA(db.Entity):
    TOX_ID = Required(ECHA_ECOTOX_TOX_ADM)
    TOX_DATA_ID = PrimaryKey(int, auto=True)
    ORGANISM = Optional(unicode)
    EXP_DURATION_VALUE = Optional(unicode)
    EXP_DURATION_UNIT = Optional(unicode)
    ENDPOINT = Optional(unicode)
    EFF_CONC = Optional(unicode)
    EFF_CONC_UNIT = Optional(unicode)
    BASIC_CONC = Optional(unicode)
    EFF_CONC_TYPE = Optional(unicode)
    BASIS_EFFECT = Optional(unicode)
    REMARKS = Optional(unicode)


class ECHA_TOX_DNEL(db.Entity):
    SUBST_ID = Required(Substance)
    DNEL_ID = PrimaryKey(int, auto=True)
    SOURCE = Optional(unicode)
    TARGET = Optional(unicode)
    EFFECTS = Optional(unicode)
    EXPOSURE = Optional(unicode)
    HAC = Optional(unicode)
    VALUE = Optional(unicode)
    UNIT = Optional(unicode)
    SENS_ENDP = Optional(unicode)
    ROUTE = Optional(unicode)

db.generate_mapping(create_tables=True)

def find_or_create(model, **kwargs):
    obj = model.get(**kwargs)
    if obj == None:
        obj = model(**kwargs)

    return obj

def build_path(base, parts):
    return "%s.html" % os.path.join(base,
                            "__".join([slugify(part) for part in parts]))

def open_file(path):
    return pq(re.sub(r'xmlns="[^ ]+"', '', open(path).read()))

@db_session
def ecotoxicological(substance, path):
    files = build_path(path,
                       ["ecotoxicological information",
                        "ecotoxicological information NNN"])

    for file in glob.glob(files.replace("nnn", "*")):
        d = open_file(file)

        source = d("#toc li").filter(
            lambda i, this: pq(this).children("p").size() == 1 and pq(this).children("p").text() == "Ecotoxicological Information").find(".EndpointSummary:first").text()

        for target in d("h4"):
            target = d(target)
            section = target.parents(".section")

            compartment = section.find("h3").text()
            target_text = target.text()

            hac = target.siblings("div").find("div.field").filter(lambda i, this: pq(this).children(".label").text() == "Hazard assessment conclusion").find(".value").text()
            print ""

@db_session
def parse(path):
    path = unpack(path)

    substance = find_or_create(Substance, DOSSIER_ID=os.path.split(path)[1])

    ecotoxicological(substance, path)

def unpack(path):
    unpacked = os.path.join(os.path.join(os.getcwd(), "data"),
                            os.path.split(path)[1].replace(".tar.gz", ""))

    if not os.path.exists(unpacked):
        with tarfile.open(path, "r:gz") as tar:
            tar.extractall(os.path.join(os.getcwd(), "data"))

    return unpacked

if __name__ == "__main__":

    for file in os.listdir(os.path.join(os.getcwd(), "data")):
        if file.startswith("DISS") and file.endswith(".tar.gz"):
            parse(os.path.join(os.getcwd(), "data", file))
