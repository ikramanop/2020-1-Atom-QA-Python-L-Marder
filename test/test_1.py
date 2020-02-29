"""тесты для list"""
from random import randint
import pytest


class TestList1:
    """тесты для list"""
    buff_list = list()

    def test_list_1_1(self):
        """тест функции создания списка"""
        buff = list()
        assert isinstance(buff, list)

    @pytest.mark.parametrize('i', range(10))
    def test_list_1_2(self, i):
        """тест метода append"""
        self.buff_list.append(i)
        assert self.buff_list[i] == i    
    
    @pytest.mark.parametrize('i', range(10))
    def test_list_1_3(self, i):
        """тест метода remove"""
        self.buff_list.remove(i)
        assert i not in self.buff_list


class TestList2:
    """тест метода sort"""
    buff_list = [randint(0, 100) for i in range(10)]
    
    def test_list_2_1(self):
        """проверка выполнения sort"""
        assert self.buff_list.sort() is None

    @pytest.mark.parametrize('i', range(9))
    def test_list_2_2(self, i):
        """проверка правильности метода"""
        assert self.buff_list[i] <= self.buff_list[i + 1]

 
class TestList3:
    """тест методов copy и reverse"""
    buff_list = [randint(0, 100) for i in range(10)]
    buff_listcopy = buff_list.copy()

    @pytest.mark.parametrize('i', range(10))
    def test_list_3_1(self, i):
        """тест правильности copy"""
        assert self.buff_list[i] == self.buff_listcopy[i]

    def test_list_3_2(self):
        """тест выполнения reverse"""
        assert self.buff_list.reverse() is None

    @pytest.mark.parametrize('i', range(10))
    def test_list_3_3(self, i):
        """тест правильности reverse"""
        assert self.buff_listcopy[::-1][i] == self.buff_list[i]
