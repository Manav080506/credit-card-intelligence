# AI Credit Card Data Pipeline Architecture

Goal:
Continuously collect, validate, and update real credit card reward data.

Pipeline:

Sources:
- bank websites
- fintech comparison sites
- card benefit PDFs

Workers:

1. `card_discovery_worker`
finds new credit cards

2. `card_scraper_worker`
scrapes card product pages

3. `llm_card_parser`
extracts reward structure

4. `reward_rules_validator_worker`
ensures reward logic correctness

5. `reward_refresh_worker`
detects reward changes

6. `change_history_worker`
tracks reward changes over time

7. `scheduler`
runs workers automatically

Flow:

URL list
-> scraper
-> raw text
-> llm parser
-> structured JSON
-> validator
-> dataset update
-> optimizer uses updated data

Update frequency:

daily:
check reward changes

weekly:
re-parse all cards

monthly:
manual verification

Output dataset location:

- `backend/data/cards/`
- `backend/data/cards_metadata_layer.json`
- `backend/data/cards_optimizer_layer.json`
