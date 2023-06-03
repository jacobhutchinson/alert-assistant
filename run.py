# Parses input and runs smart_monitoring on the command line, or on a local webserver
import logging
import argparse
import yaml
from smart_monitoring.main import main

LOG = logging.getLogger(__name__)

def get_parser():
    parser = argparse.ArgumentParser("Start smart_monitoring locally")
    parser.add_argument(
        "--api", action="store_true", help="Start a webserver in place of running on command line"
    )
    parser.add_argument(
        "--api_host", help="Hosting location for API (local only)", default="127.0.0.1"
    )
    parser.add_argument(
        "--api_port", help="Port for API", default="5000"
    )
    return parser

def start_api(args, config):
    LOG.error("API server not yet implemented. Remove --api argument to run in terminal.")
    sys.exit(1)

if __name__ == "__main__":
    args = get_parser().parse_args()
    logging.basicConfig(level=logging.INFO)
    with open('./config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    if args.api:
        start_api()
    else:
        main(args, config)
