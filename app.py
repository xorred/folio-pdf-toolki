"""
╔══════════════════════════════════════════════════════════════╗
║              FOLIO — Local PDF & Image Toolkit               ║
║         Premium SaaS-grade Streamlit Application             ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
import time

# ─────────────────────────────────────────────
#  PAGE CONFIG — must be first Streamlit call
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Folio — Local PDF & Image Toolkit",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  STATE MANAGEMENT
# ─────────────────────────────────────────────
if 'current_nav' not in st.session_state:
    st.session_state.current_nav = "Overview"

def set_page(page_name):
    st.session_state.current_nav = page_name

# ─────────────────────────────────────────────
#  GLOBAL CSS — Ultra-Premium Dark Mode
# ─────────────────────────────────────────────
GLOBAL_CSS = """
<style>
/* ── FONTS ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

:root {
  --bg:          #050505;
  --surface:     #0A0A0A;
  --surface-2:   #111111;
  --surface-3:   #1A1A1A;
  --border:      rgba(255,255,255,0.06);
  --border-hi:   rgba(255,255,255,0.12);
  --accent:      #5E6AD2;
  --accent-soft: rgba(94, 106, 210, 0.15);
  --accent-glow: rgba(94, 106, 210, 0.4);
  --green:       #10b981;
  --amber:       #f59e0b;
  --red:         #ef4444;
  --text-1:      #FAFAFA;
  --text-2:      #A1A1AA;
  --text-3:      #52525B;
  --radius-sm:   6px;
  --radius-md:   12px;
  --radius-lg:   20px;
  --font-body:   'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --transition:  all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

/* ── BASE INJECTIONS ── */
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
  background-color: var(--bg) !important;
  color: var(--text-1) !important;
  font-family: var(--font-body) !important;
}

#MainMenu, footer, header, [data-testid="stToolbar"], [data-testid="stDecoration"] { 
    display: none !important; 
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
  background: var(--surface) !important;
  border-right: 1px solid var(--border) !important;
  width: 280px !important;
}

/* SIDEBAR NAVIGATION (Hiding radio buttons, making them look like tabs) */
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    cursor: pointer !important;
}
/* Hide the actual radio circle */
[data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"] div:first-child {
    display: none !important; 
}
/* Style the clickable row */
[data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"] {
    background: transparent;
    padding: 10px 16px !important;
    border-radius: var(--radius-md) !important;
    margin-bottom: 4px !important;
    transition: var(--transition) !important;
    width: 100% !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"]:hover {
    background: var(--surface-3) !important;
}
/* Active state */
[data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"][aria-checked="true"] {
    background: var(--surface-2) !important;
    border: 1px solid var(--border-hi) !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.5) !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"] p {
    color: var(--text-2) !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"][aria-checked="true"] p {
    color: var(--text-1) !important;
    font-weight: 600 !important;
}

/* ── HOME PAGE CARDS (Targeting native bordered containers) ── */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: linear-gradient(180deg, rgba(26,26,26,0.4) 0%, rgba(17,17,17,0.8) 100%) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-lg) !important;
    padding: 1.75rem !important;
    transition: var(--transition) !important;
    position: relative;
    overflow: hidden;
}
[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: var(--border-hi) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 30px rgba(0,0,0,0.8), 0 0 0 1px rgba(94, 106, 210, 0.2) inset !important;
}
/* Header inside card */
[data-testid="stVerticalBlockBorderWrapper"] h3 {
    font-size: 1.25rem !important;
    font-weight: 600 !important;
    letter-spacing: -0.02em !important;
    color: var(--text-1) !important;
    margin-bottom: 0.5rem !important;
    padding: 0 !important;
}
/* Text inside card */
[data-testid="stVerticalBlockBorderWrapper"] p {
    color: var(--text-2) !important;
    font-size: 0.95rem !important;
    line-height: 1.5 !important;
    margin-bottom: 0 !important;
}

/* ── BUTTON INSIDE THE CARD (Make it look like a seamless link) ── */
[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stButton"] button {
    background: transparent !important;
    border: none !important;
    color: var(--text-3) !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.05em !important;
    padding: 0 !important;
    margin-top: 1.5rem !important;
    text-transform: uppercase !important;
    box-shadow: none !important;
    justify-content: flex-start !important;
    transition: var(--transition) !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:hover [data-testid="stButton"] button {
    color: var(--accent) !important;
}
[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stButton"] button:hover {
    color: #8C98FF !important;
    transform: translateX(4px) !important;
}

/* ── STANDARD BUTTONS ── */
.stButton > button {
  background: var(--surface-3) !important;
  color: var(--text-1) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-md) !important;
  font-weight: 500 !important;
  font-size: 0.9rem !important;
  padding: 0.6rem 1.5rem !important;
  transition: var(--transition) !important;
  cursor: pointer !important;
}
.stButton > button:hover {
  background: var(--surface-2) !important;
  border-color: var(--accent) !important;
  color: var(--accent) !important;
}

/* ── DOWNLOAD BUTTON ── */
.stDownloadButton > button {
  background: var(--accent-soft) !important;
  border: 1px solid rgba(94, 106, 210, 0.4) !important;
  color: #8C98FF !important;
  font-weight: 600 !important;
}
.stDownloadButton > button:hover { 
    background: var(--accent) !important; 
    color: #fff !important; 
    border-color: var(--accent) !important;
    box-shadow: 0 4px 15px var(--accent-glow) !important;
}

/* ── FILE UPLOADER ── */
[data-testid="stFileUploader"] {
  background: var(--surface-2) !important;
  border: 1px dashed var(--border-hi) !important;
  border-radius: var(--radius-lg) !important;
  padding: 2.5rem !important;
  transition: var(--transition) !important;
}
[data-testid="stFileUploader"]:hover {
  border-color: var(--accent) !important;
  background: rgba(94, 106, 210, 0.05) !important;
}

/* ── CUSTOM UI COMPONENTS ── */
.folio-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(255,255,255,0.05);
  color: var(--text-2);
  border: 1px solid var(--border);
  border-radius: 99px;
  padding: 4px 12px;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.folio-hero { padding: 4rem 3.5rem 3rem; }
.folio-hero h1 {
  font-size: 3.5rem;
  font-weight: 800;
  letter-spacing: -0.04em;
  line-height: 1.05;
  background: linear-gradient(180deg, #FFFFFF 0%, #A1A1AA 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 1rem;
}
.folio-hero p {
  color: var(--text-2);
  font-size: 1.15rem;
  font-weight: 400;
  line-height: 1.6;
  max-width: 600px;
}

.sidebar-logo {
  padding: 2rem 1.5rem 1.5rem;
  margin-bottom: 0.5rem;
}
.sidebar-logo .logo-mark {
  font-size: 1.4rem;
  font-weight: 800;
  letter-spacing: -0.04em;
  color: var(--text-1);
  display: flex;
  align-items: center;
  gap: 12px;
}
.sidebar-logo .logo-mark .dot {
  width: 12px; height: 12px;
  border-radius: 50%;
  background: var(--accent);
  box-shadow: 0 0 16px var(--accent-glow);
}
.sidebar-logo .tagline {
  font-size: 0.75rem;
  color: var(--text-3);
  margin-top: 8px;
  font-weight: 500;
}

.tool-area { padding: 2rem 3.5rem; max-width: 960px; }
.step-label { 
    font-size: 0.75rem; 
    font-weight: 700; 
    text-transform: uppercase; 
    letter-spacing: 0.08em; 
    color: var(--accent); 
    margin-bottom: 0.75rem; 
}
.folio-sep { height: 1px; background: linear-gradient(90deg, var(--border), transparent); margin: 2.5rem 0; }

.file-chip {
    background: var(--surface-3);
    border: 1px solid var(--border-hi);
    padding: 10px 16px;
    border-radius: var(--radius-md);
    font-size: 0.85rem;
    color: var(--text-1);
    display: inline-flex;
    align-items: center;
    gap: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}
</style>
"""

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────

def get_pdf_reader(file_bytes: bytes) -> fitz.Document:
    return fitz.open(stream=file_bytes, filetype="pdf")

def human_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024**2:
        return f"{size_bytes/1024:.1f} KB"
    else:
        return f"{size_bytes/1024**2:.2f} MB"

def pdf_to_bytes(doc: fitz.Document) -> bytes:
    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf.read()

def step(label: str):
    st.markdown(f'<div class="step-label">{label}</div>', unsafe_allow_html=True)

def section_sep():
    st.markdown('<div class="folio-sep"></div>', unsafe_allow_html=True)

def tool_header(icon: str, title: str, desc: str):
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 1.25rem; margin-bottom: 2.5rem;">
      <div style="width: 56px; height: 56px; border-radius: 14px; background: var(--surface-2); border: 1px solid var(--border-hi); display: flex; align-items: center; justify-content: center; font-size: 1.6rem; box-shadow: 0 8px 20px rgba(0,0,0,0.4);">
        {icon}
      </div>
      <div>
        <h2 style="font-size: 1.8rem; font-weight: 700; margin: 0; letter-spacing: -0.03em; color: var(--text-1);">{title}</h2>
        <p style="color: var(--text-2); font-size: 0.95rem; margin: 4px 0 0 0;">{desc}</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

def success_card(title: str, extra_html: str = ""):
    st.markdown(f"""
    <div style="background: rgba(16,185,129,0.05); border: 1px solid rgba(16,185,129,0.2); border-radius: var(--radius-md); padding: 1.25rem 1.5rem; margin-top: 1.5rem;">
        <div style="color: var(--green); font-weight: 600; font-size: 1rem; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 8px;">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
            {title}
        </div>
        {extra_html}
    </div>
    """, unsafe_allow_html=True)

def render_file_info(name: str, size_bytes: int, pages: int | None = None):
    extras = f'<span style="color:var(--text-3);">·</span> <span>{pages} pages</span>' if pages else ""
    st.markdown(f"""
    <div class="file-chip">
      <span style="font-size: 1.1rem;">📄</span> 
      <strong style="font-weight: 500;">{name}</strong> 
      <span style="color:var(--text-3); margin-left:4px; margin-right:4px;">|</span> 
      <span style="color:var(--text-2);">{human_size(size_bytes)}</span>
      {extras}
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────

NAV_ITEMS = [
    ("🏠 Overview", "Overview"),
    ("🔗 Merge PDFs", "Combine multiple PDFs"),
    ("✂️ Split PDF", "Extract pages"),
    ("🔄 Convert", "JPEG ↔ PDF"),
    ("⚡ Compress", "Reduce file size"),
]

with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
      <div class="logo-mark"><div class="dot"></div> Folio</div>
      <div class="tagline">Local PDF &amp; Image Toolkit</div>
    </div>
    """, unsafe_allow_html=True)

    tool_labels = [item[0] for item in NAV_ITEMS]

    # Clean, styled radio buttons acting as nav
    selected_tool = st.radio(
        "Navigation",
        options=tool_labels,
        label_visibility="collapsed",
        key="current_nav"
    )

    st.markdown("""<div style="flex:1; margin-top: 45vh;"></div>""", unsafe_allow_html=True)
    st.markdown("""
    <div style="padding:1.5rem; border-top:1px solid var(--border);">
      <div style="font-size:0.8rem; color:var(--text-3); line-height:1.6; display:flex; flex-direction:column; gap:8px;">
        <span style="color:var(--text-2); font-weight:600; letter-spacing:0.02em; display:flex; align-items:center; gap:6px;">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
            Privacy First
        </span>
        100% local processing. Zero data leaves your device.
      </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  HOME PAGE
# ─────────────────────────────────────────────

def page_home():
    st.markdown("""
    <div class="folio-hero">
      <div style="margin-bottom:1.25rem;"><span class="folio-badge">Folio v2.0 Toolkit</span></div>
      <h1>Your documents,<br>under your control.</h1>
      <p>A professional toolkit running entirely on your machine. Fast, secure, and beautifully simple.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="tool-area" style="padding-top:0;">', unsafe_allow_html=True)

    tools_info = [
        ("🔗 Merge PDFs", "Combine multiple PDFs into a single, cohesive document instantly.", "🔗 Merge PDFs"),
        ("✂️ Split PDF",  "Extract specific pages or page ranges from any PDF file.", "✂️ Split PDF"),
        ("🔄 Convert",    "Transform JPEGs to PDFs or extract high-fidelity images from documents.", "🔄 Convert"),
        ("⚡ Compress",   "Slash file sizes natively without sacrificing visual readability.", "⚡ Compress"),
    ]

    col1, col2 = st.columns(2, gap="large")
    for i, (title, desc, nav_target) in enumerate(tools_info):
        with (col1 if i % 2 == 0 else col2):
            # The border container is styled by CSS to look like a premium hover card
            with st.container(border=True):
                st.markdown(f"### {title}")
                st.markdown(f"<p>{desc}</p>", unsafe_allow_html=True)
                # Seamless button styled via CSS
                st.button("USE TOOL →", key=f"btn_{i}", on_click=set_page, args=(nav_target,), use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  TOOL: MERGE PDFs
# ─────────────────────────────────────────────

def page_merge():
    st.markdown('<div class="tool-area">', unsafe_allow_html=True)
    tool_header("🔗", "Merge PDFs", "Combine multiple PDF files into one seamless document.")

    step("Step 1 — Upload your PDFs")
    uploaded_files = st.file_uploader(
        "Drop PDFs here", type=["pdf"], accept_multiple_files=True, label_visibility="collapsed"
    )

    if not uploaded_files:
        st.markdown('</div>', unsafe_allow_html=True)
        return

    section_sep()
    step("Step 2 — Files to merge (in order)")

    total_pages = 0
    total_size  = 0
    for f in uploaded_files:
        data = f.read()
        f.seek(0)
        doc = get_pdf_reader(data)
        total_pages += len(doc)
        total_size  += len(data)
        render_file_info(f.name, len(data), len(doc))
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    section_sep()
    step("Step 3 — Merge")

    if st.button("🔗 Merge Documents"):
        with st.spinner("Merging documents..."):
            progress = st.progress(0)
            merged = fitz.open()
            for i, f in enumerate(uploaded_files):
                data = f.read()
                doc = get_pdf_reader(data)
                merged.insert_pdf(doc)
                progress.progress(int((i + 1) / len(uploaded_files) * 100))
                time.sleep(0.05)
            output = pdf_to_bytes(merged)
            progress.empty()

        success_card("Merged successfully!", f"<span style='color:var(--text-2); font-size:0.85rem;'>Final Output: <strong style='color:var(--text-1)'>{human_size(len(output))}</strong> · {total_pages} pages</span>")
        st.download_button("⬇ Download Merged PDF", output, file_name="folio_merged.pdf", mime="application/pdf")

    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  TOOL: SPLIT PDF
# ─────────────────────────────────────────────

def page_split():
    st.markdown('<div class="tool-area">', unsafe_allow_html=True)
    tool_header("✂️", "Split PDF", "Extract a page range or individual pages from any PDF.")

    step("Step 1 — Upload your PDF")
    uploaded = st.file_uploader("Drop a PDF here", type=["pdf"], label_visibility="collapsed")

    if not uploaded:
        st.markdown('</div>', unsafe_allow_html=True)
        return

    data = uploaded.read()
    doc = get_pdf_reader(data)
    total = len(doc)
    
    render_file_info(uploaded.name, len(data), total)

    section_sep()
    step("Step 2 — Extraction mode")
    mode = st.radio("Mode", ["Page Range", "Individual Pages", "Split into Single Pages"], horizontal=True, label_visibility="collapsed")
    new_doc = fitz.open()

    if mode == "Page Range":
        col1, col2 = st.columns(2)
        with col1:
            start = st.number_input("From page", min_value=1, max_value=total, value=1)
        with col2:
            end = st.number_input("To page", min_value=1, max_value=total, value=total)
            
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        if st.button("✂️ Extract Range"):
            with st.spinner("Extracting..."):
                new_doc.insert_pdf(doc, from_page=start-1, to_page=end-1)
                output = pdf_to_bytes(new_doc)
            success_card("Extraction complete!")
            st.download_button("⬇ Download Extracted PDF", output, file_name=f"folio_pages_{start}-{end}.pdf", mime="application/pdf")

    elif mode == "Individual Pages":
        pages_str = st.text_input("Page numbers (comma-separated)", placeholder=f"e.g. 1, 3, 5")
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        if st.button("✂️ Extract Pages"):
            try:
                page_nums = [int(p.strip()) for p in pages_str.split(",") if p.strip()]
                for p in page_nums:
                    new_doc.insert_pdf(doc, from_page=p-1, to_page=p-1)
                output = pdf_to_bytes(new_doc)
                success_card("Extraction complete!")
                st.download_button("⬇ Download Extracted PDF", output, file_name="folio_selected.pdf", mime="application/pdf")
            except Exception:
                st.error("Invalid input. Use comma-separated numbers.")

    else:
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        if st.button("✂️ Split All Pages"):
            with st.spinner("Splitting..."):
                for i in range(total):
                    single = fitz.open()
                    single.insert_pdf(doc, from_page=i, to_page=i)
                    st.download_button(f"⬇ Download Page {i+1}", pdf_to_bytes(single), file_name=f"folio_page_{i+1}.pdf", mime="application/pdf", key=f"dl_{i}")

    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  TOOL: CONVERT
# ─────────────────────────────────────────────

def page_convert():
    st.markdown('<div class="tool-area">', unsafe_allow_html=True)
    tool_header("🔄", "Convert", "Transform images to PDF or extract PDF pages as images.")

    step("Choose conversion direction")
    direction = st.radio("Direction", ["JPEG / PNG → PDF", "PDF → JPEG Images"], horizontal=True, label_visibility="collapsed")
    section_sep()

    if direction == "JPEG / PNG → PDF":
        step("Upload images")
        images = st.file_uploader("Drop image files", type=["jpg", "jpeg", "png"], accept_multiple_files=True, label_visibility="collapsed")
        
        if images:
            st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
            if st.button("🔄 Convert to PDF"):
                with st.spinner("Converting..."):
                    doc = fitz.open()
                    for img_file in images:
                        img = Image.open(img_file).convert("RGB")
                        img_bytes = io.BytesIO()
                        img.save(img_bytes, format="JPEG", quality=95)
                        img_bytes.seek(0)
                        img_doc = fitz.open("jpg", img_bytes.read())
                        pdfbytes = img_doc.convert_to_pdf()
                        doc.insert_pdf(fitz.open("pdf", pdfbytes))
                    output = pdf_to_bytes(doc)
                success_card("Conversion complete!")
                st.download_button("⬇ Download PDF", output, file_name="folio_converted.pdf", mime="application/pdf")
    else:
        step("Upload PDF")
        uploaded = st.file_uploader("Drop a PDF here", type=["pdf"], label_visibility="collapsed")
        
        if uploaded:
            data = uploaded.read()
            doc = get_pdf_reader(data)
            
            section_sep()
            step("Image Quality Settings")
            dpi = st.slider("Render DPI", 72, 300, 150, step=24)
            
            st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
            if st.button("🔄 Extract as Images"):
                with st.spinner("Rendering..."):
                    for i in range(len(doc)):
                        pix = doc[i].get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72))
                        st.download_button(f"⬇ Download Page {i+1} (JPEG)", pix.tobytes("jpeg"), file_name=f"page_{i+1}.jpg", mime="image/jpeg", key=f"img_{i}")

    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  TOOL: COMPRESS
# ─────────────────────────────────────────────

def page_compress():
    st.markdown('<div class="tool-area">', unsafe_allow_html=True)
    tool_header("⚡", "Compress PDF", "Reduce file size intelligently.")

    step("Step 1 — Upload PDF")
    uploaded = st.file_uploader("Drop a PDF here", type=["pdf"], label_visibility="collapsed")
    
    if not uploaded:
        st.markdown('</div>', unsafe_allow_html=True)
        return

    data = uploaded.read()
    doc = get_pdf_reader(data)
    render_file_info(uploaded.name, len(data), len(doc))

    section_sep()
    step("Step 2 — Compression Settings")
    
    col1, col2 = st.columns(2)
    with col1: quality = st.slider("Image Quality", 10, 95, 60)
    with col2: dpi = st.slider("Render DPI", 72, 200, 100)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    if st.button("⚡ Compress PDF"):
        with st.spinner("Compressing (this may take a moment)..."):
            out_doc = fitz.open()
            progress = st.progress(0)
            total = len(doc)
            
            for i, page in enumerate(doc):
                pix = page.get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72))
                img_doc = fitz.open("jpg", pix.tobytes("jpeg", jpg_quality=quality))
                out_doc.insert_pdf(fitz.open("pdf", img_doc.convert_to_pdf()))
                progress.progress(int((i + 1) / total * 100))
                
            output = pdf_to_bytes(out_doc)
            progress.empty()
            
        success_card("Compression complete!", f"<span style='color:var(--text-2); font-size:0.85rem;'>Saved size: <span style='text-decoration:line-through;'>{human_size(len(data))}</span> → <strong style='color:var(--green)'>{human_size(len(output))}</strong></span>")
        st.download_button("⬇ Download Compressed PDF", output, file_name="folio_compressed.pdf", mime="application/pdf")

    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  ROUTER
# ─────────────────────────────────────────────
if st.session_state.current_nav == "🏠 Overview":
    page_home()
elif st.session_state.current_nav == "🔗 Merge PDFs":
    page_merge()
elif st.session_state.current_nav == "✂️ Split PDF":
    page_split()
elif st.session_state.current_nav == "🔄 Convert":
    page_convert()
elif st.session_state.current_nav == "⚡ Compress":
    page_compress()
