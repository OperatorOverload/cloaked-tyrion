
import os, re, codecs
from pyquery import PyQuery as pq
from slugify import slugify


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

def html_value_by_select(data, selector):
    return data.find("%s .value" % selector).html() or ""

def fieldify(kwargs):
    return dict((k.upper(), v) for k, v in kwargs.iteritems())
