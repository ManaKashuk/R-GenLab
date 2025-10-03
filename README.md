# R‑Group Variant Generator (Demo)

Welcome to **R-GenLab**, a Streamlit-powered demo application under the **NARIA.app** brand. This tool enables chemists and researchers to generate molecular variants by attaching R-group substituents to a scaffold structure using SMARTS-based anchor points.

---

## 🚀 Purpose

The app demonstrates a simple but powerful approach to **R-group substitution** using RDKit. It allows users to:
- Input a scaffold molecule with anchor points (e.g., `[*:1]`, `[*:2]`, `[*:3]`)
- Provide substituents that match those anchor labels
- Generate a new molecule with the substituents grafted onto the scaffold
- View the resulting structure and download its SMILES representation

---

## 🧪 Usage

1. **Base Scaffold**: Enter a SMILES string with anchor points (e.g., `c1cc([*:1])ccc1[*:2]`)
2. **Substituents**: Provide SMILES strings for R1, R2, and optionally R3 (e.g., `[*:1]C`, `[*:2]OCC`)
3. **Generate Molecule**: Click the button to visualize the resulting structure
4. **Download**: Save the generated SMILES string for further use

Example inputs:
- Scaffold: `c1cc([*:1])ccc1[*:2]`
- R1: `[*:1]C`
- R2: `[*:2]OCC`

---

# Clone the repository
git clone https://github.com/ManaKashuk/R-GenLab.git
cd R-GenLab

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # or venv\\Scripts\\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
