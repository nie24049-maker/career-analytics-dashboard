import re
from datetime import date
from urllib.parse import parse_qs, urlparse

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Austin Nielsen | Operations Hub", page_icon="🎓", layout="wide")

TODAY = pd.Timestamp(date.today())
CANONICAL = ["Contact", "Category", "Organization", "Method", "Last Contact", "Status", "Priority", "Next Action", "Key Takeaway", "Homework Anchor", "Referred By"]
DEFAULTS = {
    "Category": "Uncategorized", "Organization": "", "Method": "", "Last Contact": "",
    "Status": "Planned", "Priority": "Medium", "Next Action": "", "Key Takeaway": "",
    "Homework Anchor": "", "Referred By": "",
}
DEFAULT_CONTACTS = [
    {"Contact":"Sister Paulette Kirkham", "Category":"Faculty", "Organization":"Leadership Communication", "Method":"In-person", "Last Contact":"2026-11-17", "Status":"Completed", "Priority":"High", "Next Action":"Request warm intro to Brother Tim Rarick or Dean Greenwood", "Key Takeaway":"Create conditions where people choose to thrive.", "Homework Anchor":"The Law of Love; Letters to a Young Mormon", "Referred By":"Self"},
    {"Contact":"Bob Morley", "Category":"Industry practitioner", "Organization":"Strategy & Training Consulting", "Method":"In-person", "Last Contact":"", "Status":"Follow-up due", "Priority":"High", "Next Action":"Share a short update and ask about consulting contacts", "Key Takeaway":"Translate analysis into decisions leaders can act on.", "Homework Anchor":"How Will You Measure Your Life?", "Referred By":"Amy Staiger"},
    {"Contact":"Jared Stanger", "Category":"Industry practitioner", "Organization":"Healthcare AI & Lean", "Method":"Text / WhatsApp", "Last Contact":"2026-11-19", "Status":"Outreach Sent", "Priority":"High", "Next Action":"Send a brief follow-up about AI and process optimization", "Key Takeaway":"Pair responsible AI with measurable process improvement.", "Homework Anchor":"Lean and responsible AI next steps", "Referred By":"Healthcare lecture"},
    {"Contact":"Amy Staiger", "Category":"Academic advising", "Organization":"Academic Advising", "Method":"In-person", "Last Contact":"", "Status":"Completed", "Priority":"Medium", "Next Action":"Review flex-track courses and peer-advisor opportunities", "Key Takeaway":"Good systems make student progress easier to navigate.", "Homework Anchor":"Confirm next registration and aid questions", "Referred By":"Advising Center"},
    {"Contact":"Dean Janelle Greenwood", "Category":"Campus administration", "Organization":"Health & Human Sciences", "Method":"Email", "Last Contact":"", "Status":"Planned", "Priority":"High", "Next Action":"Request a 15-minute conversation about institutional leadership", "Key Takeaway":"Learn how campus systems support student success.", "Homework Anchor":"Prepare three questions about campus systems", "Referred By":"Sister Paulette Kirkham"},
    {"Contact":"Brother Tim Rarick", "Category":"Faculty / mentor", "Organization":"UN Student Delegation", "Method":"Email", "Last Contact":"", "Status":"Planned", "Priority":"High", "Next Action":"Ask about the UN delegation and leadership opportunities", "Key Takeaway":"Explore practical leadership experience with campus impact.", "Homework Anchor":"Ask about delegation requirements and timeline", "Referred By":"Sister Paulette Kirkham"},
    {"Contact":"Brother Johan Delton", "Category":"Faculty", "Organization":"I-O Psychology", "Method":"Email", "Last Contact":"", "Status":"Planned", "Priority":"Medium", "Next Action":"Ask about I-O career pathways and graduate preparation", "Key Takeaway":"Connect coursework to evidence-based people strategy.", "Homework Anchor":"Prepare questions about I-O pathways", "Referred By":"Sister Paulette Kirkham"},
    {"Contact":"Brother Devin Merritt", "Category":"Faculty", "Organization":"I-O Psychology", "Method":"Email", "Last Contact":"", "Status":"Planned", "Priority":"High", "Next Action":"Ask about PSYCH 445 and future TA opportunities", "Key Takeaway":"Build academic authority through hands-on teaching experience.", "Homework Anchor":"Ask about TA preparation and PSYCH 445", "Referred By":"Sister Paulette Kirkham"},
    {"Contact":"Savannah Presby", "Category":"Student leadership", "Organization":"Student Leadership Council", "Method":"Email", "Last Contact":"", "Status":"Planned", "Priority":"Medium", "Next Action":"Check on SLC application and committee placement", "Key Takeaway":"Turn governance access into measurable process improvement.", "Homework Anchor":"Confirm SLC application and interview status", "Referred By":"Student Leadership Council"},
]

def normalize_contacts(df):
    aliases = {
        "Contact": ["contact", "name", "contact name"], "Category": ["category", "role", "role_category"],
        "Organization": ["organization", "department", "dept", "department_organization", "role / organization"],
        "Method": ["method", "contact_method", "preferred_channel", "contact method"],
        "Last Contact": ["last contact", "last_contact", "last_contact_date", "date"],
        "Status": ["status"], "Priority": ["priority"], "Next Action": ["next action", "next_action"],
        "Key Takeaway": ["key takeaway", "key_takeaway", "key_takeaways"],
        "Homework Anchor": ["homework anchor", "homework_anchor", "book", "resource"],
        "Referred By": ["referred by", "referred_by", "referral source"],
    }
    cleaned = {re.sub(r"[^a-z0-9]", "", str(c).lower()): c for c in df.columns}
    rename = {}
    for target, choices in aliases.items():
        for choice in choices:
            source = cleaned.get(re.sub(r"[^a-z0-9]", "", choice))
            if source:
                rename[source] = target
                break
    out = df.rename(columns=rename).copy()
    for column in CANONICAL:
        if column not in out.columns:
            out[column] = DEFAULTS.get(column, "")
    return out[CANONICAL].fillna("")

def sheet_csv_url(url):
    if "docs.google.com/spreadsheets" not in url:
        return url
    match = re.search(r"/spreadsheets/d/([a-zA-Z0-9_-]+)", url)
    if not match:
        return url
    gid = parse_qs(urlparse(url).query).get("gid", ["0"])[0]
    return f"https://docs.google.com/spreadsheets/d/{match.group(1)}/export?format=csv&gid={gid}"

if "contacts" not in st.session_state:
    st.session_state.contacts = normalize_contacts(pd.DataFrame(DEFAULT_CONTACTS))
if "source_name" not in st.session_state:
    st.session_state.source_name = "Starter records"

with st.sidebar:
    st.title("🎓 Austin Nielsen")
    st.caption("Weekly Academic & Career Operations Hub")
    st.divider()
    st.subheader("Focus")
    st.write("Business Operations × I-O Psychology")
    st.write("Optimize team performance and campus systems.")
    st.subheader("Targets")
    st.metric("Career chats goal", "50+")
    st.metric("GPA target", "3.75+")
    st.metric("President Meredith", "Spring 2028")
    st.divider()
    st.subheader("Single source of truth")
    sheet_url = st.text_input("Google Sheet or published CSV URL", placeholder="Paste your Google Sheets URL here")
    if st.button("Refresh from Google Sheets", type="primary"):
        try:
            loaded = pd.read_csv(sheet_csv_url(sheet_url.strip()))
            st.session_state.contacts = normalize_contacts(loaded)
            st.session_state.source_name = "Google Sheets"
            st.success(f"Loaded {len(st.session_state.contacts)} records.")
        except Exception as exc:
            st.error("Could not load that sheet. Make sure the sheet is published or shared as CSV.")
    if sheet_url.startswith("https://"):
        st.link_button("Open the source sheet", sheet_url)
    st.download_button("Download normalized backup", st.session_state.contacts.to_csv(index=False), "austin_contacts_backup.csv", "text/csv")
    st.caption("Enter meetings once in Google Sheets, then refresh here. The app calculates follow-up actions without creating a second contact database.")

st.markdown("""
<div class="hero" style="background:linear-gradient(120deg,#0b3954,#087e8b);color:white;padding:2rem;border-radius:18px;margin-bottom:1rem">
<div style="text-transform:uppercase;letter-spacing:.12em;font-size:.8rem;color:#a7f3d0">Weekly command center</div>
<h1>Austin Nielsen</h1>
<p><b>Business Management</b> × <b>Industrial-Organizational Psychology</b></p>
<p>One source of truth for contacts; one action layer for follow-ups, evidence, and milestones.</p>
</div>
""", unsafe_allow_html=True)

contacts = normalize_contacts(st.session_state.contacts)
contacts["Last Contact"] = pd.to_datetime(contacts["Last Contact"], errors="coerce")
contacts["Days Since Contact"] = contacts["Last Contact"].apply(lambda x: (TODAY - x).days if pd.notna(x) else pd.NA)
contacts["Follow-up Due"] = contacts["Last Contact"].apply(lambda x: x + pd.Timedelta(days=56) if pd.notna(x) else pd.NaT)
def cadence(row):
    if pd.isna(row["Last Contact"]): return "No date"
    days = int(row["Days Since Contact"])
    if days >= 56: return "Overdue"
    if days >= 42: return "Due soon"
    return "Active"
contacts["Cadence"] = contacts.apply(cadence, axis=1)
completed = int(contacts["Status"].str.lower().isin(["completed", "re-engaged"]).sum())
overdue = contacts[contacts["Cadence"] == "Overdue"]
due_soon = contacts[contacts["Cadence"] == "Due soon"]
dates = contacts["Last Contact"].dropna()
weeks = max(1, int(((TODAY - dates.min()).days / 7) if len(dates) else 1))
pace = completed / weeks
remaining = max(0, 50 - completed)
projected_days = int((remaining / pace) * 7) if pace > 0 else 0

k1, k2, k3, k4 = st.columns(4)
k1.metric("Contacts in source sheet", len(contacts))
k2.metric("Completed conversations", f"{completed}/50", f"{pace:.1f} per week")
k3.metric("Follow-ups due", len(overdue), f"{len(due_soon)} due soon")
k4.metric("Source", st.session_state.source_name)

home_tab, network_tab, skills_tab, roadmap_tab = st.tabs(["Command Center", "Networking CRM", "Skills & Evidence", "Roadmap"])
with home_tab:
    st.subheader("This week’s operating picture")
    st.progress(min(completed / 50, 1.0), text=f"Career chat progress: {completed}/50 • Current pace: {pace:.1f} per week")
    if pace > 0:
        st.caption(f"At the current pace, the remaining {remaining} conversations would take about {projected_days // 30} months. This is a planning estimate, not a promise.")
    if overdue.empty:
        st.success("No follow-ups are overdue.")
    else:
        st.warning(f"{len(overdue)} follow-up action(s) are overdue under the 8-week cadence.")
        st.dataframe(overdue[["Contact", "Method", "Homework Anchor", "Next Action", "Days Since Contact"]], use_container_width=True, hide_index=True)
        names = overdue["Contact"].tolist()
        selected = st.selectbox("Generate a follow-up draft", names)
        person = overdue[overdue["Contact"] == selected].iloc[0]
        draft = f"Hi {selected}, I’ve been thinking about our conversation and your recommendation to focus on {person['Homework Anchor']}. I wanted to share a quick update and thank you for the guidance. Would you be open to reconnecting for a brief follow-up?"
        st.code(draft, language="text")
    st.info("Workflow: log the meeting once in Google Sheets → refresh this app → review cadence → copy the generated draft → update the sheet after outreach.")

with network_tab:
    st.subheader("Networking CRM view")
    st.caption("The Google Sheet is the editable record. This view adds calculated cadence and action fields so you do not maintain two separate databases.")
    search = st.text_input("Search contacts, organizations, or actions", placeholder="Try: psychology or SLC")
    view = contacts.copy()
    if search:
        mask = view.astype(str).apply(lambda row: row.str.contains(search, case=False, na=False).any(), axis=1)
        view = view[mask]
    st.dataframe(view[["Contact", "Category", "Organization", "Method", "Status", "Priority", "Cadence", "Next Action", "Key Takeaway"]], use_container_width=True, hide_index=True)

with skills_tab:
    st.subheader("Skills connected to evidence")
    skills = pd.DataFrame({"Skill":["Business Operations","I-O Psychology","AI Prompt Engineering","Process Optimization","Team Assessment Design"], "Proficiency":[82,76,68,73,64]}).set_index("Skill")
    st.bar_chart(skills, y="Proficiency", horizontal=True, use_container_width=True)
    st.caption("These scores are planning estimates. Update them when you can point to a course, project, interview takeaway, or deliverable.")

with roadmap_tab:
    st.subheader("President Meredith readiness roadmap")
    milestones = pd.DataFrame([
        {"Milestone":"Student Leadership Council deliverable", "Target":"Winter–Fall 2027", "Domain":"SLC Governance", "Status":"Not Started", "Evidence":"Policy or process improvement with measurable campus impact"},
        {"Milestone":"Academic TA-ship", "Target":"Fall 2027–Winter 2028", "Domain":"Academic TA-ship", "Status":"Not Started", "Evidence":"Teaching, research, or faculty-supported project evidence"},
        {"Milestone":"Senior administrative endorsements", "Target":"Winter 2028", "Domain":"Administrative Endorsement", "Status":"Not Started", "Evidence":"Relationships with Dean Greenwood, Tim Rarick, and SLC advisors"},
        {"Milestone":"President Meredith meeting", "Target":"March / April 2028", "Domain":"Presidential Briefing", "Status":"Not Started", "Evidence":"One-page briefing with governance findings and career vision"},
    ])
    st.dataframe(milestones, use_container_width=True, hide_index=True)
    st.progress(0, text="0 of 3 preparation milestones complete")
    st.info("Keep Google Sheets for the record. Use this roadmap to decide what evidence you need to create next.")

st.divider()
st.caption("Architecture: Google Sheets source of truth + Streamlit executive action layer. The app does not send messages or alter your sheet; it calculates and drafts next actions.")
