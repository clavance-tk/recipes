# Standard Library
from typing import Any, Dict, List, Union

# From apps
from models.recipes import Ingredient, Recipe
from repository.errors import RepositoryError
from repository.recipes import RecipesRepository, logger


class RecipesService:
    @staticmethod
    def get_recipe(recipe_id: str) -> Dict[str, Union[str, Dict]]:
        try:
            repository = RecipesRepository()
            recipe_data = repository.get_recipe(recipe_id)

            # checks required because repository can return Recipe, dict, or error
            if isinstance(recipe_data, dict) and "error" in recipe_data:
                return {"status": "error", "message": recipe_data["message"]}

            if isinstance(recipe_data, dict):
                if "ingredients" in recipe_data:
                    recipe_data["ingredients"] = [Ingredient(**item) for item in recipe_data["ingredients"]]

                recipe = Recipe(**recipe_data)
            elif isinstance(recipe_data, Recipe):
                recipe = recipe_data
            else:
                return {"status": "error", "message": "Unexpected data format from repository"}

            return {"status": "success", "data": recipe.model_dump()}

        except RepositoryError as e:
            return {"status": "error", "message": str(e)}

        except Exception as e:
            return {"status": "error", "message": f"An unexpected error occurred: {str(e)}"}

    @staticmethod
    def create_recipe(data: dict) -> Dict[str, Union[str, Dict[str, Any]]]:
        try:
            recipe_data = Recipe(**data)

            repository = RecipesRepository()
            result = repository.insert_recipe(recipe_data)

            return {"status": "success", "data": result.model_dump()}

        except RepositoryError as e:
            return {"status": "error", "message": str(e)}

        except Exception as e:
            logger.error("Unexpected error in create_recipe: %s", e)
            return {"status": "error", "message": "An unexpected error occurred."}

    @staticmethod
    def list_recipes() -> Dict[str, Union[str, List[Dict[str, Any]]]]:
        try:
            repository = RecipesRepository()
            recipes = repository.list_recipes()

            recipes_data = [Recipe(**item).model_dump() for item in recipes]

            return {"status": "success", "data": recipes_data}

        except RepositoryError as e:
            return {"status": "error", "message": str(e)}

        except Exception as e:
            logger.error("Unexpected error in list_recipes: %s", e)
            return {"status": "error", "message": "An unexpected error occurred."}

    @staticmethod
    def search_recipes_by_name(name_substring: str) -> Dict[str, Union[str, List[Dict[str, Any]]]]:
        try:
            repository = RecipesRepository()
            recipes = repository.search_recipes_by_name(name_substring)

            recipes_data = [Recipe(**item).model_dump() for item in recipes]

            return {"status": "success", "data": recipes_data}

        except RepositoryError as e:
            return {"status": "error", "message": str(e)}

        except Exception as e:
            logger.error("Unexpected error in search_recipes_by_name: %s", e)
            return {"status": "error", "message": "An unexpected error occurred."}

    @staticmethod
    def update_recipe(recipe_id: str, updates: dict) -> dict:
        try:
            for key in updates:
                if key not in Recipe.model_fields:
                    raise ValueError(f"Invalid field: {key}")

            repository = RecipesRepository()
            updated_recipe = repository.update_recipe(recipe_id, updates)

            return {"status": "success", "data": updated_recipe}

        except ValueError as e:
            return {"status": "error", "message": str(e)}

        except RepositoryError as e:
            return {"status": "error", "message": str(e)}

        except Exception as e:
            logger.error("Unexpected error in update_recipe: %s", e)
            return {"status": "error", "message": "An unexpected error occurred."}

    @staticmethod
    def delete_recipe(recipe_id: str) -> dict:
        try:
            repository = RecipesRepository()
            repository.delete_recipe(recipe_id)

            return {"status": "success", "message": None}

        except RepositoryError as e:
            return {"status": "error", "message": str(e)}

        except Exception as e:
            logger.error("Unexpected error in delete_recipe: %s", e)
            return {"status": "error", "message": "An unexpected error occurred."}
