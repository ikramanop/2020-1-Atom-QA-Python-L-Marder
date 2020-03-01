"""тесты для list"""
from random import randint
import pytest


class TestList1:
    """тесты для list"""

    def test_list_1_1(self):
        """тест функции создания списка"""
        buff_list = list()
        assert isinstance(buff_list, list)

    def test_list_1_2(self):
        """тест метода append"""
        rand_num = randint(10, 1000)
        buff_list = list()
        assert len(buff_list) == 0
        assert buff_list.append(rand_num) is None
        assert len(buff_list) == 1
        assert rand_num in buff_list
    
    def test_list_1_3(self):
        """тест метода remove"""
        rand_num = randint(10, 1000)
        buff_list = [rand_num]
        assert len(buff_list) == 1
        assert buff_list.remove(rand_num) is None
        assert len(buff_list) == 0
        assert rand_num not in buff_list
        with pytest.raises(ValueError):
            assert buff_list.remove(rand_num)


class TestList2:
    """тест метода sort"""
    buff_list = [randint(0, 100) for i in range(10)]
    buff_list.sort()

    @pytest.mark.parametrize('i', range(9))
    def test_list_2_1(self, i):
        """проверка правильности sort"""
        assert self.buff_list[i] <= self.buff_list[i + 1]

 
class TestList3:
    """тест метода copy"""
    buff_list = [randint(0, 100) for i in range(10)]
    buff_listcopy = buff_list.copy()

    @pytest.mark.parametrize('i', range(10))
    def test_list_3_1(self, i):
        """тест правильности copy"""
        assert self.buff_list[i] == self.buff_listcopy[i]


class TestList4:
    """тест метода reverse"""
    buff_list = [randint(0, 100) for i in range(10)]
    buff_listcopy = buff_list.copy()
    buff_list.reverse()

    @pytest.mark.parametrize('i', range(10))
    def test_list_4_1(self, i):
        """тест правильности reverse"""
        assert self.buff_listcopy[::-1][i] == self.buff_list[i]
