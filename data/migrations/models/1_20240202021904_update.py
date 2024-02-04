from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ADD "captcha_passed" INT NOT NULL  DEFAULT 0;
        ALTER TABLE "user" ADD "emoji_passed" INT NOT NULL  DEFAULT 0;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" DROP COLUMN "captcha_passed";
        ALTER TABLE "user" DROP COLUMN "emoji_passed";"""
