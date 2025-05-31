# RIJF Schedule Maker

A simple Python web app that uses backtracking DFS to create schedules for the Rochester International Jazz Festival.

---

## Getting Started

1. **Requirements**
   - Python (latest version recommended)
   - Flask
   - BeautifulSoup4 (required only for `webscrape.py`)

2. **Setup**
   - Download or clone this repository.
   - To run the app:
     - Use Flask:  
       ```
       flask --app app run
       ```
     - Or run directly with Python:  
       ```
       python [app.py](http://_vscodecontentref_/0)
       ```
   - Open your browser and navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000). The app should be running!

---

## Changelog

## 5/30/25

#### `webscrape.py`
- Removed `requests` usage and webscraping capabilities.  
  RIJF now uses JavaScript to render their site, so scraping with only bs4/requests is no longer possible.
- Restructured to read from a `.html` source and create `artists.json` from that source.

#### `algorithm.py`
- Reworked `backtrack()` to only return a created schedule, raising a custom exception otherwise.
- `makeSchedule()` now catches this exception and returns `False` on failure.
- Added logic to allow a specified number of time slot overlaps (schedules can now accommodate concurrent show times).

#### `app.py` (Web UI)
- Added customization for max overlap.
- Updated general CSS to match the RIJF website more.
- Added color mapping for show names to increase schedule contrast.
- Added a "Shrink Table" control to compress unfilled time slots for readability.
- Added a "to top" button for easier navigation
- Verified CSS functionality in Edge.

#### Miscellaneous
- Added a `sources/` directory for better organization.

---