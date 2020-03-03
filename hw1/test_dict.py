"""тесты для dict"""
import pytest


class TestDict1:
    """тесты для dict"""
    buff_dict = {i: i for i in range(10)}

    def test_dict_1_1(self):
        """тест создания словаря"""
        buff_dict = dict()
        assert isinstance(buff_dict, dict)

    @pytest.mark.parametrize('i', range(10))
    def test_dict_1_2(self, i):
        """тест методов keys и values"""
        assert i in self.buff_dict.keys()
        assert i in self.buff_dict.values()

    def test_dict_1_3(self):
        """тест метода clear"""
        assert len(self.buff_dict) == 10
        assert self.buff_dict.clear() is None
        assert len(self.buff_dict) == 0


class TestDict2:
    """тесты для dict"""
    buff_dict = {i: i for i in range(10)}

    def test_dict_2_1(self):
        """тест метода popitem"""
        assert len(self.buff_dict) == 10
        assert self.buff_dict.popitem() == (9, 9)
        assert len(self.buff_dict) == 9
        assert (9, 9) not in self.buff_dict.items()

    @pytest.mark.parametrize('i', range(10))
    def test_dict_2_2(self, i):
        """тест метода get"""
        try:
            assert self.buff_dict.get(i) == i
        except AssertionError:
            assert self.buff_dict.get(i) is None
