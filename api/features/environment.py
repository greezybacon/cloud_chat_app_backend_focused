from behave import use_fixture
import os, os.path
import subprocess

from chat_app_api.app import app
from chat_app_api.database import init_db, db_shut

from_here = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.abspath(os.path.join(from_here, '..', '..', 'postgres'))

def rest_api_client(context):
    app.testing = True
    context.api_client = app.test_client()
    with app.app_context():
        pg_tmp = subprocess.run(
            f"{db_path}/util/pg_tmp.sh -w 0 -d {db_path}/data start",
            stdout=subprocess.PIPE, shell=True, text=True
        )
        dsn = pg_tmp.stdout.strip()
        init_db(dsn)
        app.db.commit()

    yield context.api_client

    # Close database and cleanup
    with app.app_context():
        db_shut()

    subprocess.run(
        f"{db_path}/util/pg_tmp.sh stop -d {db_path}/data",
        shell=True
    )

def before_feature(context, feature):
    use_fixture(rest_api_client, context)

def before_scenario(context, scenario):
    with app.app_context():
        app.autocommit = False

def after_scenario(context, scenario):
    with app.app_context():
        app.db.rollback()