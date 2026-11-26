import streamlit as st
import pandas as pd
from datetime import date, timedelta

st.set_page_config(page_title="Austin Nielsen | Operations Hub", page_icon="🎓", layout="wide")

st.markdown("""
<style>
.stApp { background: #f4f7fb; color: #102a43; }
[data-testid="stSidebar"] { background: #102a43; }
[data-testid="stSidebar"] * { color: white; }
.hero { background: linear-gradient(120deg,#0b3954,#087e8b); color:white; padding:2rem; border-radius:18px; margin-bottom:1rem; }
.hero h1 { margin:0; font-size:2.5rem; }
</style>
""", unsafe_allow_html=True)

TODAY = pd.Timestamp(date.today())

DEFAULT_CONTACTS = [
    {"Contact":"Sister Paulette Kirkham", "Category":"Faculty", "Organization":"Leadership Communication", "Method":"In-person", "Last Contact":"2026-11-17", "Status":"Completed", "Priority":"High", "Next Action":"Request warm intro to Brother Tim Rarick or Dean Greenwood", "Key Takeaway":"Create conditions where people choose to thrive."},
    {"Contact":"Bob Morley", "Category":"Industry practitioner", "Organization":"Strategy & Training Consulting", "Method":"In-person", "Last Contact":"", "Status":"Follow-up due", "Priority":"High", "Next Action":"Share a short update and ask about consulting contacts", "Key Takeaway":"Translate analysis into decisions leaders can act on."},
    {"Contact":"Jared Stanger", "Category":"Industry practitioner", "Organization":"Healthcare AI & Lean", "Method":"Text / WhatsApp", "Last Contact":"2026-11-19", "Status":"Outreach Sent", "Priority":"High", "Next Action":"Send a brief follow-up about AI and process optimization", "Key Takeaway":"Pair responsible AI with measurable process improvement."},
    {"Contact":"Amy Staiger", "Category":"Academic advising", "Organization":"Academic Advising", "Method":"In-person", "Last Contact":"", "Status":"Completed", "Priority":"Medium", "Next Action":"Review flex-track courses and peer-advisor opportunities", "Key Takeaway":"Good systems make student progress easier to navigate."},
    {"Contact":"Dean Janelle Greenwood", "Category":"Campus administration", "Organization":"Health & Human Sciences", "Method":"Email", "Last Contact":"", "Status":"Planned", "Priority":"High", "Next Action":"Request a 15-minute conversation about institutional leadership", "Key Takeaway":"Learn how campus systems support student success."},
    {"Contact":"Brother Tim Rarick", "Category":"Faculty / mentor", "Organization":"UN Student Delegation", "Method":"Email", "Last Contact":"", "Status":"Planned", "Priority":"High", "Next Action":"Ask about the UN delegation and leadership opportunities", "Key Takeaway":"Explore practical leadership experience with campus impact."},
    {"Contact":"Brother Johan Delton", "Category":"Faculty", "Organization":"I-O Psychology", "Method":"Email", "Last Contact":"", "Status":"Planned", "Priority":"Medium", "Next Action":"Ask about I-O career pathways and graduate preparation", "KeyTakeaway":"Connect coursework to evidence-based people strategy."},
    {"Contact":"Brother Devin Merritt", "Category":"Faculty", "Organization":"I-O Psychology", "Method":"Email", "Last Contact":"", "Status":"Planned", "Priority":"High", "Next Action":"Ask about PSYCH 445 and future TA opportunities", "Key Takeaway":"Build academic authority through hands-on teaching experience."},
    {"Contact":"Savannah Presby", "Category":"Student leadership", "Organization":"Student Leadership Council", "Method":"Email", "Last Contact":"", "Status":"Planned", "Priority":"Medium", "Next Action":"Check on SLC application and committee placement", "Key Takeaway":"Turn governance access into measurable process improvement."},
]

# Repair one spelling in the seed data without hiding it from the user.
DEFAULT_CONTACTS[6]["Key Takeaway"] = "Connect coursework to evidence-based people strategy."

if "contacts" not in st.session_state:
    st.session_state.contacts = pd.DataFrame(DEFAULT_CONTACTS)

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
    st.subheader("Data controls")
    upload = st.file_uploader("Load a saved contacts CSV", type="csv")
    if upload is not None:
        st.session_state.contacts = pd.read_csv(upload).fillna("")
        st.success("Contacts loaded for this session.")
    st.download_button("Download contacts CSV", st.session_state.contacts.to_csv(index=False), "austin_contacts.csv", "text/csv")
    st.caption("New entries are session-based. Export the CSV to keep a backup; a future version can connect Google Sheets or Firebase for permanent storage.")

st.markdown("""
<div class="hero">
<div style="text-transform:uppercase;letter-spacing:.12em;font-size:.8rem;color:#a7f3d0">Weekly command center</div>
<h1>Austin Nielsen</h1>
<p><b>Business Management</b> × <b>Industrial-Organizational Psychology</b></p>
<p>Turn every conversation into a next action, every course into evidence, and every milestone into a plan.</p>
</div>
""", unsafe_allow_html=True)

contacts = st.session_state.contacts.copy().fillna("")
contacts["Last Contact"] = pd.to_datetime(contacts["Last Contact"], errors="coerce")
contacts["Follow-up Due"] = contacts["Last Contact"].apply(lambda x: x + pd.Timedelta(days=56) if pd.notna(x) else pd.NaT)
contacts["Days Since Contact"] = contacts["Last Contact"].apply(lambda x: (TODAY - x).days if pd.notna(x) else pd.NA)
contacts["Follow-up Flag"] = contacts.apply(lambda r: "Due" if r["Status"] == "Follow-up due" or (pd.notna(r["Follow-up Due"]) and r["Follow-up Due"] <= TODAY) else "On track", axis=1)

completed = int(contacts["Status"].isin(["Completed", "Re-engaged"]).sum())
followups = int((contacts["Follow-up Flag"] == "Due").sum())
planned = int((contacts["Status"] == "Planned").sum())
readiness = "0/3"

k1, k2, k3, k4 = st.columns(4)
k1.metric("Contacts in pipeline", len(contacts))
k2.metric("Completed conversations", completed, f"{completed}/50 goal")
k3.metric("Follow-ups needing action", followups)
k4.metric("Spring 2028 readiness", readiness)

home_tab, network_tab, skills_tab, roadmap_tab = st.tabs(["Command Center", "Networking CRM", "Skills & Evidence", "Roadmap"])

with home_tab:
    st.subheader("This week’s operating picture")
    due = contacts[contacts["Follow-up Flag"] == "Due"]
    if due.empty:
        st.success("No follow-ups are currently flagged. Add dates after each meeting to activate the 8-week cadence.")
    else:
        st.warning(f"{len(due)} follow-up action(s) need attention.")
        st.dataframe(due[["Contact", "Priority", "Next Action", "Status"]], use_container_width=True, hide_index=True)
    st.subheader("Next best actions")
    actions = contacts[contacts["Status"].isin(["Planned", "Follow-up due"])].sort_values(["Priority", "Contact"], ascending=[True, True])
    st.dataframe(actions[["Contact", "Organization", "Next Action", "Priority"]].head(6), use_container_width=True, hide_index=True)
    st.info("Workflow: meet → record takeaway → choose next action → set last-contact date → return when the follow-up flag turns Due.")

with network_tab:
    st.subheader("Networking CRM")
    st.caption("This is the useful core: a contact record, a follow-up cadence, and one concrete next action.")
    filter_text = st.text_input("Search contacts, organizations, or actions", placeholder="Try: psychology or SLC")
    view = contacts.copy()
    if filter_text:
        mask = view.astype(str).apply(lambda row: row.str.contains(filter_text, case=False, na=False).any(), axis=1)
        view = view[mask]
    editable_cols = ["Contact", "Category", "Organization", "Method", "Last Contact", "Status", "Priority", "Next Action", "Key Takeaway"]
    edited = st.data_editor(view[editable_cols], use_container_width=True, hide_index=True, num_rows="dynamic", key="contact_editor")
    if not edited.equals(view[editable_cols]):
        if filter_text:
            contacts.loc[view.index, editable_cols] = edited.values
        else:
            contacts = edited.copy()
        st.session_state.contacts = contacts[editable_cols].fillna("")
        st.rerun()
    with st.expander("Add a new contact or meeting"):
        with st.form("add_contact_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            name = c1.text_input("Contact name")
            organization = c2.text_input("Role or organization")
            c3, c4, c5 = st.columns(3)
            category = c3.selectbox("Category", ["Faculty", "Campus administration", "Industry practitioner", "Student leadership", "Personal connection"])
            method = c4.selectbox("Contact method", ["In-person", "Email", "LinkedIn", "Text / WhatsApp"])
            last_contact = c5.date_input("Last contact date", value=None)
            status = st.selectbox("Status", ["Planned", "Outreach Sent", "Completed", "Follow-up due", "Re-engaged"])
            priority = st.selectbox("Priority", ["High", "Medium", "Low"])
            next_action = st.text_input("Next action")
            takeaway = st.text_area("Key takeaway")
            submitted = st.form_submit_button("Add to pipeline")
            if submitted and name.strip():
                new_row = {"Contact":name.strip(), "Category":category, "Organization":organization.strip(), "Method":method, "Last Contact":str(last_contact) if last_contact else "", "Status":status, "Priority":priority, "Next Action":next_action.strip(), "Key Takeaway":takeaway.strip()}
                st.session_state.contacts = pd.concat([st.session_state.contacts, pd.DataFrame([new_row])], ignore_index=True)
                st.success(f"Added {name.strip()} to the pipeline.")
                st.rerun()

with skills_tab:
    st.subheader("Skills connected to evidence")
    skills = pd.DataFrame({"Skill":["Business Operations","I-O Psychology","AI Prompt Engineering","Process Optimization","Team Assessment Design"], "Proficiency":[82,76,68,73,64]}).set_index("Skill")
    st.bar_chart(skills, y="Proficiency", horizontal=True, use_container_width=True)
    st.caption("Update these scores only when you can point to evidence: a course, project, interview takeaway, or deliverable.")

with roadmap_tab:
    st.subheader("President Meredith readiness roadmap")
    milestones = pd.DataFrame([
        {"Milestone":"Student Leadership Council deliverable", "Target":"Winter–Fall 2027", "Domain":"SLC Governance", "Status":"Not Started", "Evidence to collect":"Policy or process improvement with measurable campus impact"},
        {"Milestone":"Academic TA-ship", "Target":"Fall 2027–Winter 2028", "Domain":"Academic TA-ship", "Status":"Not Started", "Evidence to collect":"Teaching, research, or faculty-supported project evidence"},
        {"Milestone":"Senior administrative endorsements", "Target":"Winter 2028", "Domain":"Administrative Endorsement", "Status":"Not Started", "Evidence to collect":"Relationships with Dean Greenwood, Tim Rarick, and SLC advisors"},
        {"Milestone":"President Meredith meeting", "Target":"March / April 2028", "Domain":"Presidential Briefing", "Status":"Not Started", "Evidence to collect":"One-page briefing: governance findings, interdisciplinary model, career vision"},
    ])
    st.dataframe(milestones, use_container_width=True, hide_index=True)
    st.progress(0, text="0 of 3 preparation milestones complete")
    st.info("The meeting is the destination; the SLC deliverable, TA-ship, and senior endorsements are the preparation evidence.")

st.divider()
st.caption("Cloud app: Streamlit Community Cloud + GitHub. Current data entry is session-based with CSV export; persistent storage is the next upgrade.")
