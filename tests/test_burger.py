from testing_data import TestingData
from src.bun import Bun
from src.ingredient import Ingredient
from src.ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING
import pytest

class TestBurger:
    @pytest.mark.parametrize('name, price', [
        (TestingData.BLACK_BUN_NAME, TestingData.BLACK_BUN_PRICE),
        (TestingData.WHITE_BUN_NAME, TestingData.WHITE_BUN_PRICE),
        (TestingData.RED_BUN_NAME, TestingData.RED_BUN_PRICE)
    ])
    def test_set_buns_to_burger_selected_buns_added_to_the_burger(self, mock, burger, name, price):
        mock.get_name.return_value = name
        mock.get_price.return_value = price
        burger.set_buns(mock)
        
        assert burger.bun.get_name() == name and burger.bun.get_price() == price
    
    def test_add_ingredient_to_burger_selected_ingredients_added_to_the_burger(self, mock, burger):
        # Test with one ingredient type - behavior is same for all
        mock.get_type.return_value = INGREDIENT_TYPE_SAUCE
        mock.get_name.return_value = TestingData.HOT_SAUCE_NAME
        mock.get_price.return_value = TestingData.HOT_SAUCE_PRICE
        burger.add_ingredient(mock)
        
        assert burger.ingredients == [mock]
    
    def test_remove_ingredient_from_burger_added_ingredient_is_removed(self, mock, burger):
        # Test removal - behavior is same regardless of ingredient type
        mock.get_type.return_value = INGREDIENT_TYPE_SAUCE
        mock.get_name.return_value = TestingData.HOT_SAUCE_NAME
        mock.get_price.return_value = TestingData.HOT_SAUCE_PRICE
        burger.add_ingredient(mock)
        burger.remove_ingredient(0)
        
        assert burger.ingredients == []
    
    def test_move_ingredient_in_burger_ingredients_are_swapped(self, burger):
        # Test with one set of ingredients - behavior is same for all combinations
        ingredient_0 = Ingredient(INGREDIENT_TYPE_SAUCE, TestingData.HOT_SAUCE_NAME, TestingData.HOT_SAUCE_PRICE)
        ingredient_1 = Ingredient(INGREDIENT_TYPE_FILLING, TestingData.CUTLET_FILLING_NAME, TestingData.CUTLET_FILLING_PRICE)
        burger.add_ingredient(ingredient_0)
        burger.add_ingredient(ingredient_1)
        burger.move_ingredient(0, 1)
        
        assert burger.ingredients[1].name == ingredient_0.name
        assert burger.ingredients[0].name == ingredient_1.name
    
    @pytest.mark.parametrize('bun_name, bun_price', [
        (TestingData.BLACK_BUN_NAME, TestingData.BLACK_BUN_PRICE),
        (TestingData.WHITE_BUN_NAME, TestingData.WHITE_BUN_PRICE),
        (TestingData.RED_BUN_NAME, TestingData.RED_BUN_PRICE)
    ])
    def test_get_price_of_the_burger_price_is_calculated_from_buns_and_ingredient_prices_correctly(self, burger, bun_name, bun_price):
        # Test only bun variation - ingredient can be fixed
        bun = Bun(bun_name, bun_price)
        ingredient = Ingredient(INGREDIENT_TYPE_SAUCE, TestingData.HOT_SAUCE_NAME, TestingData.HOT_SAUCE_PRICE)
        burger.set_buns(bun)
        burger.add_ingredient(ingredient)
        expected_price = bun_price * 2 + TestingData.HOT_SAUCE_PRICE
        
        assert burger.get_price() == expected_price
    
    @pytest.mark.parametrize('bun_name, bun_price', [
        (TestingData.BLACK_BUN_NAME, TestingData.BLACK_BUN_PRICE),
        (TestingData.WHITE_BUN_NAME, TestingData.WHITE_BUN_PRICE),
        (TestingData.RED_BUN_NAME, TestingData.RED_BUN_PRICE)
    ])
    def test_get_receipt_of_burger_with_only_buns_in_it_shows_only_buns_and_their_prices(self, burger, bun_name, bun_price):
        bun = Bun(bun_name, bun_price)
        burger.set_buns(bun)
        expected_receipt = f'(==== {bun.get_name()} ====)\n(==== {bun.get_name()} ====)\n\nPrice: {bun.get_price() * 2}'
        
        assert burger.get_receipt() == expected_receipt

    def test_get_receipt_of_burger_with_buns_and_one_ingredient_in_it(self, burger):
        # Test with one fixed set - logic is same for all combinations
        bun = Bun(TestingData.BLACK_BUN_NAME, TestingData.BLACK_BUN_PRICE)
        ingredient = Ingredient(INGREDIENT_TYPE_SAUCE, TestingData.HOT_SAUCE_NAME, TestingData.HOT_SAUCE_PRICE)
        burger.set_buns(bun)
        burger.add_ingredient(ingredient)
        expected_receipt = (
            f"(==== {bun.get_name()} ====)\n"
            f"= {str(INGREDIENT_TYPE_SAUCE).lower()} {ingredient.get_name()} =\n"
            f"(==== {bun.get_name()} ====)\n"
            f"\nPrice: {bun.get_price() * 2 + ingredient.get_price()}"
        )
        
        assert burger.get_receipt() == expected_receipt

    def test_get_receipt_multiple_ingredients(self, burger):
        # Test with one fixed combination - logic is same for all
        bun = Bun(TestingData.BLACK_BUN_NAME, TestingData.BLACK_BUN_PRICE)
        ingredient_1 = Ingredient(INGREDIENT_TYPE_SAUCE, TestingData.HOT_SAUCE_NAME, TestingData.HOT_SAUCE_PRICE)
        ingredient_2 = Ingredient(INGREDIENT_TYPE_FILLING, TestingData.CUTLET_FILLING_NAME, TestingData.CUTLET_FILLING_PRICE)
        burger.set_buns(bun)
        burger.add_ingredient(ingredient_1)
        burger.add_ingredient(ingredient_2)
        expected_receipt = (
            f"(==== {bun.get_name()} ====)\n"
            f"= {str(INGREDIENT_TYPE_SAUCE).lower()} {ingredient_1.get_name()} =\n"
            f"= {str(INGREDIENT_TYPE_FILLING).lower()} {ingredient_2.get_name()} =\n"
            f"(==== {bun.get_name()} ====)\n"
            f"\nPrice: {bun.get_price() * 2 + ingredient_1.get_price() + ingredient_2.get_price()}"
        )
        
        assert burger.get_receipt() == expected_receipt