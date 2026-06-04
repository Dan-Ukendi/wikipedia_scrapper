# 🌍 Wikipedia Scraper

A Python pipeline that retrieves political leaders from a REST API and scrapes their biographical intro from Wikipedia — built as a pair programming project.

---

## 📖 Description

This project queries the [Country Leaders API](https://country-leaders.onrender.com/docs) to get a list of political leaders per country, then scrapes the first paragraph of each leader's Wikipedia page to build a structured JSON dataset.

The codebase is split into two independent modules:
- `api_client.py` — handles all communication with the REST API (cookie management, countries, leaders)
- `html_scraper.py` — handles Wikipedia HTML fetching, parsing, and text cleaning

Both are orchestrated by `main.py`.

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
    └── html_scraper.py
```

---

## ⚙️ Installation

**1. Clone the repository**
```bash
git clone https://github.com/VictorCourtois135/wikipedia-scraper.git
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
3. Scrape the first paragraph of each leader's Wikipedia page
4. Save the results to `leaders_data.json`

---

## 📦 Output

The script generates a `leaders_data.json` file structured like this:

```json
{
  "be": [
    {
      "id": "...",
      "first_name": "Alexander",
      "last_name": "De Croo",
      "birth_date": "...",
      "wikipedia_url": "https://en.wikipedia.org/wiki/Alexander_De_Croo",
      "bio": "Alexander De Croo is a Belgian liberal politician..."
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
| `refresh_cookie()` | Fetches a fresh session cookie |
| `get_countries()` | Returns a list of supported country codes |
| `get_leaders(country)` | Returns the list of leaders for a given country |

### `src/html_scraper.py` — `WikipediaScraper`

Handles Wikipedia page fetching and parsing.

| Method | Description |
|---|---|
| `fetch_html(url)` | Downloads raw HTML from a URL with error handling |
| `get_first_paragraph(html)` | Extracts the first biographical paragraph |
| `clean_text(text)` | Strips citation brackets and unwanted characters |
| `to_json_file(filepath)` | Saves the leaders dataset to a JSON file |

---

## 🛠️ Tech Stack

- [Python 3](https://www.python.org/)
- [requests](https://docs.python-requests.org/) — HTTP calls
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) — HTML parsing

---

## 👥 Authors

- **Victor** — API Client module
- **Dan** — HTML Scraper module