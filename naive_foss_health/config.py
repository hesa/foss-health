import os


NFHC_VERSION = 0.1
NFHC_SHORT_NAME = "nfhc"
NFHC_LONG_NAME = "Naive FOSS Health Checker"
NFHC_DESCRIPTION = "Tries to quickly check the health of a FOSS project"

SCRIPT_DIR = os.path.realpath(os.path.dirname(os.path.realpath(__file__)))

NFHC_CONFIG = os.path.join((os.path.join(SCRIPT_DIR, "var")), "nfhc.json")


