# NARIA.app — R‑Group Variant Generator (Demo)

A minimal Streamlit prototype that lets you:
- enter a **base scaffold** SMILES with attachment points labeled as `[*:1]`, `[*:2]`, `[*:3]`
- enter **substituent** SMILES for `R1`, `R2`, `R3` using the same anchor label (e.g., `[*:1]C` for methyl)
- generate the substituted molecule and visualize it
- download the resulting SMILES

This project is a first step toward your broader NARIA.app concept (DECIMER + RDKit + patent scaffolds).

## Quickstart

### 1) Clone & set up
```bash
git clone https://github.com/<YOUR-USERNAME>/naria-app-demo.git
cd naria-app-demo
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Run the app
```bash
streamlit run app.py
```

### 3) Open in your browser
Streamlit will print a local URL (e.g., `http://localhost:8501`).

## How to label attachment points

Use wildcard atoms with map numbers on your **scaffold** and **substituents**:
- Scaffold example (para-disubstituted benzene, two anchors): `c1cc([*:1])ccc1[*:2]`
- Substituent for R1 (methyl): `[*:1]C`
- Substituent for R2 (ethoxy): `[*:2]OCC`

> The `[*:n]` atom acts as a removable **anchor**. The app will remove the anchors and connect the neighboring atoms.

## Notes

- This is a **demo** (happy-path) and assumes anchors each have a single neighbor.
- RDKit is used locally; DECIMER/image-to-SMILES can be added later.
- For multi-variant combinatorics, extend `generate_variants()` accordingly.

## Deploying on Streamlit Community Cloud

1. Push this repo to GitHub.
2. Go to https://streamlit.io/cloud and connect your GitHub.
3. Select this repo, set `app.py` as the entry point, and deploy.
4. Add the following in **Advanced settings** if needed:
   - Python version: 3.11
   - `requirements.txt` is auto-detected.

## License
MIT
