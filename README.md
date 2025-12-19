# WishList (Travel Wishlist)

Travel Wishlist – FastAPI backend + Streamlit frontend alkalmazás városokhoz tartozó POI-k (látnivalók) keresésére és wishlist-be mentésére.

## Funkciók
- Város + keresőkifejezés alapján POI-k keresése (OSM: Nominatim + Overpass)
- Wishlist CRUD: létrehozás, listázás, törlés
- Címkék: food / culture / nature
- Statisztika: top címkék, top városok
- Automatizáció: heti top wishlisted elemek generálása (SQLite-ba mentve)
- Tesztek: pytest (3 teszt, 1 parametrizált)

## Követelmények
- Python 3.10+ ajánlott
- venv használata
- `.env` szükséges (ld. alább)

## Telepítés
```bash
python -m venv .venv
# Windows:
.\.venv\Scripts\activate
pip install -r requirements.txt
