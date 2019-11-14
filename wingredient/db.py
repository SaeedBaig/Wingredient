from contextlib import contextmanager
from pathlib import Path
from typing import cast
from .dbdata import DBWriterFiles
import psycopg2.pool

from . import config

DBDATA_DIR = Path(__file__).parent / "dbdata"
SCHEMA_SCRIPT = DBDATA_DIR / "wingredient-schema.sql"
#DATA_SCRIPT = DBDATA_DIR / "wingredient-insert.sql"


SQLCOPY1 = DBDATA_DIR / "recipe.csv"
SQLCOPY2 = DBDATA_DIR / "ingredient.csv"
SQLCOPY3 = DBDATA_DIR / "recipeToIngredient.csv"
SQLCOPY4 = DBDATA_DIR / "equipment.csv"
SQLCOPY5 = DBDATA_DIR / "recipeToEquipment.csv"

pool = cast(psycopg2.pool.ThreadedConnectionPool, None)


def init_db() -> int:
    config.init_config()
    init_pool()

    with pool.getconn() as conn:
        with conn.cursor() as cu:
            with SCHEMA_SCRIPT.open() as f:
                cu.execute(f.read())
            with open(SQLCOPY1, 'r', encoding='utf-8') as f:
                cu.copy_expert("COPY recipe FROM stdin DELIMITER ',' CSV HEADER", f)
            with open(SQLCOPY2, 'r', encoding='utf-8') as f:
                cu.copy_expert("COPY ingredient FROM stdin DELIMITER ',' CSV HEADER", f)
            with open(SQLCOPY3, 'r', encoding='utf-8') as f:
                cu.copy_expert("COPY recipeToIngredient FROM stdin DELIMITER ',' CSV HEADER", f)
            with open(SQLCOPY4, 'r', encoding='utf-8') as f:
                cu.copy_expert("COPY equipment FROM stdin DELIMITER ',' CSV HEADER", f)
            with open(SQLCOPY5, 'r', encoding='utf-8') as f:
                cu.copy_expert("COPY recipeToEquipment FROM stdin DELIMITER ',' CSV HEADER", f)
            #with DATA_SCRIPT.open() as f:
            #    cu.execute(f.read())

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


@contextmanager
def getconn():
    conn = pool.getconn()
    try:
        yield conn
    finally:
        pool.putconn(conn)
