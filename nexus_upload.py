#!/usr/bin/env python3
"""This scripts uploads files to Nexus3 repository using POST method"""

import argparse
import glob
import logging
import os
import sys
import requests
import requests.auth


class CustomFormatter(logging.Formatter):
    """Formatter for logging"""

    grey = "\x1b[38;20m"
    green = "\x1b[32;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    log_format = "%(asctime)s - %(levelname)s - %(message)s"

    FORMATS = {
        logging.DEBUG: grey + log_format + reset,
        logging.INFO: green + log_format + reset,
        logging.WARNING: yellow + log_format + reset,
        logging.ERROR: red + log_format + reset,
        logging.CRITICAL: bold_red + log_format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def check_env():
    """Checks if required env variables are set"""
    if os.environ.get('NEXUS_HOST_URL') is None:
        raise ValueError('NEXUS_HOST_URL var not set')
    if os.environ.get('NEXUS_USER') is None:
        raise ValueError('NEXUS_USER var not set')
    if os.environ.get('NEXUS_TOKEN') is None:
        raise ValueError('NEXUS_TOKEN env not set')


def search_files(pattern: str):
    """Search files using pattern"""
    files = glob.glob(pattern)
    return files


def upload_apt(filename: str, repo: str, timeout: int):
    """Uploads deb package to Nexus3 APT repository"""
    url = os.environ.get('NEXUS_HOST_URL') + '/service/rest/v1/components'
    params = {'repository': repo}
    with open(filename, 'rb') as file:
        files = {
            'apt.asset': (filename, file)
        }
        auth = requests.auth.HTTPBasicAuth(
            username=os.environ.get('NEXUS_USER'),
            password=os.environ.get('NEXUS_TOKEN'))
        response = requests.post(
            url=url, params=params, files=files,
            auth=auth, timeout=timeout)
        response.raise_for_status()


def upload_raw(filename: str, repo: str, timeout: int):
    """Uploads file to Nexus3 RAW repository"""
    url = os.environ.get('NEXUS_HOST_URL') + '/service/rest/v1/components'
    params = {'repository': repo}
    with open(filename, 'rb') as file:
        files = {
            'raw.asset1': (filename, file)
        }
        data = {
            'raw.directory': '/',
            'raw.asset1.filename': filename
        }
        auth = requests.auth.HTTPBasicAuth(
            username=os.environ.get('NEXUS_USER'),
            password=os.environ.get('NEXUS_TOKEN'))
        response = requests.post(
            url=url, params=params, files=files,
            data=data, auth=auth, timeout=timeout)
        response.raise_for_status()


def main():
    """Main function"""

    check_env()

    log = logging.getLogger('nexus_upload')
    log.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(CustomFormatter())
    log.addHandler(stream_handler)
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', required=True,
                        help='Comma separated list of repositories to upload')
    parser.add_argument('-p', required=True,
                        help='File name pattern to search')
    parser.add_argument('-d', required=False,
                        help='Subdirectory in WORKSPACE for file search')
    parser.add_argument('-t', required=False,
                        help='Timeout in seconds for single file upload',
                        type=int, default=100)
    args = parser.parse_args()
    if len(args.d) > 0:
        os.chdir(args.d)
    log.warning("Working directory: %s", os.getcwd())
    upload_files = search_files(args.p)
    if len(upload_files) > 0:
        log.warning("Files to upload: %s", upload_files)
        for repo in args.r.split(','):
            log.warning("Uploading files to %s repository", repo)
            for file in upload_files:
                if args.p.endswith(".deb"):
                    log.info("Uploading APT: %s", file)
                    upload_apt(file, repo, args.t)
                else:
                    log.info("Uploading RAW: %s", file)
                    upload_raw(file, repo, args.t)
                log.info('Done')
    else:
        log.warning("No files found")
    sys.exit(0)


if __name__ == '__main__':
    main()
