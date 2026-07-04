import streamlit as st
from engine.anagram import generate_anagrams_fast
from engine.model import MarkovModel
from collections import Counter

st.set_page_config(page_title="Style Anagram Engine", layout="wide")

st.title("🧬 Style Anagram Engine")

word = st.text_input("Wort eingeben", "markuseckel")

style = st.selectbox(
    "Stil",
    ["medieval", "fantasy", "modern", "scifi"]
)

top_n = st.slider("Top Ergebnisse", 10, 200, 50)


@st.cache_resource
def load_model(style):
    model = MarkovModel()
    model.load(f"models/{style}.json")
    return model


model = load_model(style)


def score(word):
    return model.probability(word)


if st.button("Generate"):
    target = Counter(word)
    results = []

    with st.spinner("Berechne Anagramme..."):
        for perm in generate_anagrams_fast(word):
            if Counter(perm) != target:
                continue

            results.append((score(perm), perm))

    results.sort(reverse=True)

    st.subheader("Ergebnisse")

    for s, w in results[:top_n]:
        st.markdown(f"**{w}**  \n`{s:.8f}`")