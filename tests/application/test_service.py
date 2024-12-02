# Standard Library
from unittest import mock

# Dependencies
import pytest
from pydantic import ValidationError

# From apps
from application.service import RecipesService
from models.recipes import Ingredient, Recipe


@pytest.fixture
def mock_repository():
    with mock.patch("src.application.service.RecipesRepository") as MockRepo:
        yield MockRepo


def test_get_recipe_success(mock_repository):
    mock_repository.return_value.get_recipe.return_value = {"id": "1", "name": "Pizza"}
    response = RecipesService.get_recipe("1")
    assert response == {"status": "success", "data": {"id": "1", "name": "Pizza"}}
    mock_repository.return_value.get_recipe.assert_called_once_with("1")


def test_get_recipe_not_found(mock_repository):
    mock_repository.return_value.get_recipe.return_value = {"error": True, "message": "Recipe not found"}
    response = RecipesService.get_recipe("999")
    assert response == {"status": "error", "message": "Recipe not found"}
    mock_repository.return_value.get_recipe.assert_called_once_with("999")


def test_create_recipe_success(mock_repository):
    mock_repository.return_value.insert_recipe.return_value = Recipe(
        id="1", name="Pizza", description="Bake it", ingredients=[Ingredient(name="Flour")]
    )
    data = {"name": "Pizza", "description": "Bake it", "ingredients": []}
    response = RecipesService.create_recipe(data)
    assert response == {
        "status": "success",
        "data": {"id": "1", "name": "Pizza", "description": "Bake it", "ingredients": [{"name": "Flour"}]},
    }
    mock_repository.return_value.insert_recipe.assert_called_once()


@mock.patch("src.models.recipes.Recipe", side_effect=ValidationError)
def test_create_recipe_invalid_data(mock_repository):
    data = {"invalid_field": "value"}
    response = RecipesService.create_recipe(data)

    assert response["status"] == "error"
    assert "validation error" in response["message"].lower()


def test_list_recipes_success(mock_repository):
    mock_repository.return_value.list_recipes.return_value = [
        {"id": "1", "name": "Pizza", "description": "Bake it", "ingredients": [{"name": "Flour"}]},
        {"id": "2", "name": "Burger", "description": "Grill it", "ingredients": [{"name": "Bun"}]},
    ]
    response = RecipesService.list_recipes()
    assert response == {
        "status": "success",
        "data": [
            {"id": "1", "name": "Pizza", "description": "Bake it", "ingredients": [{"name": "Flour"}]},
            {"id": "2", "name": "Burger", "description": "Grill it", "ingredients": [{"name": "Bun"}]},
        ],
    }
    mock_repository.return_value.list_recipes.assert_called_once()


def test_list_recipes_no_data(mock_repository):
    mock_repository.return_value.list_recipes.return_value = {"error": True, "message": "No recipes found"}
    response = RecipesService.list_recipes()
    assert response == {"status": "error", "message": "No recipes found"}
    mock_repository.return_value.list_recipes.assert_called_once()


def test_search_recipes_by_name_success(mock_repository):
    mock_repository.return_value.search_recipes_by_name.return_value = [
        {"id": "1", "name": "Dutch baby", "description": "Beat it", "ingredients": [{"name": "Flour"}]},
    ]
    response = RecipesService.search_recipes_by_name("Pizza")
    assert response == {
        "status": "success",
        "data": [{"id": "1", "name": "Dutch baby", "description": "Beat it", "ingredients": [{"name": "Flour"}]}],
    }
    mock_repository.return_value.search_recipes_by_name.assert_called_once_with("Pizza")


def test_update_recipe_success(mock_repository):
    mock_repository.return_value.update_recipe.return_value = {"id": "1", "name": "Updated Pizza"}
    updates = {"name": "Updated Pizza"}
    response = RecipesService.update_recipe("1", updates)
    assert response == {"status": "success", "data": {"id": "1", "name": "Updated Pizza"}}
    mock_repository.return_value.update_recipe.assert_called_once_with("1", updates)


def test_update_recipe_invalid_field(mock_repository):
    updates = {"invalid_field": "value"}
    response = RecipesService.update_recipe("1", updates)
    assert response == {"status": "error", "message": "Invalid field: invalid_field"}


def test_delete_recipe_success(mock_repository):
    mock_repository.return_value.delete_recipe.return_value = None
    response = RecipesService.delete_recipe("1")
    assert response == {"status": "success", "message": None}
    mock_repository.return_value.delete_recipe.assert_called_once_with("1")


def test_delete_recipe_not_found(mock_repository):
    mock_repository.return_value.delete_recipe.return_value = {"error": True, "message": "Recipe not found"}
    response = RecipesService.delete_recipe("999")
    assert response == {"status": "error", "message": "Recipe not found"}
    mock_repository.return_value.delete_recipe.assert_called_once_with("999")
