def calculate_risk(contract_data):
    score = 0
    text = " ".join(contract_data.values()).lower()
    if "unlimited liability" in text:
        score += 35
    if "auto renewal" in text:
        score += 20
    if "penalty" in text or "late payment" in text:
        score += 15
    if "regulatory" in text or "compliance" in text:
        score += 10
    if "termination notice 90" in text:
        score += 10
    return min(score, 100)