from sqlalchemy import Column, Integer, String, SmallInteger, DateTime, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'test_users'
    __table_args__ = (
        UniqueConstraint('email', name='email'),
        UniqueConstraint('username', name='ix_test_users_username'),
        {'mysql_charset': 'utf8'}
    )

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String(16), nullable=True)
    password = Column(String(255), nullable=False)
    email = Column(String(64), nullable=False)
    access = Column(SmallInteger, nullable=True)
    active = Column(SmallInteger, nullable=True)
    start_active_time = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"{self.id} {self.username} {self.email} {self.access} {self.active} {self.start_active_time}"
