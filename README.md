# Money Tracker Bot

A Telegram bot for tracking personal expenses with multi-currency support (UAH/USD) and Excel report generation.

## Table of Contents
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Bot Commands](#bot-commands)
- [Database Schema](#database-schema)
- [Security](#security)
- [Error Handling](#error-handling)
- [Deployment](#deployment)
- [Dependencies](#dependencies)
- [Future Plans](#future-plans)

## Architecture

The project consists of two main components:

### Backend API
- **Framework**: FastAPI
- **Database**: SQLite
- **ORM**: SQLAlchemy
- **Currency Rates**: Fetched from National Bank of Ukraine

### Telegram Bot
- **Framework**: aiogram 3.x
- **States**: FSM for handling user input
- **API Client**: Async client for backend communication

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/money_tracker.git
cd money_tracker
```

2. Create `.env` file with the following variables:
```
BOT_TOKEN=your_bot_token
API_SECRET_KEY=your_secret_key
ADMIN_CHAT_ID=your_admin_chat_id
DATABASE_URL=sqlite:////data/expenses.db
```

3. Run the project using Docker:
```bash
docker-compose up --build
```

## Configuration

### Environment Variables
- `BOT_TOKEN`: Your Telegram bot token (get from @BotFather)
- `API_SECRET_KEY`: Secret key for API authentication
- `ADMIN_CHAT_ID`: Admin chat ID for notifications
- `DATABASE_URL`: Database connection URL

## Usage

### Main Features
1. Track expenses in UAH and USD
2. Generate Excel reports
3. Edit and delete expenses
4. Filter expenses by period

### Key Features
- Automatic USD conversion using NBU rates
- User data protection
- User-friendly Telegram interface
- Detailed reports with totals

## API Endpoints

### 1. Create Expense
```http
POST /expenses/
Authorization: X-API-Key your_secret_key
Content-Type: application/json

{
    "user_id": 123456789,
    "name": "Groceries",
    "date": "2024-04-05",
    "amount_uah": 1000.00
}
```

### 2. Get Expenses
```http
GET /expenses/?user_id=123456789&start_date=2024-04-01&end_date=2024-04-30
Authorization: X-API-Key your_secret_key
```

### 3. Update Expense
```http
PUT /expenses/1
Authorization: X-API-Key your_secret_key
Content-Type: application/json

{
    "user_id": 123456789,
    "name": "Groceries",
    "date": "2024-04-05",
    "amount_uah": 1200.00
}
```

### 4. Delete Expense
```http
DELETE /expenses/1?user_id=123456789
Authorization: X-API-Key your_secret_key
```

### 5. Generate Report
```http
GET /expenses/report/?user_id=123456789&start_date=2024-04-01&end_date=2024-04-30
Authorization: X-API-Key your_secret_key
```

## Bot Commands

### Add Expense
1. Click "Add Expense ➕"
2. Enter expense name
3. Enter date (YYYY-MM-DD or YYYY.MM.DD)
4. Enter amount in UAH

### View Report
1. Click "Report 📊"
2. Enter start date (or /skip)
3. Enter end date (or /skip)
4. Receive Excel file with expenses

### Edit Expense
1. Click "Edit Expense 📝"
2. Get list of expenses
3. Enter expense ID to edit
4. Enter new name
5. Enter new amount

### Delete Expense
1. Click "Delete Expense 🗑"
2. Get list of expenses
3. Enter expense ID to delete

## Database Schema

```sql
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    date DATE NOT NULL,
    amount_uah FLOAT NOT NULL,
    amount_usd FLOAT NOT NULL,
    user_id INTEGER NOT NULL
);
```

## Security

1. **API Authentication**
   - All API requests require secret key
   - Key passed via X-API-Key header

2. **User Isolation**
   - Users can only see their own expenses
   - user_id verification on each request

3. **Input Validation**
   - All input data validation
   - Date format validation
   - Numeric value validation

## Error Handling

1. **Date Validation**
   - Support for YYYY-MM-DD and YYYY.MM.DD formats
   - Date correctness validation

2. **Expense Verification**
   - No expenses found messages
   - Non-existent ID handling

3. **Network Error Handling**
   - Currency rate fallback
   - Retry attempts on errors

## Deployment

### Local Deployment
```bash
# Install dependencies
pip install -r backend/requirements.txt
pip install -r bot/requirements.txt

# Run backend
cd backend
uvicorn app.main:app --reload

# Run bot
cd ../bot
python main.py
```

### Docker Deployment
```bash
docker-compose up --build
```

## Dependencies

### Backend
```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.2
requests==2.31.0
beautifulsoup4==4.12.2
xlsxwriter==3.1.9
python-multipart==0.0.6
python-dotenv==1.0.0
```

### Bot
```
aiogram==3.3.0
python-dotenv==1.0.0
aiohttp==3.9.1
```

## Future Plans

1. **Functionality**
   - [ ] Add expense categories
   - [ ] Implement budgeting
   - [ ] Add expense charts
   - [ ] Implement recurring expenses
   - [ ] Add export to other formats

2. **Interface**
   - [ ] Implement multi-language support
   - [ ] Add web interface
   - [ ] Improve bot UX/UI

3. **Social Features**
   - [ ] Implement shared expenses
   - [ ] Add expense templates
   - [ ] Implement recommendations

4. **Analytics**
   - [ ] Add detailed expense analytics
   - [ ] Implement forecasting
   - [ ] Add period comparison

5. **Integrations**
   - [ ] Add support for more currencies
   - [ ] Integrate with banking APIs
   - [ ] Add export to accounting systems 