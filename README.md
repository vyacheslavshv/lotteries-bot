# Lottery Bot Project

The Lottery Bot is a Telegram bot developed to facilitate lottery games, manage wallet transactions, and streamline user interactions within the TON blockchain environment. It integrates various components, including command handlers, a service layer for business logic, models for database operations, and scheduled tasks for routine maintenance and operations.

## Requirements

- Python >= 3.9
- SQLite for database management
- Node.js and npm for running TypeScript scripts
- A TON blockchain wallet with funds for transactions

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/vyacheslavshv/lottery-bot.git
   cd lottery-bot
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install the necessary Python packages:**

   ```bash
   pip install -r requirements.txt
   ```

## Aerich Database Migrations Setup

Aerich is utilized for managing database migrations. Given that the initial Aerich setup and migration files are included in the project repository, you only need to apply the migrations to update your database schema to the latest version.

### Applying Migrations

To apply existing migrations to your database, ensuring it's up to date with the latest schema defined in your project, run:

```bash
aerich upgrade
```

This command applies all pending migrations to the database, making it reflect the current state of your models as defined in `bot/models` and tracked through the migration files in `data/migrations`.

Ensure your `TORTOISE_ORM` configuration in `bot/config.py` is correctly set to point to your database and that Aerich is properly initialized in your project.

## Configuration and Environment Variables

Before running the application, set up your environment variables. These variables are crucial for configuring the bot's settings securely.

### Setting Up Environment Variables

1. **Using `.env.example`:** An `.env.example` file is provided to showcase the necessary environment variables. This file serves as a template.

   Example `.env.example` content:
   
   ```plaintext
   API_ID=1911744
   API_HASH=275a53e955llcDk6d980c222640f36add

   BOT_TOKEN=6605161404:AAHORGl295flKMbghmcGBQ1HDtAdp_VJjv00
   BOT_NAME=LotteryBot
   BOT_CHANNEL=LotteryChannel

   MANIFEST_URL=https://raw.githubusercontent.com/vyacheslavshv/lottery-bot-manifest/main/pytonconnect-manifest.json

   TS_PROJECT_DIR="../../TON/send-ton-coins"
   TS_SCRIPT_DIR="scripts/sendTon.ts"
   ```
   
2. **Creating `.env`:** Copy `.env.example` and rename it to `.env`. Replace the placeholders with your actual configuration details.

## Setting Up the TON Project

To run the required TypeScript scripts for blockchain interactions, you need to create a TON project using "blueprint" for example.

## Usage

The bot can be started with the following command:

```bash
python main.py
```

After starting, the bot will listen for commands on Telegram and perform actions based on its configuration and the commands received.

## Scheduled Tasks

Scheduled tasks for deleting old callback data and processing monthly withdrawals can be set up as cron jobs or using a scheduler in Python. Refer to the documentation of the scheduler you choose for setup instructions.