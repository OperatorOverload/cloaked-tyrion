
import os, tarfile, glob, re, codecs, shutil
from pony.orm import *
from slugify import slugify
from pyquery import PyQuery as pq

db = Database('sqlite', 'db.sqlite', create_db=True)
MAX_LENGTH=600

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
    UNIT = Optional(unicode, MAX_LENGTH)
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
    ORGANISM = Optional(unicode, MAX_LENGTH)
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
    EXP_DURATION_UNIT = Optional(unicode, MAX_LENGTH)
    ENDPOINT = Optional(unicode, MAX_LENGTH)
    EFF_CONC = Optional(unicode, MAX_LENGTH)
    EFF_CONC_UNIT = Optional(unicode, MAX_LENGTH)
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
    UNIT = Optional(unicode, MAX_LENGTH)
    SENS_ENDP = Optional(unicode, MAX_LENGTH)
    ROUTE = Optional(unicode, MAX_LENGTH)

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
    return pq(re.sub(r'xmlns="[^ ]+"', u'', codecs.open(path, encoding="utf-8").read()))

def class_ends(data, end):
    return data.filter(lambda i, this: pq(this).attr("class").endswith(end))

def pick_by_label(data, label):
    return data.find("div.field").filter(
        lambda i, this: pq(this).find(".label").text() == label)

def value_by_select(data, selector):
    return data.find("%s .value" % selector).text()

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

            data = target.siblings("div").find("div.field")

            hac = class_ends(data, "_NO").find(".value").text()
            value = class_ends(data, "_VALUE").find(".value span:first").text()
            unit = class_ends(data, "_VALUE").find(".value span:last").text()
            ass_fac = class_ends(data, "_ASS_FAC").find(".value").text()
            extr_meth = class_ends(data, "_EXTR_METH").find(".value").text()

            pnec = find_or_create(ECHA_ECOTOX_PNEC,
                           SUBST_ID=substance,
                           SOURCE=source,
                           COMPARTMENT=compartment,
                           TARGET=target_text,
                           HAC=hac,
                           VALUE=value,
                           UNIT=unit,
                           ASS_FAC=ass_fac,
                           EXTR_METH=extr_meth)

def aquatic(substance, path):
    files = build_path(path,
                       ["ecotoxicological information",
                        "aquatic toxicity",
                        "thingsthingsthings"])

    toxicity(files, substance, "AQUATIC")

def terrestrial(substance, path):
    files = build_path(path,
                       ["ecotoxicological information",
                        "terrestrial toxicity",
                        "thingsthingsthings"])
    toxicity(files, substance, "TERRESTRIAL")

def sediment(substance, path):
    files = build_path(path,
                       ["ecotoxicological information",
                        "sediment toxicity",
                        "thingsthingsthings"])
    toxicity(files, substance, "SEDIMENT")

@db_session
def toxicity(files, substance, tox_type):
    for file in glob.glob(files.replace("thingsthingsthings", "*")):
        d = open_file(file)
        data = d("#inner")

        esr = d("#page_header h2").text()
        reliability = pick_by_label(data, "Reliability").find(".value").text()
        guideline = pick_by_label(data, "Guideline").find(".value").text()
        qualifier = pick_by_label(data, "Qualifier").find(".value").text()
        glp = data.find(".GLP_COMPLIANCE_STATEMENT").find(".value").text()
        organism = data.find(".ORGANISM").find(".value:first").text()

        aqua_adm = find_or_create(ECHA_ECOTOX_TOX_ADM,
                                  SUBST_ID=substance,
                                  TOX_TYPE=tox_type,
                                  ESR=esr,
                                  RELIABILITY=reliability,
                                  GUIDELINE=guideline,
                                  QUALIFIER=qualifier,
                                  GLP=glp,
                                  ORGANISM=organism)

        references(aqua_adm, data)
        datas(aqua_adm, data)

@db_session
def references(aqua_adm, data):
    print "References for", aqua_adm.ESR
    for ref in data.find("#GEN_DATA_SOURCE_HD .set"):
        ref = pq(ref)

        reference = find_or_create(
            ECHA_ECOTOX_TOX_REF,
            TOX_ID=aqua_adm,
            REFERENCE_TYPE=value_by_select(ref, ".REFERENCE_TYPE"),
            REFERENCE_AUTHOR=value_by_select(ref, ".REFERENCE_AUTHOR"),
            REFERENCE_YEAR=value_by_select(ref, ".REFERENCE_YEAR"),
            REFERENCE_TITLE=value_by_select(ref, ".REFERENCE_TITLE"),
            REFERENCE_SOURCE=value_by_select(ref, ".REFERENCE_SOURCE"))

@db_session
def datas(aqua_adm, data):
    print "Datas for", aqua_adm.ESR
    for data in data.find("#GEN_RESULTS_HD .set"):
        data = pq(data)

        duration_value = data.find(".EXP_DURATION_VALUE .value span:first").text()
        duration_unit = data.find(".EXP_DURATION_VALUE .value span:last").text()

        eff_conc = data.find(".LOQUALIFIER .value span:first").text()
        eff_conc_unit = data.find(".LOQUALIFIER .value span:last").text()

        datum = find_or_create(
            ECHA_ECOTOX_TOX_DATA,
            TOX_ID=aqua_adm,
            ORGANISM=value_by_select(data, ".ORGANISM"),
            EXP_DURATION_VALUE=duration_value,
            EXP_DURATION_UNIT=duration_unit,
            ENDPOINT=value_by_select(data, ".ENDPOINT"),
            EFF_CONC=eff_conc,
            EFF_CONC_UNIT=eff_conc_unit,
            BASIS_CONC=value_by_select(data, ".BASIS_CONC"),
            EFF_CONC_TYPE=value_by_select(data, ".EFF_CONC_TYPE"),
            BASIS_EFFECT=value_by_select(data, ".BASIS_EFFECT"),
            REMARKS=value_by_select(data, ".REM"))

@db_session
def dnel(substance, path):
    files = build_path(path,
                       ["toxicological information",
                        "toxicological information NNN"])

    for file in glob.glob(files.replace("nnn", "*")):
        d = open_file(file)
        data = d("#inner")

        source = d("#page_header h2").text()
        exposures = data.find("h5").filter(lambda i, this: not pq(this).text().startswith("DN(M)EL"))

        for exposure in exposures:
            exposure = pq(exposure)
            data = exposure.parent().find("div.field")

            target = exposure.parents(".section").find("h3").text()
            effects = exposure.parent().parent().find("h4").text()
            hac = class_ends(data, "_DNMEL").find(".value").text()
            value = class_ends(data, "_DNMEL_VALUE").find(".value span:first").text()
            unit = class_ends(data, "_DNMEL_VALUE").find(".value span:last").text()
            sens_endp = class_ends(data, "_SENS_ENDP").find(".value").text()
            route = class_ends(data, "_ROUTE").find(".value").text()

            toxicological = find_or_create(ECHA_TOX_DNEL,
                                           SUBST_ID=substance,
                                           SOURCE=source,
                                           TARGET=target,
                                           EFFECTS=effects,
                                           EXPOSURE=exposure.text(),
                                           HAC=hac,
                                           VALUE=value,
                                           UNIT=unit,
                                           SENS_ENDP=sens_endp,
                                           ROUTE=route)

@db_session
def parse(path):
    path = unpack(path)
    dossier_id = os.path.split(path)[1]

    substance = find_or_create(Substance, DOSSIER_ID=dossier_id)

    print "Ecotoxicity for", dossier_id
    ecotoxicological(substance, path)
    print "Aquatic toxicity for", dossier_id
    aquatic(substance, path)
    print "Terrestrial toxicity for", dossier_id
    terrestrial(substance, path)
    print "Sediment toxicity for", dossier_id
    sediment(substance, path)
    print "Dnels for", dossier_id
    dnel(substance, path)

def unpack(path):
    unpacked = os.path.join(os.path.join(os.getcwd(), "data"),
                            os.path.split(path)[1].replace(".tar.gz", ""))

    if not os.path.exists(unpacked):
        with tarfile.open(path, "r:gz") as tar:
            tar.extractall(os.path.join(os.getcwd(), "data"))

    return unpacked

def cleanup(path):
    shutil.rmtree(path.replace(".tar.gz", ""))


if __name__ == "__main__":

    for file in os.listdir(os.path.join(os.getcwd(), "data")):
        if file.startswith("DISS") and file.endswith(".tar.gz"):
            parse(os.path.join(os.getcwd(), "data", file))
            cleanup(os.path.join(os.getcwd(), "data", file))
