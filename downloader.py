
import urlparse, os, requests
from pyquery import PyQuery as pq

def process(dossier):
    #url = url(dossier)
    path = os.path.normpath(os.path.join(os.getcwd(),
                                         "data", dossier))
    if not os.path.exists(path):
        os.mkdir(path)

    print "Fetching %s" % dossier
    html = fetch(url(dossier))

    print "Storing %s" % dossier
    if not os.path.exists(os.path.join(path, "main.html")):
        store(os.path.join(path, "main.html"), html)

    print "Finding sublinks"
    print sublinks(os.path.join(path, "main.html"))

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

def sublinks(file):
    d = pq(filename=file)
    print d("#toc")

if __name__ == '__main__':
    for line in open("dossiers.txt"):
        process(line.strip())
        break
