
import os, re, codecs, glob, logging
from pyquery import PyQuery as pq
from slugify import slugify

from db import *

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
    d = data.find("%s .value" % selector)
    if len(d.find("span")) > 1 and any(fragment in selector for fragment in
                                       ["QUALIFIER", ".FORM", ".ODOUR", ".TEMP_VALUE",
                                        "EXPLOS_LIMIT", ".PERCENTILE", "_VALUE"]):
        return d.html() or ""
    else:
        return d.text()

def html_value_by_select(data, selector):
    return data.find("%s .value" % selector).html() or ""

def get_esr(d):
    return d("#page_header h2").text()

def fieldify(kwargs):
    return dict((k.upper(), v) for k, v in kwargs.iteritems())

def magic_fields(field):
    if len(field) < 2:
        k = field[0]
        field = (k, ".%s" % k.upper())
    return field

def save_data(data, table, known_data, fields):
    models = []
    known_data = [known_data] if type(known_data) == tuple else known_data

    fields = [(f[0], ".%s" % f[0].upper()) if len(f) < 2 else f
              for f in fields]

    for d in data:
        d = pq(d)

        kwargs = [(field, value_by_select(d, selector))
                  for field, selector in fields]

        if all(v.strip() <= 0
               for k, v in kwargs + known_data
               if type(v) == str):
            continue

        kwargs = dict(kwargs + known_data)

        models.append(find_or_create(table, **fieldify(kwargs)))

    return models

def save_refs(data, table, parent):
    return save_data(data.find(".set.REFERENCE"),
                     table, parent,
                     [("reference_type", ".REFERENCE_TYPE"),
                      ("reference_author", ".REFERENCE_AUTHOR"),
                      ("reference_year", ".REFERENCE_YEAR"),
                      ("reference_title", ".REFERENCE_TITLE"),
                      ("reference_source", ".REFERENCE_SOURCE")])

def save_guidelines(data, table, parent):
    return save_data(data.find(".set.GUIDELINE"),
                     table, parent,
                     [("guideline", ".GUIDELINE"),
                      ("qualifier", ".QUALIFIER"),
                      ("deviation", ".DEVIATION")])

def parse_files(path, path_parts, step_func):
    files = build_path(path, path_parts)

    for file in glob.glob(files.replace("sss", "*")):
        d = open_file(file)
        data = d("#inner")

        logging.info("Esr, %s" % get_esr(d))
        step_func(d, data, file)

def make_fields(custom, default):
    return custom + [(f,) for f in default]
