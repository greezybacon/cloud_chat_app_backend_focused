from contextlib import contextmanager
import os, os.path
import psycopg2
import subprocess

from .app import app

pwd = os.path.dirname(os.path.abspath(__file__))

def init_db(dsn):
    open_db(dsn)
    setup_db()

def open_db(dsn):
    app.db = psycopg2.connect(dsn=dsn)
    assert app.db

def db_shut():
    app.db.close()

def setup_db():
    with open(os.path.join(pwd, 'setup', 'schema.sql'), 'rt') as schema:
        block = ''
        for line in schema:
            block += line
            if line.strip().endswith(';'):
                if block.strip():
                    try:
                        app.db.cursor().execute(block)
                    except Exception as e:
                        print("Oops: that didn't work:" + repr(e))
                block = ''


@contextmanager
def temp_database():
    from_here = os.path.dirname(os.path.abspath(__file__))
    api_root = os.path.abspath(os.path.join(from_here, '..'))

    pg_tmp = subprocess.run(
        f"{api_root}/util/pg_tmp.sh create",
        stdout=subprocess.PIPE, shell=True, text=True
    )
    data_dir = pg_tmp.stdout.strip()

    pg_tmp = subprocess.run(
        f"{api_root}/util/pg_tmp.sh -w 0 -d {data_dir} start",
        stdout=subprocess.PIPE, shell=True, text=True
    )
    dsn = pg_tmp.stdout.strip()

    yield dsn

    subprocess.run(
        f"{api_root}/util/pg_tmp.sh stop -d {data_dir}",
        shell=True
    )