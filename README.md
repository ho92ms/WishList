# WishList (Travel Wishlist)

A **Travel Wishlist** egy Python alapú webalkalmazás, amely lehetővé teszi városokhoz tartozó POI-k (látnivalók, helyek) keresését, valamint ezek wishlist-be mentését.  
A rendszer **FastAPI backendből**, **Streamlit frontendből**, adatbázisból és statisztikai funkciókból áll.

---

## Fő funkciók

- Város + keresőkifejezés alapján POI-k keresése  
  (külső API lánc: **Geocoding + Overpass / OpenStreetMap**)
- Wishlist CRUD műveletek:
  - létrehozás
  - listázás
  - törlés
- Címkézés: `food`, `culture`, `nature`
- Statisztikák:
  - top címkék
  - top városok
- Automatizációs logika:
  - heti top wishlisted elemek számítása (DB-be menthető)
- Tesztelés:
  - `pytest`
  - parametrizált teszt is szerepel

---

## Live (Deploy)

- **Frontend (Streamlit Cloud):**  
  https://nemdavid.streamlit.app/

- **Backend (Render):**  
  https://wishlist-calv.onrender.com/

- **Swagger / API dokumentáció:**  
  https://wishlist-calv.onrender.com/docs

---

## Követelmények

- Python **3.10+** (ajánlott)
- Virtuális környezet (`venv`)
- `.env` konfigurációs fájl (példa: `.env.example`)

---

## Telepítés

### Virtuális környezet létrehozása

```bash
python -m venv .venv
```

### Virtuális környezet aktiválása (Windows)

```bash
.\.venv\Scripts\activate
```

### Csomagok telepítése

```bash
pip install -r requirements.txt
```

### PyCharm interpreter beállítása (fontos!)

A projekt virtuális környezetet (`.venv`) használ.  
Ha a PyCharm nem ezt az interpretert használja, a csomagok (pl. `requests`, `fastapi`) pirossal lesznek aláhúzva.

**Lépések PyCharm-ban:**

1. **File** → **Settings** → **Python** → **Interpreter**
2. **Add Interpreter**
3. **Add Local Interpreter**
4. **Típus:** Virtualenv Environment
5. **Jelöljük be:** Existing environment
6. **Tallózzuk ki:**  
   `<projekt_könyvtár>\.venv\Scripts\python.exe`
7. **OK**, majd várjuk meg a szinkronizálást

A PyCharm szükség esetén felajánlja a `requirements.txt` csomagjainak telepítését – ezt engedélyezni kell.

### Környezeti változók (.env)

A projekt gyökerében szükséges egy `.env` fájl.  
Kiindulásként használhato a `.env.example` fájl.

**Megjegyzés geocodinghoz:**
- Lokális futtatásnál használható a **Nominatim**
- Cloud környezetben (Render) stabilabb az **Open-Meteo Geocoding**, ezért ott ez van használva

---

## Indítás

### Backend (FastAPI)

```bash
uvicorn backend.main:app --reload
```

- **API:** http://127.0.0.1:8000
- **Swagger:** http://127.0.0.1:8000/docs

### Frontend (Streamlit)

Új terminál ablakban:

```bash
streamlit run frontend/app.py
```

- **Böngésző:** http://localhost:8501

A Streamlit alkalmazás innen hívja a FastAPI backend végpontjait.

### Worker (automatizációs logika)

Új terminál ablakban:

```bash
python scripts/worker.py
```

Ez kiszámítja a heti top wishlist elemeket és elmenti azokat az adatbázisba.

---

## Tesztek futtatása

```bash
pytest -q