# Standard Library
import json
from unittest import mock

# From apps
from api.handler import (
    delete_recipe_handler,
    get_recipe_handler,
    list_or_search_recipes_handler,
    patch_recipe_handler,
    post_recipe_handler,
)


@mock.patch(
    "src.api.handler.RecipesService.get_recipe",
    return_value={"status": "success", "data": {"id": "1", "name": "Pizza"}},
)
def test_get_recipe_handler_success(mock_get_recipe):
    event = {"pathParameters": {"id": "1"}}
    context = mock.Mock()
    response = get_recipe_handler(event, context)

    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == {"status": "success", "data": {"id": "1", "name": "Pizza"}}
    mock_get_recipe.assert_called_once_with("1")


@mock.patch(
    "src.api.handler.RecipesService.get_recipe", return_value={"status": "error", "message": "Recipe not found"}
)
def test_get_recipe_handler_not_found(mock_get_recipe):
    event = {"pathParameters": {"id": "999"}}
    context = mock.Mock()
    response = get_recipe_handler(event, context)

    assert response["statusCode"] == 404
    assert json.loads(response["body"]) == {"status": "error", "message": "Recipe not found"}
    mock_get_recipe.assert_called_once_with("999")


@mock.patch(
    "src.api.handler.RecipesService.create_recipe",
    return_value={"status": "success", "data": {"id": "1", "name": "Pizza"}},
)
def test_post_recipe_handler_success(mock_create_recipe):
    event = {"body": json.dumps({"name": "Pizza", "description": "Bake it", "ingredients": [{"name": "Cheese"}]})}
    context = mock.Mock()
    response = post_recipe_handler(event, context)

    assert response["statusCode"] == 201
    assert json.loads(response["body"]) == {"status": "success", "data": {"id": "1", "name": "Pizza"}}
    mock_create_recipe.assert_called_once_with(
        {"name": "Pizza", "description": "Bake it", "ingredients": [{"name": "Cheese"}]}
    )


def test_post_recipe_handler_invalid_json():
    event = {"body": "invalid json"}
    context = mock.Mock()
    response = post_recipe_handler(event, context)

    assert response["statusCode"] == 400
    assert json.loads(response["body"]) == {
        "status": "error",
        "message": "Invalid JSON input: Expecting value: line 1 column 1 (char 0)",
    }


@mock.patch(
    "src.api.handler.RecipesService.list_recipes",
    return_value={"status": "success", "data": [{"id": "1", "name": "Pizza"}]},
)
def test_list_recipes_handler(mock_list_recipes):
    event = {"queryStringParameters": None}
    context = mock.Mock()
    response = list_or_search_recipes_handler(event, context)

    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == {"status": "success", "data": [{"id": "1", "name": "Pizza"}]}
    mock_list_recipes.assert_called_once()


@mock.patch(
    "src.api.handler.RecipesService.search_recipes_by_name",
    return_value={"status": "success", "data": [{"id": "1", "name": "Pizza"}]},
)
def test_search_recipes_handler(mock_search_recipes):
    event = {"queryStringParameters": {"name": "Pizza"}}
    context = mock.Mock()
    response = list_or_search_recipes_handler(event, context)

    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == {"status": "success", "data": [{"id": "1", "name": "Pizza"}]}
    mock_search_recipes.assert_called_once_with("Pizza")


@mock.patch(
    "src.api.handler.RecipesService.update_recipe",
    return_value={"status": "success", "data": {"id": "1", "name": "Updated Pizza"}},
)
def test_patch_recipe_handler_success(mock_update_recipe):
    event = {"pathParameters": {"id": "1"}, "body": json.dumps({"name": "Updated Pizza"})}
    context = mock.Mock()
    response = patch_recipe_handler(event, context)

    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == {"status": "success", "data": {"id": "1", "name": "Updated Pizza"}}
    mock_update_recipe.assert_called_once_with("1", {"name": "Updated Pizza"})


@mock.patch("src.api.handler.RecipesService.delete_recipe", return_value={"status": "success"})
def test_delete_recipe_handler_success(mock_delete_recipe):
    event = {"pathParameters": {"id": "1"}}
    context = mock.Mock()
    response = delete_recipe_handler(event, context)

    assert response["statusCode"] == 204
    assert response["body"] == ""
    mock_delete_recipe.assert_called_once_with("1")


@mock.patch(
    "src.api.handler.RecipesService.delete_recipe", return_value={"status": "error", "message": "Recipe not found"}
)
def test_delete_recipe_handler_not_found(mock_delete_recipe):
    event = {"pathParameters": {"id": "999"}}
    context = mock.Mock()
    response = delete_recipe_handler(event, context)

    assert response["statusCode"] == 404
    assert json.loads(response["body"]) == {"status": "error", "message": "Recipe not found"}
    mock_delete_recipe.assert_called_once_with("999")
