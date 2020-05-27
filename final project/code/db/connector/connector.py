import sqlalchemy
from sqlalchemy.orm import sessionmaker

from ..models.models import Base, User

import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


class MySQLConnector:

    def __init__(self, hostname, port, username, password, db=None):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.db = db

    def connect_master(self):
        self.connection = self.connect()

        self.session = sessionmaker(
            bind=self.connection.engine,
            autocommit=True
        )()

        Base.metadata.create_all(self.connection.engine)

    def connect_slave(self):
        self.connection = self.get_connection(db=self.db)

        self.session = sessionmaker(
            bind=self.connection.engine,
            autocommit=True
        )()

        Base.metadata.create_all(self.connection.engine)

    def get_connection(self, db=''):
        engine = sqlalchemy.create_engine(
            'mysql+pymysql://{user}:{password}@{host}:{port}/{db}'.format(
                user=self.username,
                password=self.password,
                host=self.hostname,
                port=self.port,
                db=db
            ),
            encoding='utf8',
            pool_pre_ping=True,
            echo=True
        )

        return engine.connect()

    def connect(self):
        if self.db is None:
            self.db = 'users'

        connection = self.get_connection()
        connection.execute(f'DROP DATABASE IF EXISTS `{self.db}`')
        connection.execute(f'CREATE DATABASE `{self.db}`')
        connection.close()

        return self.get_connection(db=self.db)

    def sql(self, query):
        return self.connection.execute(query)

    def add_user(self, user):
        self.session.add(user)
        self.session.flush()

    def delete_user(self, username):
        self.session.query(User).filter_by(username=username).delete(synchronize_session='fetch')
        self.session.flush()

    def get_user(self, username):
        self.session.flush()
        return self.session.query(User).filter_by(username=username).first()
