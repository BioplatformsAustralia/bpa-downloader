#!/usr/bin/env python3

# example.py

# Use query.py to drive the Bulk Download tool from the
# Bioplatforms Australia Data Portal to download data

from query import assemble_query, download_query
from download import make_logger

logger = make_logger(__name__)
logger.info("example.py")

# Directory for output
directory = "demo"

# assemble queries

# returns tuple - (path, query_hash_prefix)
query = assemble_query("sequence_data_type:site-image", directory)
query2 = assemble_query("sequence_data_type:ont-minion", directory)

#
results = [query2, query]

for r in results:
    download_query(r)
