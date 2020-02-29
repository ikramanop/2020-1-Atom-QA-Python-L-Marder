"""тесты для set"""
from random import randint
import pytest


class TestSet1:
    """тесты для set"""
    buff_set = set()

    def test_set_1_1(self):
        """тест функции создания"""
        buff = set()
        assert isinstance(buff, set)

    @pytest.mark.parametrize('i', range(10))
    def test_set_1_2(self, i):
        """тест метода add"""
        self.buff_set.add(i)
        assert i in self.buff_set

    @pytest.mark.parametrize('i', range(10))
    def test_set_1_3(self, i):
        """тест метода remove"""
        self.buff_set.remove(i)
        assert i not in self.buff_set
        with pytest.raises(KeyError):
            assert self.buff_set.remove(i)

    def test_set_1_4(self):
        """тест метода clear"""
        length = randint(10, 100)
        self.buff_set = set(i for i in range(length))
        assert len(self.buff_set) == length
        self.buff_set.clear()
        assert len(self.buff_set) == 0

    def test_set_1_5(self):
        """тест метода update"""
        length = randint(10, 100)
        self.buff_set.update(set(i for i in range(length)))
        assert len(self.buff_set) == length
