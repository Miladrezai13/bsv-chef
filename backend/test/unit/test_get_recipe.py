import pytest
from unittest.mock import patch
from src.controllers.receipecontroller import ReceipeController
from src.static.diets import Diet

@pytest.mark.unit
def recipes():
    return {
        'cake': {'name': 'Cake', 'diets': ['vegetarian'], 'ingredients': {'Flour': 100, 'Egg': 50}},
        'recipe_5': {'name': 'Recipe 5', 'diets': ['normal'], 'ingredients': {'Flour': 100}},
        'parametrized': {'name': 'Parametrized', 'diets': ['normal'], 'ingredients': {'Egg': 4, 'Milk': 100, 'Sugar': 25}},
    }

@pytest.mark.unit
def available_items():
    return {
        'full': {'Flour': 100, 'Egg': 50},
        'partial': {'Flour': 50},
        'excess': {'Egg': 4, 'Milk': 100, 'Sugar': 25, 'Butter': 10},
        'none': {},
    }

@patch('src.controllers.receipecontroller.calculate_readiness')
def test_optimal_ingredients_invalid_diet(mock_calculate_readiness, recipes, available_items):
    # Test case: 1
    mock_calculate_readiness.return_value = 1  
    controller = ReceipeController(None)
    result = controller.get_receipe_readiness(recipes['cake'], available_items['full'], Diet.VEGAN)
    assert result is None, "Expected None since diet does not match"

@patch('src.controllers.receipecontroller.calculate_readiness')
def test_partial_ingredients_valid_diet(mock_calculate_readiness, recipes, available_items):
    # Test case: 2
    mock_calculate_readiness.return_value = 0.5
    controller = ReceipeController(None)
    result = controller.get_receipe_readiness(recipes['recipe_5'], available_items['partial'], Diet.NORMAL)
    assert result is None or result < 0.1, "Expected None or readiness below threshold"

@patch('src.controllers.receipecontroller.calculate_readiness')
def test_excess_ingredients_valid_diet(mock_calculate_readiness, recipes, available_items):
    # Test case: 3
    mock_calculate_readiness.return_value = 1
    controller = ReceipeController(None)
    result = controller.get_receipe_readiness(recipes['parametrized'], available_items['excess'], Diet.NORMAL)
    assert result == 1, "Expected readiness of 1 since all ingredients are present and excess"

@patch('src.controllers.receipecontroller.calculate_readiness')
def test_no_ingredients_available(mock_calculate_readiness, recipes, available_items):
    # Test case: 4
    mock_calculate_readiness.return_value = 0 
    controller = ReceipeController(None)
    result = controller.get_receipe_readiness(recipes['parametrized'], available_items['none'], Diet.NORMAL)
    assert result is None, "Expected None since no ingredients are available"
