#!/usr/bin/env python3

# example.py

# Use query.py to drive the Bulk Download tool from the
# Bioplatforms Australia Data Portal to download data

from query import assemble_query, download_query
from download import make_logger

logger = make_logger(__name__)
logger.info("example.py")

results = []

# Directories for output
directory1 = "demo-images"
directory2 = "demo-images-mount-bold"

# assemble queries

# assemble_query() takes two araguments, a query, and a output directory
# returns tuple - (path, query_hash_prefix)

# assemble_query("type:gap-illumina-shortread sample_id:102.100.100/79638","gapdata")

# put these two queries in the same directory
results.append(assemble_query("sequence_data_type:image woomera", directory1))
results.append(assemble_query("sequence_data_type:image camp mountain", directory1))

# different directory for these results
results.append(assemble_query("sequence_data_type:image mount bold", directory2))

# download the results

for r in results:
    download_query(r)
