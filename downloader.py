
import urlparse, os, requests
from pyquery import PyQuery as pq
from slugify import slugify
from multiprocessing import Pool
from datetime import datetime

def process(dossier):
    print "Processing %s" % dossier
    start = datetime.now()
    path = os.path.normpath(os.path.join(os.getcwd(),
                                         "data", dossier))
    if not os.path.exists(path):
        os.mkdir(path)

    get(url(dossier), os.path.join(path, "main.html"))

    print "Finding sublinks"
    links = [(link, os.path.join(path, "%s.html" % name))
             for name, link in
             sublinks(os.path.join(path, "main.html"), url(dossier))
             if "toxicological" in name]

    L = len(links)

    links = enumerate(((L, url, path) for url, path in links))

    pool = Pool(10)
    pool.map(_get, links)

    end = datetime.now()

    print "Finished %s in %s" % (dossier, end-start)

def _get(tuple):
    N, tuple = tuple
    L, url, path = tuple

    print "Sublink %d/%d" % (N, L)
    return get(url, path)

def get(url, path):
    if not os.path.exists(path):
        print "Fetching %s" % url
        html = fetch(url)

        print "Storing %s" % path
        store(path, html)

def store(path, text):
    f = open(path, "w")
    f.write(text)
    f.close()

def fetch(url):
    r = requests.get(url)
    return r.text.encode('utf-8')

def url(dossier):
    dossier = dossier.strip()
    return urlparse.urlunparse(("http",
                                "apps.echa.europa.eu",
                                os.path.join("registered/data/dossiers",
                                             dossier,
                                             "%s_%s.html" % (dossier, dossier)),
                                "", "", ""))

def sublinks(file, base_url):
    d = pq(filename=file)
    d.make_links_absolute(base_url=base_url)

    return ((name(pq(a)), pq(a).attr("href")) for a in d("#toc")("a"))

def name(link):
    name = slugify(link.text())

    parent = link.parent()
    while parent[0].tag != "div":
        if parent[0].tag == "ul" and parent.siblings("p").length > 0:
            name = "%s__%s" % (slugify(parent.siblings("p").text()), name)

        parent = parent.parent()

    return name

if __name__ == '__main__':
    for line in open("dossiers.txt"):
        process(line.strip())
