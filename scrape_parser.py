
import os, tarfile, glob, re, codecs, shutil, logging
from pony.orm import *
from slugify import slugify
from pyquery import PyQuery as pq

from db import *
from helpers import *

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)


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
            value = class_ends(data, "_VALUE").find(".value").html() or ""
            ass_fac = class_ends(data, "_ASS_FAC").find(".value").text()
            extr_meth = class_ends(data, "_EXTR_METH").find(".value").text()

            pnec = find_or_create(ECHA_ECOTOX_PNEC,
                           SUBST_ID=substance,
                           SOURCE=source,
                           COMPARTMENT=compartment,
                           TARGET=target_text,
                           HAC=hac,
                           VALUE=value,
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

def bioacc(substance, path):
    def more_stuff(adm):
        def step(d, data, file):
            save_data(data.find(".set.BCF"), ECHA_ECOTOX_TOX_BCF,
                                ("TOX_ID", adm),
                                make_fields([],
                                            ["type", "loqualifier"]))

        parse_files(path,
                    ["environmental fate and pathways", "bioaccumulation",
                     "sss", "sss"],
                     step)

    files = build_path(path,
                       ["environmental fate and pathways",
                        "bioaccumulation",
                        "thingsthingsthings"])
    toxicity(files, substance, "BIOACC", more_stuff)

def biodegrad(substance, path):
    def more_stuff(adm):
        def step1(d, data, file):
            save_data(data.find(".set.DEGRAD"), ECHA_ECOTOX_TOX_BIODEGRAD,
                      ("TOX_ID", adm),
                      make_fields([],
                                  ["soilnumber", "loqualifier", "stdev", "parameter",
                                   "timepoint_value", "rem"]))

        def step2(d, data, file):
            save_data(data.find(".set.BOD5"), ECHA_ECOTOX_TOX_BOD,
                      ("TOX_ID", adm),
                      make_fields([],
                                  ["parameter", "loqualifier"]))

        def step3(d, data, file):
            save_data(data.find(".set.TRANSF_PRODUCTS_ID"), ECHA_ECOTOX_TOX_DEGPROD,
                      ("TOX_ID", adm),
                      make_fields([("identifier", ".ID")],
                                  ["no", "identifier"]))

        parse_files(path,
                    ["environmental fate and pathways", "biodegradation",
                     "SSS", "SSS"],
                     step1)

        parse_files(path,
                    ["environmental fate and pathways", "biodegradation",
                     "SSS", "SSS"],
                     step2)

        parse_files(path,
                    ["environmental fate and pathways", "biodegradation",
                     "SSS", "SSS"],
                     step3)


    files = build_path(path,
                       ["environmental fate and pathways",
                        "biodegradation",
                        "thingsthingsthings"])
    toxicity(files, substance, "BIODEGRAD", more_stuff)



@db_session
def toxicity(files, substance, tox_type, extra=None):
    for file in glob.glob(files.replace("thingsthingsthings", "*")):
        d = open_file(file)
        data = d("#inner")

        esr = d("#page_header h2").text()
        reliability = pick_by_label(data, "Reliability").find(".value").text()
        glp = value_by_select(data, ".GLP_COMPLIANCE_STATEMENT")
        organism = value_by_select(data, ".ORGANISM")
        testmat = value_by_select(data, ".TESTMAT_INDICATOR")
        datawaiving = value_by_select(data, ".dataWaiving")

        aqua_adm = find_or_create(ECHA_ECOTOX_TOX_ADM,
                                  SUBST_ID=substance,
                                  TOX_TYPE=tox_type,
                                  ESR=esr,
                                  RELIABILITY=reliability,
                                  GLP=glp,
                                  ORGANISM=organism,
                                  TESTMAT_INDICATOR=testmat,
                                  DATAWAIVING=datawaiving,
                                  TEST_TYPE=value_by_select(data, ".TEST_TYPE"),
                                  OXYGEN_CONDITIONS=value_by_select(data, ".OXYGEN_CONDITIONS"),
                                  INOCULUM=value_by_select(data, ".INOCULUM"),
                                  REFERENCE_SUBSTANCE=value_by_select(data, ".REFERENCE_SUBSTANCE"),
                                  VALIDITY_CRIT_SUBM=value_by_select(data, ".VALIDITY_CRIT_SUBM"),
                                  INTERPRET_RESULTS_SUBM=value_by_select(data, ".INTERPRETER_RESULTS_SUBM"))

        references(aqua_adm, data)
        datas(aqua_adm, data)
        save_guidelines(data, ECHA_ECOTOX_TOX_GUIDELINES,
                        ("TOX_ID", aqua_adm))

        if extra:
            extra(aqua_adm)

@db_session
def references(aqua_adm, data):
    logging.info("References for %s" % aqua_adm.ESR)
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
    logging.info("Datas for %s" % aqua_adm.ESR)

    for data in data.find("#GEN_RESULTS_HD .set"):
        data = pq(data)

        duration_value = value_by_select(data, ".EXP_DURATION_VALUE")
        eff_conc = value_by_select(data, ".LOQUALIFIER")

        datum = find_or_create(
            ECHA_ECOTOX_TOX_DATA,
            TOX_ID=aqua_adm,
            ORGANISM=value_by_select(data, ".ORGANISM"),
            EXP_DURATION_VALUE=duration_value,
            ENDPOINT=value_by_select(data, ".ENDPOINT"),
            EFF_CONC=eff_conc,
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
            value = class_ends(data, "_DNMEL_VALUE").find(".value").html() or ""
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
                                           SENS_ENDP=sens_endp,
                                           ROUTE=route)

@db_session
def toxicokinetics(substance, path):
    import toxicokinetics as tox

    tox.basic(substance, path)
    tox.dermal(substance, path)
    tox.acute(substance, path)
    tox.irritation(substance, path)
    tox.sensitisation(substance, path)
    tox.repeated_dose(substance, path)
    tox.genetic(substance, path)

@db_session
def physical(substance, path):
    import physical as phys

    phys.parse(substance, path)

@db_session
def parse(path):
    path = unpack(path)
    dossier_id = os.path.split(path)[1]

    substance = find_or_create(Substance, DOSSIER_ID=dossier_id)

    logging.info("Ecotoxicity for %s" % dossier_id)
    ecotoxicological(substance, path)

    logging.info("Aquatic toxicity for %s" % dossier_id)
    aquatic(substance, path)

    logging.info("Terrestrial toxicity for %s" % dossier_id)
    terrestrial(substance, path)

    logging.info("Sediment toxicity for %s" % dossier_id)
    sediment(substance, path)

    logging.info("Biodegradation for %s" % dossier_id)
    biodegrad(substance, path)

    logging.info("Bioaccumulation for %s" % dossier_id)
    bioacc(substance, path)

    logging.info("Dnels for %s" % dossier_id)
    dnel(substance, path)

    logging.info("Toxicokinetics for %s" % dossier_id)
    toxicokinetics(substance, path)

    logging.info("Physical properties for %s" % dossier_id)
    physical(substance, path)

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

    print "Done."
