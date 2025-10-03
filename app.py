import io
import base64
import streamlit as st
import pandas as pd

st.set_page_config(page_title="NARIA.app — R-Group Variant Generator (Demo)", layout="wide")

st.title("R‑Group Variant Generator (Demo)")
st.caption("Enter a scaffold with attachment points [*:1], [*:2], [*:3] and substituents with the same labels (e.g., [*:1]C).")

# ---------- Placeholder Chemistry Logic ----------
def build_placeholder_molecule(scaffold_smiles, rsubs):
    parts = [scaffold_smiles]
    for mapnum, s in rsubs.items():
        s = (s or "").strip()
        if s:
            parts.append(f"R{mapnum}: {s}")
    return " + ".join(parts)

def smiles_download_button(smiles, filename="molecule.smiles"):
    b64 = base64.b64encode(smiles.encode("utf-8")).decode()
    href = f'<a download="{filename}" href="data:text/plain;base64,{b64}">Download SMILES</a>'
    st.markdown(href, unsafe_allow_html=True)

# ---------- UI ----------
st.subheader("Inputs")

col1, col2 = st.columns([1,1])
with col1:
    scaffold = st.text_input(
        "Base Scaffold (SMILES with anchors)",
        value="c1cc([*:1])ccc1[*:2]",
        help="Example: c1cc([*:1])ccc1[*:2] (para-disubstituted benzene with two anchors)"
    )
    st.markdown(
        "**Tip:** Anchors are wildcard atoms with map numbers (e.g., `[*:1]`). "
        "Your substituents must include the same anchor label they attach to (e.g., `[*:1]C`)."
    )

with col2:
    r1 = st.text_input("R1 substituent (SMILES, must include [*:1])", value="[*:1]C")
    r2 = st.text_input("R2 substituent (SMILES, must include [*:2])", value="[*:2]OCC")
    r3 = st.text_input("R3 substituent (optional; include [*:3])", value="")

run = st.button("Generate Molecule")

st.divider()

if run:
    try:
        result = build_placeholder_molecule(scaffold, {1: r1, 2: r2, 3: r3})
        st.subheader("Result")
        st.code(result, language="text")
        smiles_download_button(result, filename="naria_generated.smiles")
    except Exception as e:
        st.error(f"Error: {e}")

st.divider()
st.caption("Demo build focused on R-group substitution. Extend with DECIMER & patent modules later.")
