from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" TEXT,
    "username" TEXT,
    "last_activity" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "balance" INT NOT NULL  DEFAULT 0,
    "wallet_address" TEXT,
    "is_admin" INT NOT NULL  DEFAULT 0,
    "is_banned" INT NOT NULL  DEFAULT 0,
    "withdraw_request" INT NOT NULL  DEFAULT 0,
    "referred_by_id" BIGINT REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "callback_data" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "data" JSON NOT NULL,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
