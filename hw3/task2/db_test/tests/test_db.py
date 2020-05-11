import pytest
from faker import Faker

from builder import OrmBuilder

fake = Faker(locale='ru_RU')


class TestDB:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, connector):
        self.connection = connector
        self.builder = OrmBuilder(connector)

    def test_database(self):
        for _ in range(10):
            self.builder.add_data()

        data = self.connection.sql('SELECT count(*) as `count` FROM `test_table`')
        for row in data:
            assert row['count'] == 10
