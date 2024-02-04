import subprocess
from bot.models.user_models import User
from bot.config import TS_PROJECT_DIR, TS_SCRIPT_DIR
from bot.utils.utils import setup_logger

logger = setup_logger(__name__)


async def process_monthly_withdrawals(client):
    users = await User.filter(withdraw_request=True).all()
    for user in users:
        try:
            if user.wallet_address and user.balance > 0:
                ton_amount = str(user.balance * 0.01)
                command = [
                    "npx", "ts-node", TS_SCRIPT_DIR,
                    user.wallet_address, ton_amount
                ]
                subprocess.run(command, cwd=TS_PROJECT_DIR, text=True)

                user.balance = 0
                logger.info(f"Sent ton for {user.name} to wallet {user.wallet_address}")
                await client.send_message(
                    user.id, f"{ton_amount} ton coins has been transferred to your wallet: {user.wallet_address}"
                )

            user.withdraw_request = False
            await user.save()

        except Exception as e:
            logger.error(f"Error while sending ton to wallet {user.wallet_address}: {e}", exc_info=True)
            continue
