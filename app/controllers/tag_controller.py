import os
import logging
from typing import List, Optional
from uuid import uuid4

import boto3
from boto3.dynamodb.conditions import Attr

from ..models.tag import Tag, TagCreate, TagUpdate

logger = logging.getLogger(__name__)


dynamodb = boto3.resource(
    "dynamodb",
    region_name=os.getenv("AWS_DEFAULT_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

table_name = os.getenv("DYNAMO_TABLE", "zettelkasten-tags-1")
table = dynamodb.Table(table_name)


async def create_tag(data: TagCreate) -> Tag:
    tag_id = str(uuid4())
    logger.info("Creating tag '%s' for user '%s'", tag_id, data.userId)
    item = {**data.model_dump(), "tag_id": tag_id}
    table.put_item(Item=item)
    return Tag(**item)


async def list_tags() -> List[Tag]:
    logger.info("Listing all tags")
    response = table.scan()
    items = response.get("Items", [])
    return [Tag(**item) for item in items]


async def list_user_tags(user_id: str) -> List[Tag]:
    logger.info("Listing tags for user '%s'", user_id)
    response = table.scan(FilterExpression=Attr("userId").eq(user_id))
    items = response.get("Items", [])
    return [Tag(**item) for item in items]


async def get_tag(tag_id: str) -> Optional[Tag]:
    logger.info("Fetching tag '%s'", tag_id)
    response = table.get_item(Key={"tag_id": tag_id})
    item = response.get("Item")
    if item:
        return Tag(**item)
    return None


async def update_tag(tag_id: str, data: TagUpdate) -> Optional[Tag]:
    logger.info("Updating tag '%s'", tag_id)
    update_data = data.model_dump(exclude_unset=True)
    if not update_data:
        return await get_tag(tag_id)
    update_expression = "SET " + ", ".join(f"{k}=:{k}" for k in update_data.keys())
    expression_values = {f":{k}": v for k, v in update_data.items()}
    table.update_item(
        Key={"tag_id": tag_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_values,
    )
    return await get_tag(tag_id)


async def delete_tag(tag_id: str) -> bool:
    logger.info("Deleting tag '%s'", tag_id)
    response = table.delete_item(Key={"tag_id": tag_id}, ReturnValues="ALL_OLD")
    return "Attributes" in response
