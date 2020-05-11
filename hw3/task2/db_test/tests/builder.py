from faker import Faker

from models.models import Base, Human

fake = Faker(locale='ru_RU')


class OrmBuilder:

    def __init__(self, connector):
        self.connection = connector
        self.engine = connector.connection.engine
        self.create_table()

    def create_table(self):
        if not self.engine.dialect.has_table(self.engine, 'test_table'):
            Base.metadata.tables['test_table'].create(self.engine)

    def add_data(self):
        human = Human(
            name=fake.first_name(),
            surname=fake.last_name(),
            job=fake.job()
        )

        self.connection.session.add(human)
        self.connection.session.commit()
