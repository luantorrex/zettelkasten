import os
import logging
from typing import Dict, List, Optional

import boto3

from ..models.tag import Tag, TagCreate, TagUpdate

logger = logging.getLogger(__name__)


dynamodb = boto3.resource(
    "dynamodb",
    region_name=os.getenv("AWS_DEFAULT_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

table_name = os.getenv("DYNAMO_TABLE", "zetteltasken-tags-1")
table = dynamodb.Table(table_name)


async def create_tag(data: TagCreate) -> Tag:
    logger.info("Creating tags for user '%s'", data.userId)
    item = data.model_dump()
    table.put_item(Item=item)
    return Tag(**item)


async def list_tags() -> Dict[str, List[str]]:
    logger.info("Listing all tags")
    response = table.scan()
    items = response.get("Items", [])
    return {item["userId"]: item.get("tags", []) for item in items}


async def get_tag(user_id: str) -> Optional[Dict[str, List[str]]]:
    logger.info("Fetching tags for user '%s'", user_id)
    response = table.get_item(Key={"userId": user_id})
    item = response.get("Item")
    if item:
        return {user_id: item.get("tags", [])}
    return None


async def update_tag(user_id: str, data: TagUpdate) -> Optional[Tag]:
    logger.info("Updating tags for user '%s'", user_id)
    update_data = data.model_dump(exclude_unset=True)
    if not update_data:
        existing = await get_tag(user_id)
        if existing:
            return Tag(userId=user_id, tags=existing[user_id])
        return None
    table.update_item(
        Key={"userId": user_id},
        UpdateExpression="SET tags=:tags",
        ExpressionAttributeValues={":tags": update_data["tags"]},
    )
    updated = await get_tag(user_id)
    if updated:
        return Tag(userId=user_id, tags=updated[user_id])
    return None


async def delete_tag(user_id: str) -> bool:
    logger.info("Deleting tags for user '%s'", user_id)
    response = table.delete_item(Key={"userId": user_id}, ReturnValues="ALL_OLD")
    return "Attributes" in response
