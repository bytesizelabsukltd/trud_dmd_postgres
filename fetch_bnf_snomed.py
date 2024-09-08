import glob
import os
import re
import zipfile
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse

import requests
from bs4 import BeautifulSoup

# Replace Django's settings with a constant
PIPELINE_DATA_BASEDIR = "../PIPELINE_DATA_BASEDIR"

def mkdir_p(path):
    os.makedirs(path, exist_ok=True)

def main():
    page_url = "https://www.nhsbsa.nhs.uk/prescription-data/understanding-our-data/bnf-snomed-mapping"
    filename_re = re.compile(
        r"^BNF Snomed Mapping data (?P<date>20\d{6})\.zip$", re.IGNORECASE
    )

    rsp = requests.get(page_url)
    rsp.raise_for_status()
    doc = BeautifulSoup(rsp.text, "html.parser")

    matches = []
    for a_tag in doc.find_all("a", href=True):
        url = urljoin(page_url, a_tag["href"])
        filename = Path(unquote(urlparse(url).path)).name
        match = filename_re.match(filename)
        if match:
            matches.append((match.group("date"), url, filename))

    if not matches:
        raise RuntimeError(f"Found no URLs matching {filename_re} at {page_url}")

    # Sort by release date and get the latest
    matches.sort()
    datestamp, url, filename = matches[-1]

    release_date = f"{datestamp[:4]}_{datestamp[4:6]}_{datestamp[6:]}"
    dir_path = os.path.join(PIPELINE_DATA_BASEDIR, "bnf_snomed_mapping", release_date)

    # Check if directory with the same date already exists
    if os.path.exists(dir_path) and glob.glob(os.path.join(dir_path, "*.xlsx")):
        print(f"Directory {dir_path} already exists and contains .xlsx files. Skipping download.")
        return

    zip_path = os.path.join(dir_path, filename)

    mkdir_p(dir_path)

    rsp = requests.get(url, stream=True)
    rsp.raise_for_status()

    with open(zip_path, "wb") as f:
        for block in rsp.iter_content(32 * 1024):
            f.write(block)

    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(dir_path)

    print(f"Files downloaded and extracted to: {dir_path}")

if __name__ == "__main__":
    main()