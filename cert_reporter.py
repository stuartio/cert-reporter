import argparse
import csv
import logging
from akamaithon.property import AkamaiProperty
from akamaithon.cps import AkamaiCPS
from fnmatch import fnmatch


# Set options
usage = "usage: python cert_reporter.py --output-file report.csv [--log-level WARNING] [--edgerc ~/.edgerc] [--section default] [--accountSwitchKey <ask>] [--loglevel INFO]"
parser = argparse.ArgumentParser(usage=usage)
parser.add_argument(
    "-o",
    "--output-file",
    action="store",
    dest="output_file",
    required=False,
    default="results.csv",
    help="Output file for the report",
)
parser.add_argument(
    "-l",
    "--log-level",
    action="store",
    dest="log_level",
    type=str.upper,
    choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    default="INFO",
    help="Logging level. Defaults to INFO",
)
parser.add_argument("-e", "--edgerc", action="store", dest="edgerc", help='EdgeRC file. Defaults to "~/.edgerc"')
parser.add_argument("-s", "--section", action="store", dest="section", help='EdgeRC Section. Defaults to "default"')
parser.add_argument(
    "-a",
    "--account-switch-key",
    action="store",
    dest="account_switch_key",
    help="Account switch key. Only used by Akamai internal staff",
)

args = parser.parse_args()

# Set up logging
logging.basicConfig(
    level=args.log_level,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("cert_reporter")

# Set up clients
property_client = AkamaiProperty(args.edgerc, args.section, args.account_switch_key)
cps_client = AkamaiCPS(args.edgerc, args.section, args.account_switch_key)

enrollments = cps_client.list_enrollments()
logger.debug("Retrieved %d enrollments", len(enrollments))

# Filter for existing slot
enrollments = [enrollment for enrollment in enrollments if len(enrollment["productionSlots"]) > 0]

stls_enrollments = [enrollment for enrollment in enrollments if enrollment["networkConfiguration"]["secureNetwork"] == "standard-tls"]
etls_enrollments = [enrollment for enrollment in enrollments if enrollment["networkConfiguration"]["secureNetwork"] == "enhanced-tls"]

stls_wildcard_enrollments = [enrollment for enrollment in stls_enrollments if "*" in enrollment["csr"]["cn"] or any("*" in san for san in enrollment["csr"]["sans"])]
logger.debug("Identified %d STLS wildcard enrollments", len(stls_wildcard_enrollments))

etls_wildcard_enrollments = [enrollment for enrollment in etls_enrollments if "*" in enrollment["csr"]["cn"] or any("*" in san for san in enrollment["csr"]["sans"])]
logger.debug("Identified %d ETLS wildcard enrollments", len(etls_wildcard_enrollments))

hostnames = property_client.list_account_hostnames(network="PRODUCTION")
logger.debug("Retrieved %d account hostnames", len(hostnames))

parsed_hostnames = [
    {
        "hostname": item["cnameFrom"],
        "enhanced_tls": "edgekey.net" in (item.get("productionCnameTo") or ""),
    }
    for item in hostnames
]
sorted_hostnames = sorted(parsed_hostnames, key=lambda parsed_hostname: parsed_hostname["hostname"])

results = []
for parsed_hostname in sorted_hostnames:
    hostname = parsed_hostname["hostname"]
    matched_enrollments = []

    if parsed_hostname["enhanced_tls"]:
        exact_matches = [enrollment for enrollment in etls_enrollments if enrollment["csr"]["cn"] == hostname or hostname in enrollment["csr"]["sans"]]

        if exact_matches:
            matched_enrollments.extend(exact_matches)

        for wildcard_enrollment in etls_wildcard_enrollments:
            if fnmatch(hostname, wildcard_enrollment["csr"]["cn"]) or any(fnmatch(hostname, san) for san in wildcard_enrollment["csr"]["sans"]):
                matched_enrollments.append(wildcard_enrollment)

    else:
        exact_matches = [enrollment for enrollment in stls_enrollments if enrollment["csr"]["cn"] == hostname or hostname in enrollment["csr"]["sans"]]

        if exact_matches:
            matched_enrollments.extend(exact_matches)

        for wildcard_enrollment in stls_wildcard_enrollments:
            if fnmatch(hostname, wildcard_enrollment["csr"]["cn"]) or any(fnmatch(hostname, san) for san in wildcard_enrollment["csr"]["sans"]):
                matched_enrollments.append(wildcard_enrollment)

    for matched_enrollment in matched_enrollments:
        result = {
            "hostname": hostname,
            "commonName": matched_enrollment["csr"]["cn"],
            "enrollmentId": matched_enrollment["id"],
            "slotNumber": matched_enrollment["productionSlots"][0],
            "network": matched_enrollment["networkConfiguration"]["secureNetwork"],
            "sniOnly": matched_enrollment["networkConfiguration"]["sniOnly"],
            "cipherSuite": matched_enrollment["networkConfiguration"]["mustHaveCiphers"],
            "disallowedTlsVersions": ",".join(matched_enrollment["networkConfiguration"]["disallowedTlsVersions"]),
        }
        results.append(result)

# Write to csv
if len(results) > 0:
    with open(args.output_file, "w", encoding="utf8", newline="") as output_file:
        fc = csv.DictWriter(
            output_file,
            fieldnames=results[0].keys(),
        )
        fc.writeheader()
        fc.writerows(results)
    logger.info("Wrote %d lines to file '%s'", len(results), args.output_file)
else:
    logger.warning("No hostnames retrieved.")