"""тесты для set"""
from random import randint
import pytest


class TestSet1:
    """тесты для set"""

    def test_set_1_1(self):
        """тест функции создания"""
        buff_set = set()
        assert isinstance(buff_set, set)

    def test_set_1_2(self):
        """тест метода add"""
        rand_num = randint(10, 1000)
        buff_set = set()
        assert len(buff_set) == 0
        assert buff_set.add(rand_num) is None
        assert len(buff_set) == 1
        assert rand_num in buff_set

    def test_set_1_3(self):
        """тест метода remove"""
        rand_num = randint(10, 1000)
        buff_set = {rand_num}
        assert len(buff_set) == 1
        assert buff_set.remove(rand_num) is None
        assert len(buff_set) == 0
        assert rand_num not in buff_set
        with pytest.raises(KeyError):
            assert buff_set.remove(rand_num)

    def test_set_1_4(self):
        """тест метода clear"""
        length = randint(10, 100)
        buff_set = set(range(length))
        assert len(buff_set) == length
        assert buff_set.clear() is None
        assert len(buff_set) == 0

    def test_set_1_5(self):
        """тест метода update"""
        length = randint(10, 100)
        buff_set = set()
        assert len(buff_set) == 0
        assert buff_set.update(set(range(length))) is None
        assert len(buff_set) == length


class TestSet2:
    """тест метода copy"""
    buff_set = set(randint(10, 100) for i in range(10))
    buff_setcopy = buff_set.copy()

    def test_set_2_1(self):
        """тест метода copy"""
        assert len(self.buff_set) == len(self.buff_setcopy)

    @pytest.mark.parametrize('i', range(10))
    def test_set_2_2(self, i):
        """тест правильности метода copy"""
        assert  self.buff_set.pop() == self.buff_setcopy.pop()
