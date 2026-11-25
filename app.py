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
.card { background:white; border:1px solid #d9e2ec; border-radius:14px; padding:1rem; box-shadow:0 4px 12px #102a4314; }
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

cols = st.columns(4)
for col, value, label in zip(cols, ["50+", "3.75+", "5", "2028"], ["Target career chats", "GPA target", "Core competencies", "Governance horizon"]):
    with col:
        st.markdown(f'<div class="card"><h2>{value}</h2><p>{label}</p></div>', unsafe_allow_html=True)

networking, skills, roadmap = st.tabs(["Networking & Career Chats", "Competency & Skill Matrix", "Strategic Milestones Roadmap"])

with networking:
    st.subheader("Recent informational interviews")
    data = pd.DataFrame([
        ["Sister Paulette Kirkham", "Leadership Communication", "Values-based communication builds trust during change.", "Thank-you sent"],
        ["Bob Morley", "Strategy Consulting", "Strong problem framing makes recommendations actionable.", "Schedule next chat"],
        ["Jared Stanger", "Healthcare AI & Lean", "Pair AI experiments with disciplined process measurement.", "Notes captured"],
        ["Amy Staiger", "Academic Advising", "Easy-to-navigate support systems improve student success.", "Intro requested"],
    ], columns=["Contact", "Role", "Key Takeaway", "Follow-up Status"])
    statuses = st.multiselect("Filter by follow-up status", data["Follow-up Status"].unique(), default=list(data["Follow-up Status"].unique()))
    st.dataframe(data[data["Follow-up Status"].isin(statuses)], use_container_width=True, hide_index=True)

with skills:
    st.subheader("Competency & Skill Matrix")
    st.write("Adjust the sliders to model current proficiency.")
    defaults = {"Business Operations":78, "I-O Psychology":68, "AI Prompt Engineering":62, "Process Optimization":74, "Team Assessment Design":58}
    values = {skill: st.slider(skill, 0, 100, score, 5) for skill, score in defaults.items()}
    chart = pd.DataFrame({"Skill": list(values), "Proficiency": list(values.values())})
    st.bar_chart(chart, x="Skill", y="Proficiency", color="#087e8b")
    st.info(f"Average proficiency: {round(chart['Proficiency'].mean())}/100")

with roadmap:
    st.subheader("Strategic Milestones Roadmap")
    milestones = [
        ("2026–2027", "Student Leadership Council Governance", "Build governance experience through committee service and measurable campus improvements."),
        ("2027", "Academic TA-ship", "Apply business and I-O Psychology concepts while mentoring peers and improving learning workflows."),
        ("Spring 2028", "President Meredith Meeting", "Present a campus-systems portfolio focused on team performance and operational excellence."),
    ]
    for year, title, detail in milestones:
        st.markdown(f"### {year} — {title}
{detail}

---")

st.caption("Austin Nielsen • Academic & Career Operations Hub • Built with Streamlit")
