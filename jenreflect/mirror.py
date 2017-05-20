import argparse
import base64
import hashlib
import json
import logging
import os
import sys


import requests


logger = logging.getLogger(__name__)


def verify_file(filename, checksum):
    with open(filename, "rb") as f:
        content = f.read()
    m = hashlib.sha1()
    m.update(content)
    return m.digest()==checksum


def download_and_verify(url, filename, checksum):
    try:
        file_previously_downloaded = verify_file(filename, checksum)
    except:
        file_previously_downloaded = False

    if file_previously_downloaded:
        logger.info("File {} previously downloaded and SHA1 matches, skipping download.".format(filename))
        return

    logger.info("Downloading: {}".format(url))
    content = requests.get(url).content
    with open(filename, "wb") as f:
        f.write(content)

    try:
        valid_file = verify_file(filename, checksum)
    except:
        valid_file = False

    if not valid_file:
        logger.error("SHA1 verification FAILED.")
        raise Exception("SHA1 verification FAILED.")

    logger.debug("SHA1 verification PASSED.")


def main(arguments=None):
    if arguments is None:
        arguments = sys.argv[1:]

    parser = argparse.ArgumentParser(
            description="Tool for downloading Jenkins update-center JSON, war, and plugins",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
            "-v", "--verbose",
            default=False,
            action="store_true",
            help="Show debug log messages")
    parser.add_argument(
            "-q", "--quiet",
            default=False,
            action="store_true",
            help="Only show warning/error log messages")
    parser.add_argument(
            "--url",
            default="https://updates.jenkins-ci.org/stable/update-center.json",
            help="URL for update-center.json")
    parser.add_argument(
            "--path",
            default="jenkins-mirror",
            help="Local path to the mirror directory")
    args = parser.parse_args(arguments)

    logging.basicConfig(level=logging.WARN)
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    elif args.quiet:
        logger.setLevel(logging.WARN)
    else:
        logger.setLevel(logging.INFO)

    os.makedirs(args.path, exist_ok=True)

    logger.info("Downloading: {}".format(args.url))
    update_center_json = requests.get(args.url).text
    with open(os.path.join(args.path, "update-center.json"), "w") as f:
        f.write(update_center_json)

    update_center_info = json.loads(update_center_json.splitlines()[1])
    jenkins_version = update_center_info["core"]["version"]
    jenkins_war_url = update_center_info["core"]["url"]
    logger.debug("Jenkins version={} url={}".format(jenkins_version, jenkins_war_url))
    download_and_verify(
            jenkins_war_url,
            os.path.join(args.path, "jenkins-{}.war".format(jenkins_version)),
            base64.b64decode(update_center_info["core"]["sha1"]))

    plugin_count = len(update_center_info["plugins"])
    logger.debug("Plugin count={}".format(plugin_count))
    for i, plugin in enumerate(update_center_info["plugins"]):
        plugin_info = update_center_info["plugins"][plugin]
        logger.info("Plugin {} of {}: {}".format(i, plugin_count, plugin))
        outfile = os.path.join(
                args.path,
                plugin,
                plugin_info["version"],
                "{}.hpi".format(plugin))
        os.makedirs(os.path.dirname(outfile), exist_ok=True)
        download_and_verify(plugin_info["url"], outfile, base64.b64decode(plugin_info["sha1"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
