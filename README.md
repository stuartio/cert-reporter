# Akamai Certificate Reporter

This utility will list all hostnames in your account and try to match them with CPS enrollments (if any).

## Installation

This script requires Python 3.10 or later. Install the prerequisite pips with the following command:

```shell
python -m pip install -r requirements.txt
```

## Usage 

```shell
usage: usage: python cert_reporter.py --output-file report.csv [--log-level WARNING] [--edgerc ~/.edgerc] [--section default] [--accountSwitchKey <ask>] [--loglevel INFO]

options:
  -h, --help            show this help message and exit
  -o, --output-file OUTPUT_FILE
                        Output file for the report
  -l, --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Logging level. Defaults to INFO
  -e, --edgerc EDGERC   EdgeRC file. Defaults to "~/.edgerc"
  -s, --section SECTION
                        EdgeRC Section. Defaults to "default"
  -a, --account-switch-key ACCOUNT_SWITCH_KEY
                        Account switch key. Only used by Akamai internal staff
```