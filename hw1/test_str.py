"""тесты для string"""
import pytest


class TestStr1:
    """тесты методов, связанных с верхним регистром"""
    string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    @pytest.mark.parametrize('i', range(len(string)))
    def test_str_1_1(self, i):
        """тест функции ord"""
        assert 65 <= ord(self.string[i]) <= 90

    def test_str_1_2(self):
        """тест метода isupper"""
        assert self.string.isupper()

    def test_str_1_3(self):
        """тест методов lower и islower"""
        self.string = self.string.lower()
        assert self.string == 'abcdefghijklmnopqrstuvwxyz'
        assert self.string.islower()


class TestStr2:
    """тесты методов, связанных с нижним регистром"""
    string = 'abcdefghijklmnopqrstuvwxyz'

    @pytest.mark.parametrize('i', range(len(string)))
    def test_str_2_1(self, i):
        """тест функции ord"""
        assert 97 <= ord(self.string[i]) <= 122

    def test_str_2_2(self):
        """тест метода islower"""
        assert self.string.islower()

    def test_str_2_3(self):
        """тест методов upper и lower"""
        self.string = self.string.upper()
        assert self.string == 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        assert self.string.isupper()


class TestStr3:
    """тесты методов, связанных со списками"""
    string = ''

    def test_str_3_1(self):
        """тест метода join и метода isnumeric"""
        self.string = self.string.join([str(i) for i in range(10)])
        assert self.string == '0123456789'
        assert self.string.isnumeric()

    def test_str_3_2(self):
        """тест метода split"""
        self.string = 'stringy string'
        buff_list = self.string.split(' ')
        assert len(buff_list) == 2
        assert buff_list[0] == 'stringy' and buff_list[1] == 'string'
