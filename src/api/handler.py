from __future__ import annotations

# Standard Library
import json
from typing import Any, Dict

# From apps
from application.service import RecipesService


def get_recipe_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    recipe_id = event["pathParameters"]["id"]

    response = RecipesService.get_recipe(recipe_id)

    return {"statusCode": 200 if response["status"] == "success" else 404, "body": json.dumps(response)}


# since this is just an exercise, the recipe Name field is not unique - duplicates are accepted
def post_recipe_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        body = json.loads(event["body"])

        response = RecipesService.create_recipe(body)

        response = {"statusCode": 201 if response["status"] == "success" else 400, "body": json.dumps(response)}

        return r
    except json.JSONDecodeError as e:
        return {"statusCode": 400, "body": json.dumps({"status": "error", "message": f"Invalid JSON input: {str(e)}"})}
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"status": "error", "message": f"An unexpected error occurred: {str(e)}"}),
        }


def list_or_search_recipes_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        query_params = event.get("queryStringParameters") or {}
        name = query_params.get("name")

        # this logic is required because API Gateway doesn't allow differentiation of endpoints by the presence of query parameters
        # so both list and search by query param functions are on the same GET /recipes endpoint and handler
        if name:
            response = RecipesService.search_recipes_by_name(name)
        else:
            response = RecipesService.list_recipes()

        return {"statusCode": 200 if response["status"] == "success" else 404, "body": json.dumps(response)}
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"status": "error", "message": f"An unexpected error occurred: {str(e)}"}),
        }


def patch_recipe_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        recipe_id = event["pathParameters"]["id"]
        updates = json.loads(event["body"])
        response = RecipesService.update_recipe(recipe_id, updates)

        return {"statusCode": 200 if response["status"] == "success" else 400, "body": json.dumps(response)}

    except json.JSONDecodeError as e:
        return {"statusCode": 400, "body": json.dumps({"status": "error", "message": f"Invalid JSON input: {str(e)}"})}

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"status": "error", "message": f"An unexpected error occurred: {str(e)}"}),
        }


def delete_recipe_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        recipe_id = event["pathParameters"]["id"]
        response = RecipesService.delete_recipe(recipe_id)

        return {
            "statusCode": 204 if response["status"] == "success" else 404,
            "body": "" if response["status"] == "success" else json.dumps(response),
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"status": "error", "message": f"An unexpected error occurred: {str(e)}"}),
        }
