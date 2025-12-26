from __future__ import annotations

import os

import matplotlib.pyplot as plt
import requests
import streamlit as st


API_BASE = st.secrets.get(
    "BACKEND_BASE_URL",
    os.getenv("BACKEND_BASE_URL", "http://127.0.0.1:8000"),
)

st.set_page_config(page_title="Travel Wishlist", layout="wide")
st.title("Travel Wishlist – Kívánságlista")

# UI -> belső tag érték mapping (DB-ben marad: food/culture/nature)
TAG_LABEL_TO_VALUE = {
    "Étel (food)": "food",
    "Kultúra (culture)": "culture",
    "Természet (nature)": "nature",
}
TAG_VALUE_TO_HU = {
    "food": "Étel",
    "culture": "Kultúra",
    "nature": "Természet",
}

tab1, tab2, tab3 = st.tabs(["Keresés", "Kívánságlista", "Statisztika"])

# ---------------------------
# TAB 1: Keresés
# ---------------------------
with tab1:
    st.subheader("POI keresés (város + opcionális keresőkifejezés)")
    city = st.text_input("Város", value="Budapest")
    query = st.text_input("Keresőkifejezés (opcionális)", value="museum")

    if st.button("Keresés"):
        try:
            r = requests.get(
                f"{API_BASE}/places/search",
                params={"city": city, "query": query},
                timeout=60,
            )
            r.raise_for_status()
            st.session_state["results"] = r.json().get("results", [])
        except Exception as e:
            st.error(f"Keresés sikertelen: {e}")
            st.session_state["results"] = []

    results = st.session_state.get("results", [])
    if results:
        st.caption(f"{len(results)} találat.")

    for i, item in enumerate(results):
        cols = st.columns([5, 2, 2])
        cols[0].write(
            f"**{item['name']}**  \n"
            f"POI: `{item['poi_id']}`  \n"
            f"{item.get('address') or ''}"
        )

        tag_label = cols[1].selectbox(
            "Címke",
            list(TAG_LABEL_TO_VALUE.keys()),
            key=f"tag_{i}",
        )
        tag = TAG_LABEL_TO_VALUE[tag_label]

        if cols[2].button("Hozzáadás", key=f"add_{i}"):
            payload = {
                "city": city,
                "poi_id": item["poi_id"],
                "name": item["name"],
                "address": item.get("address"),
                "tag": tag,
            }
            try:
                pr = requests.post(f"{API_BASE}/wishlist", json=payload, timeout=20)
                pr.raise_for_status()
                st.success("Sikeresen hozzáadva a kívánságlistához!")
            except Exception as e:
                st.error(f"Hozzáadás sikertelen: {e}")

# ---------------------------
# TAB 2: Kívánságlista
# ---------------------------
with tab2:
    st.subheader("Kívánságlista")

    tag_filter_label = st.selectbox(
        "Szűrés címke alapján",
        ["(összes)", "Étel (food)", "Kultúra (culture)", "Természet (nature)"],
    )

    params = {}
    if tag_filter_label != "(összes)":
        params["tag"] = TAG_LABEL_TO_VALUE[tag_filter_label]

    try:
        r = requests.get(f"{API_BASE}/wishlist", params=params, timeout=20)
        r.raise_for_status()
        items = r.json()
    except Exception as e:
        st.error(f"Kívánságlista betöltése sikertelen: {e}")
        items = []

    if not items:
        st.info("Még nincs mentett elem. Adj hozzá elemeket a Keresés fülön.")
    else:
        st.caption(f"{len(items)} elem a listában.")

    for it in items:
        cols = st.columns([6, 2])
        hu_tag = TAG_VALUE_TO_HU.get(it["tag"], it["tag"])
        cols[0].write(f"**{it['name']}** — {it['city']} — címke: `{hu_tag}`")

        if cols[1].button("Törlés", key=f"del_{it['id']}"):
            try:
                dr = requests.delete(f"{API_BASE}/wishlist/{it['id']}", timeout=20)
                dr.raise_for_status()
                st.rerun()
            except Exception as e:
                st.error(f"Törlés sikertelen: {e}")

# ---------------------------
# TAB 3: Statisztika
# ---------------------------
with tab3:
    st.subheader("Statisztika (vizualizáció)")

    try:
        r = requests.get(f"{API_BASE}/stats/top-tags", timeout=20)
        r.raise_for_status()
        top_tags = r.json().get("top_tags", [])
    except Exception as e:
        st.error(f"Statisztika betöltése sikertelen: {e}")
        top_tags = []

    if top_tags:
        labels = [TAG_VALUE_TO_HU.get(x["tag"], x["tag"]) for x in top_tags]
        values = [x["count"] for x in top_tags]
        fig = plt.figure()
        plt.bar(labels, values)
        plt.title("Top címkék")
        st.pyplot(fig)
    else:
        st.info("Még nincs statisztika (előbb adj hozzá elemeket a kívánságlistához).")

    st.subheader("Heti top kívánságlista elemek (utolsó riport)")
    try:
        w = requests.get(f"{API_BASE}/stats/weekly-top", timeout=20).json()
        gen_at = w.get("generated_at")
        st.write("Generálva:", gen_at if gen_at else "Nincs még generált riport.")
        st.write(w.get("items", []))
    except Exception as e:
        st.error(f"Heti riport betöltése sikertelen: {e}")
