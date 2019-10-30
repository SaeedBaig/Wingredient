import argparse
import logging
import pathlib
from typing import Optional

import yaml

log = logging.getLogger(__name__)

parser = argparse.ArgumentParser(
    prog="wingredient",
)
parser.add_argument(
    "--config-filepath", "-c",
    type=pathlib.Path,
    metavar="CONFIG_FILEPATH",
    required=False,
    dest="config_fpath",
    default=pathlib.Path("wingredient.yml")
)


# The following aren't really classes, they're just being used as objects to categorise our
# configuration options.

class server:
    host: Optional[str] = None
    port: Optional[int] = None


class database:
    host: Optional[str] = None
    port: Optional[int] = None
    user: Optional[str] = None
    password: Optional[str] = None
    dbname: Optional[str] = None


def init_config() -> int:
    cli_options = parser.parse_args()

    if not cli_options.config_fpath.is_file():
        log.warning("Config file '%s' not found, using default options", cli_options.config_fpath)
        return 0

    with cli_options.config_fpath.open() as f:
        try:
            config_data = yaml.safe_load(f)
        except yaml.YAMLError:
            log.exception("Failed to parse config file! Exiting...")
            return 1

        # Server options
        if "server" in config_data and config_data["server"]:
            server.host = config_data["server"].get("host")
            server.port = config_data["server"].get("port")
            if server.port is not None:
                server.port = int(server.port)

        # Database options
        if "database" in config_data and config_data["database"]:
            database.host = config_data["database"].get("host")
            database.port = config_data["database"].get("port")
            if database.port is not None:
                database.port = int(database.port)
            database.user = config_data["database"].get("user")
            database.password = config_data["database"].get("password")
            database.dbname = config_data["database"].get("dbname")
