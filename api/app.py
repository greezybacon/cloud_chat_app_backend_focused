import os

from chat_app_api.app import app
from chat_app_api.database import init_db

if __name__ == '__main__':
    DB_USER = os.environ['POSTGRES_USER']
    DB_PASSWD = os.environ['POSTGRES_PASSWORD']
    DB_HOST = os.environ['POSTGRES_host']
    init_db(f'postgres://{DB_USER}:{DB_PASSWD}@{DB_HOST}/chat_app')
    print("Database is READY")
    app.run(host='0.0.0.0', port=5000, debug=False)
    print("EXITING")
