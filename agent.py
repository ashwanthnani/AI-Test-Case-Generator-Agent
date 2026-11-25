from test_case_generator import generate_test_cases

def plan_requirement(requirement):
    text = requirement.lower()
    if any(x in text for x in ["login", "sign in", "password", "authentication"]):
        analysis = "Authentication feature: valid and invalid credentials, missing inputs, and boundary conditions."
    elif any(x in text for x in ["register", "registration", "sign up", "signup"]):
        analysis = "Registration feature: valid details, missing fields, invalid formats, duplicates, and boundaries."
    elif any(x in text for x in ["search", "filter"]):
        analysis = "Search feature: matching results, no results, invalid input, and boundaries."
    else:
        analysis = "General feature: successful use, invalid or missing inputs, and edge conditions."
    return {"analysis": analysis, "scenario_types": ["Positive", "Negative", "Edge Case"]}

def run_agent(requirement, model, count):
    plan = plan_requirement(requirement)
    result = generate_test_cases(requirement, model, count, plan)
    result["analysis"] = plan["analysis"]
    return result
