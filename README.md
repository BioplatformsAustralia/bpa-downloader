# bpa-downloader

This repository contains a working example of code to download resources
from the Bioplatforms Australia Data Portal given a suitable query.

## Files

The repository contains three Python files

**download.py**
> Used as a module to download the files,
> and then checksum them.  This script is cross platform and is supported
> on Linux / MacOS / Windows hosts. Requires the `requests` module.
> This script is the same as provided by the BPA Bulk Download tool
> on the BPA Data Portal.

**query.py**
> A module that takes akes a provided query, directory path, and a 
> CKAN_API_KEY assembles a download directory in the correct format 
> containing a list of URLs and MD5 sums, such that download.py module
> can be used to obtain the files

**example.py**
> Python 3 script demonstrating the use of the assembly_query and 
> download_query functions in query.py   Use this as your starting
> point for extending and adapting to your needs

## Usage

### Set up your python environment and install python requirements

It is recommended to use a Python virtual environment to run/install
this code

There are minimal dependencies for this code - ckanapi and the requests 
module.

These can be install using

```
pip install -r requirements.txt

```

### API Key

Before running either of these scripts, please set the CKAN_API_KEY
environment variable.

You can find your API Key by browsing to:

https://data.bioplatforms.com/user/YOUR_USERNAME

with YOUR_USERNAME replaced by the username you use onthe BPA Data Portal

The API key has the format:
xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
To set the environment variable in Linux/MacOS/Unix, use:
export CKAN_API_KEY=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

### Modify example.py and run

Adjust and extend the lines containing calls to assemble_query as needed
with your query and the intended output directory

```python
assemble_query("type:gap-illumina-shortread sample_id:102.100.100/79638","gapdata")
```
The script will generate the same list of URLs and MD5 sums on each
run such that it can be run multiple times if your download is interuptted.

## Limitations and future work

- Currently query.py does not download any package or resource metadata

## License

Please consult the individual files in this repository

## Queries

Please email help@bioplatforms.com
