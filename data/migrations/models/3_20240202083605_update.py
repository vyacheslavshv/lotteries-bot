from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "channel_group" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" TEXT NOT NULL,
    "url" TEXT NOT NULL
);
        CREATE TABLE IF NOT EXISTS "user_channel_group" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "channel_group_id" BIGINT NOT NULL REFERENCES "channel_group" ("id") ON DELETE CASCADE,
    "user_id" BIGINT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "channel_group";
        DROP TABLE IF EXISTS "user_channel_group";"""
