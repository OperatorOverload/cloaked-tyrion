
import os, tarfile, time
from pony.orm import *
from pyquery import PyQuery as pq

db = Database('sqlite', 'db.sqlite', create_db=True)

@db_session
def parse(path):
    print path

if __name__ == "__main__":
    for file in os.listdir(os.path.join(os.getcwd(), "data")):
        if file.startswith("DISS"):
            parse(os.path.join(os.getcwd(), "data", file))
