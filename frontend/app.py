from __future__ import annotations

import os
import requests
import streamlit as st
import matplotlib.pyplot as plt

API_BASE = os.getenv("BACKEND_BASE_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Travel Wishlist", layout="wide")
st.title("Travel Wishlist")

tab1, tab2, tab3 = st.tabs(["Search", "Wishlist", "Stats"])

with tab1:
    st.subheader("Search POI (city + optional query)")
    city = st.text_input("City", value="Budapest")
    query = st.text_input("Query (optional)", value="museum")

    if st.button("Search"):
        try:
            r = requests.get(f"{API_BASE}/places/search",
                             params={"city": city, "query": query},
                             timeout=60)
            r.raise_for_status()
            st.session_state["results"] = r.json().get("results", [])
        except Exception as e:
            st.error(f"Search failed: {e}")
            st.session_state["results"] = []

    results = st.session_state.get("results", [])
    if results:
        st.caption(f"Found {len(results)} result(s).")

    for i, item in enumerate(results):
        cols = st.columns([5, 2, 2])
        cols[0].write(
            f"**{item['name']}**  \nPOI: `{item['poi_id']}`  \n{item.get('address') or ''}"
        )
        tag = cols[1].selectbox("Tag", ["food", "culture", "nature"], key=f"tag_{i}")
        if cols[2].button("Add to wishlist", key=f"add_{i}"):
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
                st.success("Added!")
            except Exception as e:
                st.error(f"Add failed: {e}")

with tab2:
    st.subheader("Wishlist")
    tag_filter = st.selectbox("Filter by tag", ["(all)", "food", "culture", "nature"])
    params = {}
    if tag_filter != "(all)":
        params["tag"] = tag_filter

    try:
        r = requests.get(f"{API_BASE}/wishlist", params=params, timeout=20)
        r.raise_for_status()
        items = r.json()
    except Exception as e:
        st.error(f"Load wishlist failed: {e}")
        items = []

    if not items:
        st.info("No items yet. Add some from Search.")
    for it in items:
        cols = st.columns([6, 2])
        cols[0].write(f"**{it['name']}** — {it['city']} — tag: `{it['tag']}`")
        if cols[1].button("Delete", key=f"del_{it['id']}"):
            try:
                dr = requests.delete(f"{API_BASE}/wishlist/{it['id']}", timeout=20)
                dr.raise_for_status()
                st.rerun()
            except Exception as e:
                st.error(f"Delete failed: {e}")

with tab3:
    st.subheader("Stats (visualization)")

    try:
        r = requests.get(f"{API_BASE}/stats/top-tags", timeout=20)
        r.raise_for_status()
        top_tags = r.json().get("top_tags", [])
    except Exception as e:
        st.error(f"Stats load failed: {e}")
        top_tags = []

    if top_tags:
        labels = [x["tag"] for x in top_tags]
        values = [x["count"] for x in top_tags]
        fig = plt.figure()
        plt.bar(labels, values)
        plt.title("Top tags")
        st.pyplot(fig)
    else:
        st.info("No stats yet (add wishlist items first).")

    st.subheader("Weekly top wishlisted")
    try:
        w = requests.get(f"{API_BASE}/stats/weekly-top", timeout=20).json()
        st.write("Generated at:", w.get("generated_at"))
        st.write(w.get("items", []))
    except Exception as e:
        st.error(f"Weekly report load failed: {e}")
