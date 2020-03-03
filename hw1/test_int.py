"""тесты для int"""
from random import randint, random
import pytest


class TestInt1:
    """тесты для int"""
    buff_int = randint(0, 1000)
    
    def test_int_1_1(self):
        """тест приведения int к другим типам данных"""
        assert isinstance(self.buff_int, int)
        assert isinstance(str(self.buff_int), str)
        assert isinstance(float(self.buff_int), float)

    def test_int_1_2(self):
        """тест приведения других типов к int"""
        assert isinstance(self.buff_int, int)
        assert isinstance(int(random()), int)
        assert isinstance(int('123456789'), int)
        with pytest.raises(ValueError):
            assert int('string')

    @pytest.mark.parametrize('i', range(3))
    def test_int_1_3(self, i):
        """тест проверки целочисленного деления"""
        assert isinstance(self.buff_int // randint(i + 1, 1000), int)

    def test_int_1_4(self):
        """тест метода bit_length"""
        assert len(bin(self.buff_int)[2::]) == self.buff_int.bit_length()

    def test_int_1_5(self):
        """тест метода from_bytes"""
        buff_bytes = self.buff_int.to_bytes(self.buff_int.bit_length() // 8 + 1, byteorder='big')
        assert self.buff_int == int.from_bytes(buff_bytes, byteorder='big')
