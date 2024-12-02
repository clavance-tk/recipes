# Standard Library
import logging
import os
import uuid
from typing import Any, Dict, List, Union

# Dependencies
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError

# From apps
from configuration.database import ENDPOINT_URL, get_resource, resolve_table_name
from models.recipes import Recipe
from repository.errors import RepositoryError

logger = logging.getLogger(__name__)


class RecipesRepository:
    def __init__(self, table_name=None, endpoint_url=None):
        self.table_name = table_name or resolve_table_name()
        self.endpoint_url = endpoint_url or os.getenv("ENDPOINT_URL", ENDPOINT_URL)
        self.table = get_resource(self.endpoint_url).Table(self.table_name)

        logger.debug("Initializing repository with table: %s and endpoint: %s", self.table_name, self.endpoint_url)

    def insert_recipe(self, recipe: Recipe) -> Recipe:
        logger.debug("Initializing repository with table: %s and endpoint: %s", self.table_name, self.endpoint_url)

        recipe.id = str(uuid.uuid4())

        try:
            recipe_data = recipe.model_dump()
            self.table.put_item(Item=recipe_data)
            return recipe

        except ClientError as e:
            raise RepositoryError(f"ClientError: {e.response['Error']['Message']}")

        except Exception as e:
            logger.debug("Unexpected error inserting recipe with ID %s: %s", recipe.id, e)
            raise RepositoryError(f"An unexpected error occurred: {str(e)}") from e

    def get_recipe(self, recipe_id: str) -> Union[Recipe, dict]:
        try:
            response = self.table.get_item(Key={"id": recipe_id})
            if "Item" not in response:
                return {"error": True, "message": f"Recipe with ID {recipe_id} not found."}
            return response["Item"]

        except ClientError as e:
            logger.debug("Error retrieving recipe with ID: %s: %s", recipe_id, e)
            raise RepositoryError(f"ClientError: {e.response['Error']['Message']}")

        except Exception as e:
            logger.debug("Unexpected error retrieving recipe with ID: %s: %s", recipe_id, e)
            raise RepositoryError(f"An unexpected error occurred: {str(e)}") from e

    def list_recipes(self) -> Union[List[Dict[str, Any]], dict]:
        try:
            response = self.table.scan()

            if "Items" not in response or not response["Items"]:
                return {"error": True, "message": "No recipes found."}
            return response["Items"]

        except ClientError as e:
            logger.debug("Error listing recipes: %s", e)
            raise RepositoryError(f"ClientError: {e.response['Error']['Message']}")

        except Exception as e:
            logger.debug("Unexpected error listing recipes: %s", e)
            raise RepositoryError(f"An unexpected error occurred: {str(e)}") from e

    def search_recipes_by_name(self, name_substring: str) -> Union[List[Dict[str, Any]], dict]:
        try:
            response = self.table.scan(FilterExpression=Attr("name").contains(name_substring))

            if "Items" not in response or not response["Items"]:
                return {"error": True, "message": "No recipes found."}

            return response["Items"]

        except ClientError as e:
            logger.debug("Error searching recipes: %s", e)
            raise RepositoryError(f"ClientError: {e.response['Error']['Message']}")

        except Exception as e:
            logger.debug("Unexpected error searching recipes: %s", e)
            raise RepositoryError(f"An unexpected error occurred: {str(e)}") from e

    def update_recipe(self, recipe_id: str, updates: dict) -> dict:
        try:
            update_expression = "SET "
            expression_attribute_names = {}
            expression_attribute_values = {}

            # this is needed because the attribute "name" is a reserved keyword in DynamoDB, but also one of our Recipe fields
            # without this logic, we will get the error "Invalid UpdateExpression: Attribute name is a reserved keyword; reserved keyword: name"
            # so we need to map the attribute name to a temporary value then map it back :(
            for key, value in updates.items():
                temp = f"#{key}"
                update_expression += f"{temp} = :{key}, "
                expression_attribute_names[temp] = key
                expression_attribute_values[f":{key}"] = value

            update_expression = update_expression.rstrip(", ")

            response = self.table.update_item(
                Key={"id": recipe_id},
                UpdateExpression=update_expression,
                ExpressionAttributeNames=expression_attribute_names,
                ExpressionAttributeValues=expression_attribute_values,
                ReturnValues="ALL_NEW",
            )

            return response.get("Attributes", {})

        except ClientError as e:
            logger.debug("Error updating recipe with ID %s: %s", recipe_id, e)
            raise RepositoryError(f"ClientError: {e.response['Error']['Message']}")

        except Exception as e:
            logger.debug("Unexpected error updating recipe with ID %s: %s", recipe_id, e)
            raise RepositoryError(f"An unexpected error occurred: {str(e)}") from e

    def delete_recipe(self, recipe_id: str) -> None:
        try:
            self.table.delete_item(Key={"id": recipe_id}, ConditionExpression="attribute_exists(id)")
            return None

        except ClientError as e:
            logger.debug("Error deleting recipe with ID %s: %s", recipe_id, e)
            raise RepositoryError(f"ClientError: {e.response['Error']['Message']}")

        except Exception as e:
            logger.debug("Unexpected deleting recipe with ID %s: %s", recipe_id, e)
            raise RepositoryError(f"An unexpected error occurred: {str(e)}") from e
