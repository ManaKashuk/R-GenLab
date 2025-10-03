
import io
import base64
import streamlit as st
import pandas as pd

st.set_page_config(page_title="NARIA.app — R-Group Variant Generator (Demo)", layout="wide")

st.title("R‑Group Variant Generator (Demo)")
st.caption("Enter a scaffold with attachment points [*:1], [*:2], [*:3] and substituents with the same labels (e.g., [*:1]C).")

# ---------- Chemistry helpers ----------
def _get_anchor_idx(mol, mapnum):
    for atom in mol.GetAtoms():
        if atom.GetAtomMapNum() == mapnum:
            return atom.GetIdx()
    return None

def graft_substituent(scaffold_mol, substituent_mol, mapnum):
    \"\"\"Attach 'substituent_mol' to 'scaffold_mol' using anchors [*:mapnum] present in both.
    Both anchors must have exactly one neighbor. Happy-path demo implementation.
    \"\"\"
    sa = _get_anchor_idx(scaffold_mol, mapnum)
    sb = _get_anchor_idx(substituent_mol, mapnum)
    if sa is None or sb is None:
        raise ValueError(f\"Anchor [*:{mapnum}] not found in both molecules.\")

    s_rw = Chem.RWMol(scaffold_mol)
    sub_rw = Chem.RWMol(substituent_mol)

    sa_atom = s_rw.GetAtomWithIdx(sa)
    sb_atom = sub_rw.GetAtomWithIdx(sb)

    if sa_atom.GetDegree() != 1:
        raise ValueError(f\"Scaffold anchor [*:{mapnum}] must have exactly one neighbor.\")
    if sb_atom.GetDegree() != 1:
        raise ValueError(f\"Substituent anchor [*:{mapnum}] must have exactly one neighbor.\")

    scaff_neighbor = [n.GetIdx() for n in sa_atom.GetNeighbors()][0]
    sub_neighbor = [n.GetIdx() for n in sb_atom.GetNeighbors()][0]

    combo = Chem.CombineMols(s_rw, sub_rw)
    combo_rw = Chem.RWMol(combo)

    offset = s_rw.GetNumAtoms()
    combo_rw.AddBond(scaff_neighbor, sub_neighbor + offset, Chem.BondType.SINGLE)

    for idx in sorted([sa, sb + offset], reverse=True):
        combo_rw.RemoveAtom(idx)

    newmol = combo_rw.GetMol()
    Chem.SanitizeMol(newmol)
    for atom in newmol.GetAtoms():
        atom.SetAtomMapNum(0)
    return newmol

def build_molecule(scaffold_smiles, rsubs):
    mol = Chem.MolFromSmiles(scaffold_smiles)
    if mol is None:
        raise ValueError(\"Invalid scaffold SMILES.\")
    Chem.SanitizeMol(mol)

    for mapnum, s in rsubs.items():
        s = (s or \"\").strip()
        if not s:
            continue
        sub = Chem.MolFromSmiles(s)
        if sub is None:
            raise ValueError(f\"Invalid substituent SMILES for R{mapnum}: {s}\")
        Chem.SanitizeMol(sub)
        mol = graft_substituent(mol, sub, mapnum)
    return mol

def mol_to_image_bytes(mol, size=(400, 300)):
    img = Draw.MolToImage(mol, size=size)
    out = io.BytesIO()
    img.save(out, format=\"PNG\")
    return out.getvalue()

def smiles_download_button(smiles, filename=\"molecule.smiles\"):
    b64 = base64.b64encode(smiles.encode(\"utf-8\")).decode()
    href = f'<a download=\"{filename}\" href=\"data:text/plain;base64,{b64}\">Download SMILES</a>'
    st.markdown(href, unsafe_allow_html=True)

# ---------- UI ----------
st.subheader(\"Inputs\")

col1, col2 = st.columns([1,1])
with col1:
    scaffold = st.text_input(
        \"Base Scaffold (SMILES with anchors)\",
        value=\"c1cc([*:1])ccc1[*:2]\",
        help=\"Example: c1cc([*:1])ccc1[*:2] (para-disubstituted benzene with two anchors)\"
    )
    st.markdown(
        \"**Tip:** Anchors are wildcard atoms with map numbers (e.g., `[*:1]`). \"
        \"Your substituents must include the same anchor label they attach to (e.g., `[*:1]C`).\"
    )

with col2:
    r1 = st.text_input(\"R1 substituent (SMILES, must include [*:1])\", value=\"[*:1]C\")
    r2 = st.text_input(\"R2 substituent (SMILES, must include [*:2])\", value=\"[*:2]OCC\")
    r3 = st.text_input(\"R3 substituent (optional; include [*:3])\", value=\"\")

run = st.button(\"Generate Molecule\")

st.divider()

if run:
    try:
        mol = build_molecule(scaffold, {1: r1, 2: r2, 3: r3})
        smi = Chem.MolToSmiles(mol)
        st.subheader(\"Result\")
        st.code(smi, language=\"text\")
        st.image(mol_to_image_bytes(mol), caption=\"Generated Structure\", use_column_width=False)
        smiles_download_button(smi, filename=\"naria_generated.smiles\")
    except Exception as e:
        st.error(f\"Error: {e}\")

st.divider()
st.caption(\"Demo build focused on R-group substitution. Extend with DECIMER & patent modules later.\")
