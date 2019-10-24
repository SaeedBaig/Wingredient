from pathlib import Path
from typing import cast

import psycopg2.pool

from . import config

SCHEMA_SCRIPT = Path(__file__).parent / "wingredient-schema.sql"
DATA_SCRIPT = Path(__file__).parent / "wingredient-insert.sql"

pool = cast(psycopg2.pool.ThreadedConnectionPool, None)


def init_db() -> int:
    config.init_config()
    init_pool()

    with pool.getconn() as conn:
        with conn.cursor() as cu:
            with SCHEMA_SCRIPT.open() as f:
                cu.execute(f.read())
            with DATA_SCRIPT.open() as f:
                cu.execute(f.read())

    print("Database initialized!")

    return 0


def init_pool():
    global pool

    pool = psycopg2.pool.ThreadedConnectionPool(
        minconn=1,
        maxconn=10,
        host=config.database.host,
        port=config.database.port,
        user=config.database.user,
        password=config.database.password,
        dbname=config.database.dbname,
    )


def close_pool():
    if pool is not None:
        pool.closeall()
