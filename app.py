import streamlit as st
import json
import os

DATA_FILE = "gildings.json"
IMAGE_FOLDER = "images"


@st.cache_data
def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def tokenize(text):
    return [
        token.strip().lower()
        for token in text.split()
        if token.strip()
    ]


def matches_field_list(field_list, tokens):
    if not tokens:
        return True

    searchable = " ".join(field_list).lower() if field_list else ""
    return all(token in searchable for token in tokens)


def main():
    st.set_page_config(
        page_title="Gilding Database",
        layout="wide"
    )

    # Compact wiki-like styling
    st.markdown("""
    <style>

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    h1 {
        font-size: 28px !important;
        margin-bottom: 0.5rem !important;
    }

    h2 {
        font-size: 20px !important;
        margin-top: 0.5rem !important;
        margin-bottom: 0.25rem !important;
    }

    h3 {
        font-size: 16px !important;
        margin-top: 0.25rem !important;
        margin-bottom: 0.25rem !important;
    }

    div[data-testid="stVerticalBlock"] {
        gap: 0.55rem;
    }

    ul {
        margin-top: 0px !important;
        margin-bottom: 4px !important;
        line-height: 1.2;
    }

    hr {
        margin: 6px 0px;
    }

    img {
        max-width: 46px !important;
        height: auto !important;
    }

    p {
        margin: 0px !important;
        line-height: 1.4;
    }

    </style>
    """, unsafe_allow_html=True)

    st.title("Gilding Database Search")

    data = load_data()

    # --- Search fields ---
    search_name = st.text_input("Search item name / category")
    search_gilds = st.text_input("Search gilding stats (gilds)")
    search_attributes = st.text_input("Search success attributes")

    name_tokens = tokenize(search_name)
    gild_tokens = tokenize(search_gilds)
    attr_tokens = tokenize(search_attributes)

    # --- Filtering ---
    filtered_items = []

    for item in data:

        # Name / category filter
        if name_tokens:
            searchable_text = " ".join([
                item.get("name", ""),
                item.get("category", "")
            ]).lower()

            if not all(token in searchable_text for token in name_tokens):
                continue

        # Gilds filter
        if not matches_field_list(item.get("gilds", []), gild_tokens):
            continue

        # Success attributes filter
        if not matches_field_list(item.get("success_attributes", []), attr_tokens):
            continue

        filtered_items.append(item)

    st.write(f"Found {len(filtered_items)} items")

    # --- Rendering ---
    for item in filtered_items:

        cols = st.columns([0.4, 3])

        # Image + name column
        with cols[0]:
            image_file = item.get("image")

            if image_file:
                image_path = os.path.join(IMAGE_FOLDER, image_file)

                if os.path.exists(image_path):
                    st.image(image_path, width=46)

            name = item.get("name", "Unknown")
            wiki_name = name.replace(" ", "_")
            wiki_url = f"https://ringofbrodgar.com/wiki/{wiki_name}"

            st.markdown(f"**[{name}]({wiki_url})**")


        # Stats column
        with cols[1]:

            # ✅ Show full percentage string directly
            if item.get("gild_chance"):
                st.markdown(f"**Chance:** {item['gild_chance']}")

            if item.get("gilds"):
                st.markdown("**Gilds:**")
                for g in item["gilds"]:
                    st.markdown(f"- {g}")

            if item.get("success_attributes"):
                st.markdown("**Attributes:**")
                for a in item["success_attributes"]:
                    st.markdown(f"- {a}")

        st.markdown("<hr>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()