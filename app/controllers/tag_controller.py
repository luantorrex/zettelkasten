import os
import logging
from typing import List, Optional

import boto3

from ..models.tag import Tag, TagCreate, TagUpdate

logger = logging.getLogger(__name__)


dynamodb = boto3.resource(
    "dynamodb",
    region_name=os.getenv("AWS_DEFAULT_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

table_name = os.getenv("DYNAMO_TABLE", "zetteltasken-tags")
table = dynamodb.Table(table_name)


async def create_tag(data: TagCreate) -> Tag:
    logger.info("Creating tag '%s'", data.tag)
    item = data.model_dump()
    table.put_item(Item=item)
    return Tag(**item)


async def list_tags() -> List[Tag]:
    logger.info("Listing all tags")
    response = table.scan()
    items = response.get("Items", [])
    return [Tag(**item) for item in items]


async def get_tag(tag_name: str) -> Optional[Tag]:
    logger.info("Fetching tag '%s'", tag_name)
    response = table.get_item(Key={"tag": tag_name})
    item = response.get("Item")
    return Tag(**item) if item else None


async def update_tag(tag_name: str, data: TagUpdate) -> Optional[Tag]:
    logger.info("Updating tag '%s'", tag_name)
    update_data = data.model_dump(exclude_unset=True)
    if not update_data:
        return await get_tag(tag_name)
    update_expr = "SET " + ", ".join(f"#{k}=:{k}" for k in update_data)
    expr_attr_names = {f"#{k}": k for k in update_data}
    expr_attr_values = {f":{k}": v for k, v in update_data.items()}
    table.update_item(
        Key={"tag": tag_name},
        UpdateExpression=update_expr,
        ExpressionAttributeNames=expr_attr_names,
        ExpressionAttributeValues=expr_attr_values,
    )
    return await get_tag(tag_name)


async def delete_tag(tag_name: str) -> bool:
    logger.info("Deleting tag '%s'", tag_name)
    response = table.delete_item(Key={"tag": tag_name}, ReturnValues="ALL_OLD")
    return "Attributes" in response
