"""тесты для dict"""
import pytest


class TestDict1:
    """тесты для dict"""
    buff_dict = dict()

    def test_dict_1_1(self):
        """тест создания словаря"""
        buff = dict()
        assert isinstance(buff, dict)

    @pytest.mark.parametrize('i', range(10))
    def test_dict_1_2(self, i):
        """тест добавления в словарь
        и методов keys и values"""
        self.buff_dict[i] = i
        assert i in self.buff_dict.keys()
        assert i in self.buff_dict.values()

    def test_dict_1_3(self):
        """тест метода clear"""
        assert len(self.buff_dict) == 10
        self.buff_dict.clear()
        assert len(self.buff_dict) == 0


class TestDict2:
    """тесты для dict"""
    buff_dict = {i: i for i in range(10)}

    def test_dict_2_1(self):
        """тест метода popitem"""
        assert len(self.buff_dict) == 10
        self.buff_dict.popitem()
        assert len(self.buff_dict) == 9
        assert (9, 9) not in self.buff_dict.items()

    @pytest.mark.parametrize('i', range(10))
    def test_dict_2_2(self, i):
        """тест метода get"""
        if i == 9:
            assert self.buff_dict.get(i) is None
        else:
            assert self.buff_dict.get(i) == i
