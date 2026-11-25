import json, re
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from prompts import SYSTEM_PROMPT

FIELDS = ["Test Case ID","Title","Scenario Type","Preconditions","Steps","Test Data","Expected Result","Priority"]

def generate_test_cases(requirement, model, count, plan):
    llm = ChatOllama(model=model, temperature=0.2, format="json")
    prompt = f"Requirement: {requirement}\nAgent analysis: {plan['analysis']}\nGenerate up to {count} distinct cases."
    response = llm.invoke([SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=prompt)])
    raw = response.content.strip()
    raw = re.sub(r"^```(?:json)?\\s*|\\s*```$", "", raw)
    start, end = raw.find("{"), raw.rfind("}")
    if start < 0 or end < 0:
        raise ValueError("The model did not return valid JSON. Try again.")
    data = json.loads(raw[start:end+1])
    if not isinstance(data.get("test_cases"), list):
        raise ValueError("The model response has no test_cases list.")
    cleaned = []
    for i, case in enumerate(data["test_cases"][:count], 1):
        row = {k: str(case.get(k, "")).strip() for k in FIELDS}
        if not row["Title"] or not row["Steps"] or not row["Expected Result"]:
            continue
        row["Test Case ID"] = f"TC-{i:02d}"
        if row["Priority"] not in ["High","Medium","Low"]:
            row["Priority"] = "Medium"
        if row["Scenario Type"] not in ["Positive","Negative","Edge Case","Other"]:
            row["Scenario Type"] = "Other"
        cleaned.append(row)
    if not cleaned:
        raise ValueError("No valid test cases generated. Rephrase your requirement.")
    return {"analysis": str(data.get("analysis", "")),
            "assumptions": data.get("assumptions", []) if isinstance(data.get("assumptions", []), list) else [],
            "test_cases": cleaned}
