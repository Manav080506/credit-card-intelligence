# Copilot Prompt Pack

## Dataset Generator Prompt

Generate JSON dataset of Indian credit cards using schema:

- id
- bank
- annual_fee
- reward_rules
- benefits
- tags

Ensure realistic reward ranges:

- 1% to 5% cashback
- 2 to 10 lounge visits
- 0 to 10000 annual fee

## Scraper Worker Prompt

Create Python scraper architecture with class `CardScraper` and methods:

- fetch_html
- parse_rewards
- parse_fees
- parse_benefits
- normalize_data
- store_postgres

Requirements:

- Modular adapters per website
- Handle missing fields safely
- Normalize percentages to decimals

## ML Model Prompt

Create ML pipeline:

Input:

- monthly spend categories

Output:

- top 3 card recommendations

Features:

- spend ratios
- spend variance
- card annual fee
- reward rate

Model:

- RandomForestRegressor

Return:

- recommendations and confidence score

## Explanation Engine Prompt

Generate explanation text for recommendation using conditions:

- high online spend
- travel heavy user
- balanced spending

Output:

- short bullet insights
- confidence score
- optimization opportunity

## Architecture Prompt

Design fintech AI SaaS architecture with:

- React frontend
- FastAPI AI layer
- Postgres DB
- Redis cache
- worker pipeline
- card dataset ingestion

Explain data flow clearly.

## Generate New Optimizer Feature Prompt

Add feature engineering function:

- calculate spend ratios
- calculate spend entropy
- detect dominant category
- return structured features dictionary

## Generate New Worker Prompt

Create worker `CardScraperWorker` with methods:

- fetch_html
- parse_card_data
- normalize_reward_rates
- store_postgres
- log_changes

Add retry logic for transient failures.

## Generate New ML Model Prompt

Create ML recommendation model.

Input:

- user spend vector

Output:

- top 3 cards
- confidence score
- feature importance

Use sklearn `RandomForest`.

## Generate API Endpoint Prompt

Create FastAPI route:

- `POST /compare-cards`

Input:

- monthly spend

Output:

- ranked cards list
- monthly reward estimate
- yearly reward estimate
