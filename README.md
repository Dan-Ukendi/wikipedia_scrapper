# 🌍 Wikipedia Scraper

A multithreaded Python pipeline that retrieves political leaders from a REST API and scrapes their biographical intro from Wikipedia — built as a pair programming project.

---

## 📖 Description

This project queries the [Country Leaders API](https://country-leaders.onrender.com/docs) to get a list of political leaders per country, then scrapes the first paragraph of each leader's Wikipedia page to build a structured JSON dataset.

The scraping is parallelised with Python's `threading` module: one thread is spawned per country, allowing all Wikipedia pages to be fetched concurrently.

The codebase is split into three files:
- `src/api_client.py` — handles all communication with the REST API (cookie management, countries, leaders)
- `src/HTML_Scraper.py` — handles Wikipedia HTML fetching, parsing, text cleaning, and JSON export
- `main.py` — orchestrates the full pipeline using multithreading

---

## 🗂️ Project Structure

```
wikipedia-scraper/
├── .gitignore
├── README.md
├── requirements.txt
├── main.py
├── dev/
│   ├── student_a_sandbox.ipynb
│   └── student_b_sandbox.ipynb
└── src/
    ├── __init__.py
    ├── api_client.py
    └── HTML_Scraper.py
```

---

## ⚙️ Installation

**1. Clone the repository**
```bash
git clone https://github.com/<your-username>/wikipedia-scraper.git
cd wikipedia-scraper
```

**2. Create and activate a virtual environment**
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

Run the full pipeline:
```bash
python main.py
```

This will:
1. Fetch the list of available countries from the API
2. Retrieve all political leaders for each country
3. Spawn one thread per country to scrape Wikipedia bios in parallel
4. Save the enriched dataset to `leaders.json`

---

## 📦 Output

The script generates a `leaders.json` file structured like this:

```json
{
  "be": [
    {
      "id": "...",
      "first_name": "Alexander",
      "last_name": "De Croo",
      "birth_date": "1975-...",
      "wikipedia_url": "https://en.wikipedia.org/wiki/Alexander_De_Croo",
      "Bio": "Alexander De Croo is a Belgian liberal politician..."
    }
  ]
}
```

---

## 🧱 Modules

### `src/api_client.py` — `CountryLeadersAPI`

Handles all interactions with the Country Leaders REST API.

| Method | Description |
|---|---|
| `refresh_cookies()` | Fetches a fresh session cookie from the API |
| `get_countries()` | Returns a list of supported country codes |
| `get_leaders()` | Returns all leaders grouped by country code |

### `src/HTML_Scraper.py`

| Class / Function | Description |
|---|---|
| `create_session` | Creates a `requests.Session` with a Wikipedia-compliant User-Agent |
| `clean(text)` | Strips citation brackets, symbols, and extra whitespace from text |
| `date(url, leaders)` | Looks up a year/name anchor used to identify the right paragraph |
| `wikipedia_scrapper.fetch_url(url)` | Downloads raw HTML with error handling |
| `wikipedia_scrapper.get_first_paragraphe(url, leaders)` | Extracts and cleans the first biographical paragraph |
| `wikipedia_scrapper.save(leaders, filename)` | Serialises the dataset to a JSON file |

### `main.py` — `Search` thread + `main()`

| Component | Description |
|---|---|
| `Search(Thread)` | Worker thread — scrapes all leaders for one country |
| `Search.lock` | Class-level `RLock` protecting concurrent writes to the shared dict |
| `main()` | Initialises modules, spawns threads, waits for completion, saves output |

---

## ⚡ Multithreading

Each country gets its own `Search` thread. Threads run concurrently, so Wikipedia pages for all countries are fetched at the same time instead of one by one. A shared `RLock` ensures that writing results back to the dictionary is thread-safe.

A 100 ms sleep between requests inside each thread avoids hammering Wikipedia's servers.

---

## 🛠️ Tech Stack

- [Python 3](https://www.python.org/)
- [requests](https://docs.python-requests.org/) — HTTP calls
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) — HTML parsing
- [threading](https://docs.python.org/3/library/threading.html) — parallel scraping
- [re](https://docs.python.org/3/library/re.html) — text cleaning with regex

---

## 👥 Authors

- **Victor Courtois** — API Client module
- **Dan Ukendi** — HTML Scraper module