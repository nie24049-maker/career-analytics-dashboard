import streamlit as st
import pandas as pd

st.set_page_config(page_title="Austin Nielsen | Operations Hub", page_icon="🎓", layout="wide")

st.markdown("""
<style>
.stApp { background: #f4f7fb; color: #102a43; }
[data-testid="stSidebar"] { background: #102a43; }
[data-testid="stSidebar"] * { color: white; }
.hero { background: linear-gradient(120deg,#0b3954,#087e8b); color:white; padding:2rem; border-radius:18px; margin-bottom:1rem; }
.hero h1 { margin:0; font-size:2.7rem; }
.card { background:white; border:1px solid #d9e2ec; border-radius:14px; padding:1rem; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🎓 Austin Nielsen")
    st.caption("Academic & Career Operations Hub")
    st.divider()
    st.subheader("Quick bio")
    st.write("Business Management and I-O Psychology student focused on improving team performance and campus systems.")
    st.subheader("Key metrics")
    st.metric("Target career chats", "50+")
    st.metric("GPA target", "3.75+")
    st.metric("Governance goal", "2028")
    st.subheader("Connect")
    st.markdown("[LinkedIn](https://www.linkedin.com/)")
    st.markdown("[Email Austin](mailto:austin.nielsen@example.com)")

st.markdown("""
<div class="hero">
<div style="text-transform:uppercase;letter-spacing:.12em;font-size:.8rem;color:#a7f3d0">Executive student dashboard</div>
<h1>Austin Nielsen</h1>
<p><b>Business Management</b> × <b>Industrial-Organizational Psychology</b></p>
<p>Mission: optimize team performance and campus systems through leadership, process improvement, and evidence-informed people strategies.</p>
</div>
""", unsafe_allow_html=True)

st.caption("ITM 101 cloud project • Academic progress • Networking • Governance")

networking = pd.DataFrame([
    {"Contact":"Sister Paulette Kirkham", "Role":"Leadership Communication", "Key Takeaway":"Clear communication builds trust and alignment.", "Follow-up Status":"Send thank-you note"},
    {"Contact":"Bob Morley", "Role":"Strategy Consulting", "Key Takeaway":"Translate analysis into decisions leaders can act on.", "Follow-up Status":"Schedule follow-up"},
    {"Contact":"Jared Stanger", "Role":"Healthcare AI & Lean", "Key Takeaway":"Pair responsible AI with measurable process improvement.", "Follow-up Status":"Research next steps"},
    {"Contact":"Amy Staiger", "Role":"Academic Advising", "Key Takeaway":"Good systems make student progress easier to navigate.", "Follow-up Status":"Complete"},
])

skills = pd.DataFrame({"Skill":["Business Operations","I-O Psychology","AI Prompt Engineering","Process Optimization","Team Assessment Design"], "Proficiency":[82,76,68,73,64]}).set_index("Skill")

network_tab, skills_tab, roadmap_tab = st.tabs(["Networking & Career Chats", "Competency & Skill Matrix", "Strategic Milestones Roadmap"])
with network_tab:
    st.subheader("Recent informational interviews")
    search = st.text_input("Filter contacts or topics", placeholder="Try: strategy")
    view = networking if not search else networking[networking.astype(str).apply(lambda row: row.str.contains(search, case=False).any(), axis=1)]
    st.dataframe(view, use_container_width=True, hide_index=True)
with skills_tab:
    st.subheader("Current proficiency snapshot")
    st.bar_chart(skills, y="Proficiency", horizontal=True, use_container_width=True)
    st.caption("Adjust these baseline scores as coursework, projects, and conversations create new evidence.")
with roadmap_tab:
    st.subheader("Strategic milestones")
    milestones = [
        ("2026–2027", "Student Leadership Council Governance", "Build practical governance experience and improve campus systems."),
        ("2027", "Academic TA-ship", "Apply business and I-O psychology concepts while supporting other students."),
        ("Spring 2028", "President Meredith Meeting", "Present a concise vision for student leadership and campus operations."),
    ]
    for year, title, detail in milestones:
        st.markdown(f"### {year} — {title}")
        st.write(detail)
        st.divider()

st.success("Dashboard ready for continuous updates as academic, networking, and governance progress evolves.")
