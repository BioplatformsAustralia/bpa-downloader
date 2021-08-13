#!/usr/bin/env python3

# query.py
# Engine to assembly and output queries for the Bulk Download tool 
# from the Bioplatforms Australia Data Portal

# Copyright 2021 Bioplatforms Australia

# License - GNU Affero General Public License v3.0
# https://github.com/BioplatformsAustralia/ckanext-bulk/blob/master/LICENSE.txt

# This script should be cross platform and work on Linux, Windows and MacOS

import ckanapi
import requests
import hashlib
import string
import os
from urllib.parse import urlparse

from download import check_for_api_key, process_downloads, make_logger, file_present

logger = make_logger(__name__)

def make_safe(s):
    return "".join(
        t for t in s if t in string.digits or t in string.ascii_letters or t == "-"
    )


def prefix_from_components(components):
    # note: a hash is generated of the components to avoid long paths
    components = [make_safe(c) for c in components]
    component_hash = hashlib.sha1(("_".join(components)).encode("utf-8")).hexdigest()[
        -8:
    ]
    return "bpa_{}".format(component_hash)


def assemble_query(query, directory):
    directory = directory.rstrip("/")
    # check if directory exists, and is a directory, and writeable
    if os.path.isdir(directory) and os.access(directory, os.W_OK):
        logger.debug("{} looks good...".format(directory))
    elif os.path.exists(directory):
        logger.error("{} is file!".format(directory))
        return None
    else:
        # if not, create it
        logger.info("Creating directory {}".format(directory))
        os.makedirs(directory)

    # create tmp directory underdirector for urls and md5
    os.makedirs("{}/tmp".format(directory), exist_ok=True)

    md5_attribute = "md5"
    api_key = check_for_api_key()
    prefix = prefix_from_components(query)

    remote = ckanapi.RemoteCKAN("https://data.bioplatforms.com", apikey=api_key)
    logger.info("Assembling query: {}".format(query))
    # we increase the number of rows to be returned, and we
    # ask for all packages, including private packages
    result = remote.action.package_search(q=query, rows=50000, include_private=True)
    logger.info("{} matches found.".format(result["count"]))
    logger.info(prefix)
    # iterate through the resulting packages, assemble the manifest one by one
    urls = []
    md5sums = []
    for package in result["results"]:
        for resource in sorted(package["resources"], key=lambda r: r["url"]):
            url = resource["url"]
            urls.append(url)
            if md5_attribute in resource:
                filename = urlparse(url).path.split("/")[-1]
                md5 = resource[md5_attribute]
                md5sums.append((md5, filename))

    urls_fname = "{}/tmp/{}_urls.txt".format(directory, prefix)
    md5sum_fname = "{}/tmp/{}_md5sum.txt".format(directory, prefix)

    logger.info("Writing {}".format(urls_fname))
    with open(urls_fname, "w") as f:
        f.write("\n".join(urls) + "\n")
    logger.info("Writing {}".format(md5sum_fname))
    with open(md5sum_fname, "w") as f:
        f.write("\n".join("%s  %s" % t for t in md5sums) + "\n")

    return (directory, prefix)


def download_query(result_tuple):
    download_path, prefix = result_tuple

    api_key = check_for_api_key()

    # Check for our list of URLs and MD5 values
    url_list = f"{download_path}{os.path.sep}tmp{os.path.sep}{prefix}_urls.txt"
    md5_file = f"{download_path}{os.path.sep}tmp{os.path.sep}{prefix}_md5sum.txt"

    # Check we are being run from a suitable location

    file_present(url_list, "URL list")
    file_present(md5_file, "MD5 file")

    process_downloads(api_key, url_list, md5_file, download_path)


def main():
    logger.info("query.py")
    # assemble_query("sequence_data_type:image","demo_query")
    r = assemble_query("sequence_data_type:image", "demo_query")
    download_query(r)


if __name__ == "__main__":
    # execute only if run as a script
    main()
