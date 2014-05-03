
import urlparse, os, requests

def fetch(url):
    r = requests.get(url)
    return r.text


def url(dossier):
    dossier = dossier.strip()
    return urlparse.urlunparse(("http",
                                "apps.echa.europa.eu",
                                os.path.join("registered/data/dossiers",
                                             dossier,
                                             "%s_%s.html" % (dossier, dossier)),
                                "", "", ""))

if __name__ == '__main__':
    for line in open("dossiers.txt"):
        text = fetch(url(line))
        print len(text)
