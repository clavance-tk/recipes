# Standard Library
import os

# Dependencies
import pytest

# From apps
from configuration.database import get_resource
from models.recipes import Recipe
from repository.recipes import RecipesRepository
from tests.constants import ENDPOINT_URL, TABLE_NAME


@pytest.fixture(scope="module", autouse=True)
def setup_dynamodb():
    print(f"LOCALSTACK_HOSTNAME={os.getenv('LOCALSTACK_HOSTNAME')}")
    dynamodb = get_resource(endpoint_url=ENDPOINT_URL)
    table = dynamodb.create_table(
        TableName=TABLE_NAME,
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )
    table.wait_until_exists()
    yield
    table.delete()
    table.wait_until_not_exists()


def test_insert_recipe():
    repository = RecipesRepository(TABLE_NAME, ENDPOINT_URL)
    recipe = Recipe(name="Pizza", description="Bake it", ingredients=[{"name": "Cheese"}])

    result = repository.insert_recipe(recipe)

    assert isinstance(result, Recipe)
    assert result.name == "Pizza"
    assert result.description == "Bake it"
    assert result.id is not None


def test_get_recipe():
    repository = RecipesRepository(TABLE_NAME, ENDPOINT_URL)
    recipe = Recipe(name="Burger", description="Grill it", ingredients=[{"name": "Beef"}])
    inserted_recipe = repository.insert_recipe(recipe)

    retrieved_recipe = repository.get_recipe(inserted_recipe.id)

    assert retrieved_recipe["id"] == inserted_recipe.id
    assert retrieved_recipe["name"] == "Burger"
    assert retrieved_recipe["description"] == "Grill it"


def test_list_recipes():
    repository = RecipesRepository(TABLE_NAME, ENDPOINT_URL)
    recipes = repository.list_recipes()

    assert len(recipes) > 0


def test_search_recipes_by_name():
    repository = RecipesRepository(TABLE_NAME, ENDPOINT_URL)

    recipe = Recipe(name="Pizza", description="Bake it", ingredients=[{"name": "Cheese"}])
    repository.insert_recipe(recipe)

    result = repository.search_recipes_by_name("Piz")

    # Assertions
    assert isinstance(result, list)
    assert len(result) > 0
    assert result[0]["name"] == "Pizza"


def test_update_recipe():
    repository = RecipesRepository(TABLE_NAME, ENDPOINT_URL)

    recipe = Recipe(name="Pizza", description="Bake it", ingredients=[{"name": "Cheese"}])
    inserted_recipe = repository.insert_recipe(recipe)

    updates = {"name": "Updated Pizza", "description": "Bake it with extra cheese"}
    updated_recipe = repository.update_recipe(inserted_recipe.id, updates)

    assert isinstance(updated_recipe, dict)
    assert updated_recipe["name"] == "Updated Pizza"
    assert updated_recipe["description"] == "Bake it with extra cheese"


def test_delete_recipe():
    repository = RecipesRepository(TABLE_NAME, ENDPOINT_URL)

    recipe = Recipe(name="Pizza", description="Bake it", ingredients=[{"name": "Cheese"}])
    inserted_recipe = repository.insert_recipe(recipe)

    result = repository.delete_recipe(inserted_recipe.id)

    assert result is None

    retrieved_recipe = repository.get_recipe(inserted_recipe.id)
    assert isinstance(retrieved_recipe, dict)
    assert retrieved_recipe["error"] is True
    assert "not found" in retrieved_recipe["message"]
