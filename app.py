import streamlit as st
import pandas as pd
from agent import run_agent
from database import init_db, save_run, get_history, get_run, delete_run
from export_utils import to_csv

st.set_page_config(page_title="AI Test Case Generator Agent", page_icon="🧪", layout="wide")
init_db()
st.title("🧪 AI Test Case Generator Agent")
st.caption("Convert plain-English requirements into editable manual test cases.")
with st.sidebar:
    st.header("Model settings")
    model = st.text_input("Ollama model", "llama3.2:3b")
    st.info("Review AI-generated cases before using them for real software testing.")
tab1, tab2 = st.tabs(["Generate test cases", "Saved history"])
with tab1:
    requirement = st.text_area("Software requirement", height=140, placeholder="A user should be able to register using name, email, and password.")
    count = st.selectbox("Number of test cases", [5, 8, 10, 12], index=1)
    if st.button("Generate test cases", type="primary"):
        if len(requirement.strip()) < 15:
            st.warning("Please enter a clear requirement of at least 15 characters.")
        else:
            with st.spinner("Agent is analysing and generating test cases..."):
                try:
                    result = run_agent(requirement.strip(), model, count)
                    st.session_state["req"] = requirement.strip()
                    st.session_state["cases"] = result["test_cases"]
                    st.session_state["analysis"] = result["analysis"]
                    st.session_state["assumptions"] = result.get("assumptions", [])
                except Exception as e:
                    st.error(f"Generation failed: {e}")
                    st.info("Confirm Ollama is running and the selected model is downloaded.")
    if "cases" in st.session_state:
        st.subheader("Agent analysis")
        st.write(st.session_state.get("analysis", ""))
        if st.session_state.get("assumptions"):
            st.warning("Assumptions: " + "; ".join(st.session_state["assumptions"]))
        st.subheader("Review, edit or delete rows")
        edited = st.data_editor(pd.DataFrame(st.session_state["cases"]), use_container_width=True,
                                hide_index=True, num_rows="dynamic", key="editor")
        st.session_state["cases"] = edited.fillna("").to_dict("records")
        a, b = st.columns(2)
        with a:
            if st.button("Save to history", type="primary"):
                rid = save_run(st.session_state["req"], st.session_state["cases"])
                st.success(f"Saved record #{rid}")
        with b:
            st.download_button("Download CSV", to_csv(st.session_state["cases"]),
                               "generated_test_cases.csv", "text/csv")
with tab2:
    st.subheader("Saved history")
    history = get_history()
    if not history:
        st.info("No saved records yet.")
    for item in history:
        with st.expander(f"#{item['id']} — {item['created_at']}"):
            st.write("Requirement:", item["requirement"])
            cases = get_run(item["id"])
            st.dataframe(pd.DataFrame(cases), use_container_width=True, hide_index=True)
            c1, c2 = st.columns(2)
            with c1:
                st.download_button("Download CSV", to_csv(cases), f"test_cases_{item['id']}.csv",
                                   "text/csv", key=f"dl{item['id']}")
            with c2:
                if st.button("Delete record", key=f"del{item['id']}"):
                    delete_run(item["id"])
                    st.rerun()
