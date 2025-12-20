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
```

### Interpreter beállítása:
A projekt virtuális környezetet (`.venv`) használ. Fontos, hogy a PyCharm **ezt** az interpretert használja, különben a telepített csomagokat (pl. `requests`, `fastapi`) nem fogja felismerni.
Lépések:
1. **File → Settings → Python → Interpreter**
2. Kattints: **Add Interpreter**
3. Válaszd: **Add Local Interpreter**
4. Típus: **Virtualenv Environment**
5. Jelöld be: **Existing environment**
6. Tallózd ki: A projekt gyökérkönyvtárát \.venv\Scripts\python.exe
7. Azaz ne a Program Files vagy AppData python.exe-jét. 
8. OK -> várd meg, amíg a PyCharm szinkronizálja a környezetet

Szükség esetén a PyCharm felajánlja a `requirements.txt` csomagjainak telepítését — ezt engedélyezni kell.

###

### Indítás

Backend (FastAPI):

uvicorn backend.main:app --reload

Ez elindítja az API-t: http://127.0.0.1:8000

Swagger: http://127.0.0.1:8000/docs

###

### Frontend (Streamlit) indítása terminál ablakban:

streamlit run frontend/app.py


Ez megnyitja a böngészőt: http://localhost:8501

A Streamlit innen hívja a FastAPI végpontokat.
###

### Worker (automatizáció) – új terminál ablakban:

python scripts/worker.py

Ez generál “weekly top” riportot és elmenti a DB-be.
###

### Tesztek:

pytest -q
