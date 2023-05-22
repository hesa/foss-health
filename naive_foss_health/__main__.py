#!/bin/env python3

import argparse
import logging
import json
import re
import sys

from naive_foss_health.repo_factory import RepoScraperFactory
from naive_foss_health.analyzer import RepoAnalyzer
from naive_foss_health.output.output_factory import OutputFormatterFactory

from naive_foss_health.config import NFHC_VERSION
from naive_foss_health.config import NFHC_SHORT_NAME
from naive_foss_health.config import NFHC_LONG_NAME
from naive_foss_health.config import NFHC_DESCRIPTION
from naive_foss_health.config import NFHC_CONFIG

DEFAULT_OUTPUT_FORMAT = "json"

def parse():
    parser = argparse.ArgumentParser(
        prog=f'{NFHC_SHORT_NAME} - {NFHC_LONG_NAME}',
        description=f'{NFHC_DESCRIPTION}',
        epilog='Well, that\'s about it folks')

    parser.add_argument('url')
    
    parser.add_argument('-v', '--verbose',
                        action='store_true')

    
    parser.add_argument('-of', '--output-format',
                        default=DEFAULT_OUTPUT_FORMAT)

    parser.add_argument('-lof', '--list-output-formats',
                        action='store_true')

    parser.add_argument('-c', '--config',
                        default = NFHC_CONFIG)

    args = parser.parse_args()

    return args

def read_config(config):
    with open(config) as fp:
        return json.load(fp)
    

def main():
    
    args = parse()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.list_output_formats:
        print(f'Supported output formats: {OutputFormatterFactory().formats()}')
        sys.exit(0)

    config = read_config(args.config)
    formatter = OutputFormatterFactory().formatter(args.output_format)

    try:
        scraper = RepoScraperFactory.RepoScraper(args.url)
        report = scraper.scan_repo()
        analyzer = RepoAnalyzer(report, config.get("thresholds"))
        analysis = analyzer.check()
        formatted = formatter.format(analysis)
        print(formatted)
    except Exception as e:
        formatted = formatter.format_error(str(e))
        print(formatted)
    


if __name__ == '__main__':
    main()
