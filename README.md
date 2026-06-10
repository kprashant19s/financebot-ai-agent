# FinanceBot — Autonomous Data Insights Agent

An AI-powered agent that takes plain English questions about a finance database, automatically generates SQL queries, executes them safely, and produces interactive visualizations — end to end, no manual SQL required.

---

## What it does

You ask a question like:
> "Which category had the highest spending in October 2024?"

The agent:
1. Reads your database schema automatically
2. Sends the question + schema to an LLM (Groq / LLaMA 3)
3. LLM generates the correct SQL query
4. A safety validator checks the SQL before execution
5. MySQL executes the query
6. Results are displayed as a table + interactive Plotly chart

---

## Example questions it can answer

- "What are the top 3 expense categories by total amount?"
- "Compare budget vs actual spending for groceries"
- "Show total expenses by month for 2024"
- "Which month had the highest savings in 2024?"
- "What percentage of my income did I spend on dining out in February?"
- "Show me the top 5 largest transactions"
- "Which category overspent the budget in October 2024?"

---

## Tech stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Agent framework | LangChain |
| LLM | Groq API (LLaMA 3.3 70B) |
| Database | MySQL 8.0 |
| ORM / Safety | SQLAlchemy + custom validator |
| Visualization | Plotly |
| Config | python-dotenv |

---

## Project structure

```
financebot/
├── .env                        # API keys and DB config (never commit)
├── main.py                     # Entry point
├── requirements.txt            # Python dependencies
├── agent/
│   ├── agent.py                # LLM + SQL pipeline + retry logic
│   └── prompts.py              # System and human prompts
├── tools/
│   ├── schema_reader.py        # Auto-reads MySQL table structure
│   ├── sql_validator.py        # Blocks dangerous SQL keywords
│   └── sql_executor.py         # Runs queries safely via SQLAlchemy
├── viz/
│   └── chart_generator.py      # Auto-selects chart type from data shape
└── database/
    ├── schema.sql              # Creates 5 finance tables
    └── seed_data.sql           # 137 transactions across 12 months
```

---

## Setup instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-username/financebot.git
cd financebot
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the root folder:
```
GROQ_API_KEY=your_groq_api_key
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=financebot
```

### 5. Set up MySQL database
```bash
mysql -u root -p -e "CREATE DATABASE financebot;"
mysql -u root -p financebot < database/schema.sql
mysql -u root -p financebot < database/seed_data.sql
```

### 6. Run the agent
```bash
python3 main.py
```

---

## Safety features

- **SELECT only** — the validator blocks any query containing DROP, DELETE, INSERT, UPDATE, TRUNCATE, ALTER
- **Read-only MySQL user** recommended for production
- **Relevance check** — irrelevant questions are rejected before SQL generation
- **Retry logic** — automatically retries up to 2 times if SQL execution fails
- **Row limit** — all queries are limited to 500 rows maximum

---

## Dataset

The sample dataset simulates a personal finance tracker for an individual in India:
- 4 accounts: HDFC Checking, HDFC Savings, ICICI Credit Card, Zerodha Investment
- 10 categories: Salary, Freelance, Groceries, Rent, Utilities, Dining Out, Transportation, Entertainment, Healthcare, Shopping
- 137 transactions across January — December 2024
- Monthly budgets for all expense categories
- Realistic spending patterns including Diwali (October) and year-end spikes

---

## Built by

Prashant Singh — Data / Business Analyst