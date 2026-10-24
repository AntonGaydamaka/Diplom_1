from src.bun import Bun
from testing_data import TestingData
import pytest

class TestBun:
    def test_get_name_of_the_bun_name_got(self, name):
        
        price = TestingData.BLACK_BUN_PRICE
        bun = Bun(name, price)
        
        assert bun.get_name() == name
    
    @pytest.mark.parametrize('name', [
        TestingData.BLACK_BUN_NAME,
        TestingData.WHITE_BUN_NAME,
        TestingData.RED_BUN_NAME
    ])
    def test_get_name_of_the_bun_name_got(self, name):
        price = TestingData.BLACK_BUN_PRICE  # Fixed price
        bun = Bun(name, price)
        
        assert bun.get_name() == name
    
    @pytest.mark.parametrize('price', [
        TestingData.BLACK_BUN_PRICE,
        TestingData.WHITE_BUN_PRICE,
        TestingData.RED_BUN_PRICE
    ])
    def test_get_price_of_the_bun_price_got(self, price):
        name = TestingData.BLACK_BUN_NAME  # Fixed name
        bun = Bun(name, price)
        
        assert bun.get_price() == price