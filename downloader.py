
import urlparse, os, requests, tarfile, shutil, signal, time

from pyquery import PyQuery as pq
from slugify import slugify
from multiprocessing import Pool
from datetime import datetime

MAX_TIMEOUT = 1024

class ScrapingError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def process(dossier):
    print "Processing %s" % dossier
    start = datetime.now()
    base_path = os.path.normpath(os.path.join(os.getcwd(), "data"))

    path = os.path.join(base_path, dossier)

    if os.path.exists("%s.tar.gz" % path):
        print "Already have %s" % dossier
        return None

    if not os.path.exists(path):
        os.mkdir(path)

    get(url(dossier), os.path.join(path, "main.html"))

    print "Finding sublinks"
    links = [(link, os.path.join(path, "%s.html" % name))
             for name, link in
             sublinks(os.path.join(path, "main.html"), url(dossier))
             if any(candidate in name.lower() for candidate in
                    ["toxicological", "physical", "environmental"])]

    L = len(links)

    if L > 0:
        links = enumerate(((L, url, path) for url, path in links))
        pool = Pool(10, init_worker)

        try:
            pool.map(_get, links)
        except KeyboardInterrupt:
            pool.terminate()
            pool.join()
        else:
            pool.close()
            pool.join();

        compress(base_path, dossier)

    cleanup(path)
    end = datetime.now()

    print "Finished %s in %s" % (dossier, end-start)

def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def cleanup(path):
    shutil.rmtree(path)

def compress(base_path, dossier):
    target = os.path.join(base_path, "%s.tar.gz" % dossier)
    source = os.path.join(base_path, dossier)

    with tarfile.open(target, "w:gz") as tar:
        tar.add(source, arcname=os.path.basename(source))

def _get(tuple):
    N, tuple = tuple
    L, url, path = tuple

    print "Sublink %d/%d" % (N, L)
    return get(url, path)

def get(url, path, timeout=2):
    if not os.path.exists(path):
        print "Fetching %s" % url
        try:
            html = fetch(url)
        except requests.exceptions.RequestException:
            print "Sleeping for %d" % timeout

            if timeout >= MAX_TIMEOUT:
                raise ScrapingError("Failed to fetch %s" % url)

            time.sleep(timeout)
            get(url, path, timeout*3)
        else:
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
    #process("DISS-9daa7594-c409-0ed0-e044-00144f67d249")
    #process("DISS-9d998764-70a1-6fbe-e044-00144f67d249")
    for line in open("dossiers.txt"):
        process(line.strip())

    print "Done."
