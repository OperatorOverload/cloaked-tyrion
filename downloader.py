
import urlparse, os, requests
from pyquery import PyQuery as pq

def process(dossier):
    print "Processing %s" % dossier
    print url(dossier)
    #url = url(dossier)
    path = os.path.normpath(os.path.join(os.getcwd(),
                                         "data", dossier))
    if not os.path.exists(path):
        os.mkdir(path)

    if not os.path.exists(os.path.join(path, "main.html")):
        print "Fetching"
        html = fetch(url(dossier))

        print "Storing"
        store(os.path.join(path, "main.html"), html)

    print "Finding sublinks"
    print sublinks(os.path.join(path, "main.html"), url)

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
    name(pq(d("#toc")("a")[2]))
    #print [(name(pq(a)), pq(a).attr("href")) for a in d("#toc")("a")]

def name(link):
    name = link.text()

    parent = link.parent()
    while parent[0].tag != "div":
        if parent[0].tag == "ul" and parent.siblings("p").length > 0:
            name = "%s-%s" % (parent.siblings("p").text(), name)

        parent = parent.parent()

    return name


if __name__ == '__main__':
    for line in open("dossiers.txt"):
        process(line.strip())
        break
