import pymysql
from flask import current_app


def connect_to_sql():
    connection = pymysql.connect(host=current_app.config['DATABASE_HOST'], user=current_app.config['DATABASE_USER'],
                                 password=current_app.config['DATABASE_PASSWORD'],
                                 database=current_app.config['DATABASE_NAME'], port=current_app.config['DATABASE_PORT'],
                                 charset='utf8')
    return connection
