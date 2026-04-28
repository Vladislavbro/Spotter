# Spotter — Wildberries Marketplace Analytics

End-to-end pet project around Wildberries: a daily scraper, NLP-based product clustering, a MongoDB store, a Telegram bot, and a small web frontend. Live at [spotter.fun](https://spotter.fun).

## What it does

- **Scrapes Wildberries every day** — products, sizes, sales, categories — through a rotating proxy pool.
- **Tracks day-over-day sales deltas** per SKU (`day_sales_t - day_sales_{t-1}`) to surface fast-moving items.
- **Clusters product titles in Russian** to group near-duplicate listings inside each marketplace category.
- **Serves the analytics** through a Telegram bot (`@GoodsHunter_bot`) and a web UI.

## NLP pipeline (the ML-relevant part)

Implemented in `clustering.py`. For each product title:

1. **Normalisation** — lowercasing, regex cleanup, lemmatisation with `pymystem3`, Russian stopword and punctuation removal.
2. **Linguistic parsing** with spaCy (`ru_core_news_md`):
   - extract the **root noun** of the title via dependency parsing (falls back to `nsubj` when the root isn't a noun);
   - extract **descriptive features** — all `ADJ` tokens — as the product's attribute set;
   - capture **named entities** (e.g. brand) when present.
3. **Vectorisation** — spaCy document vectors (300d) per cleaned title.
4. **Clustering inside each marketplace category** — `KMeans(n_clusters=15)` per category, with DBSCAN / OPTICS / Birch experimented as alternatives. Results saved as per-cluster CSVs for inspection.

The aim: collapse near-duplicate listings inside a category so that aggregated sales metrics are comparable across competing SKUs.

## Components

| Module | Role |
|---|---|
| `parse.py` | Wildberries scraper — products, sizes, sales, categories. |
| `proxies.py` | Rotating proxy pool. |
| `models.py` | MongoDB schemas (`mongoengine`): `Products`, `Categories`, `Users`. |
| `clustering.py` | NLP pre-processing, spaCy vectorisation, per-category clustering. |
| `sales.py` | Sales-delta computation for daily reports. |
| `bot.py` | Telegram bot (python-telegram-bot, polling, persistent state). |
| `server.py` | HTTP API for the web frontend. |
| `frontend/` | Web UI. |
| `ecosystem.config.js`, `check.sh` | PM2 deployment configuration. |

## Stack

Python · spaCy (ru_core_news_md) · pymystem3 · NLTK · scikit-learn · pandas · NumPy · MongoDB (mongoengine) · python-telegram-bot · PM2

## Repository status

Personal project from 2022 (refreshed in 2025). The `master` branch holds the current code; the deployment lives at [spotter.fun](https://spotter.fun).

## Setup

```bash
pip install -r requirements.txt
python -m spacy download ru_core_news_md
python -c "import nltk; nltk.download('stopwords')"
```

Environment variables required:

```
TELEGRAM_BOT_TOKEN=...
MONGO_URI=...
```

Run components individually:

```bash
python parse.py        # scraper loop
python clustering.py   # build product clusters per category
python bot.py          # Telegram bot
python server.py       # HTTP API
```
