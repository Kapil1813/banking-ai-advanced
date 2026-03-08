from openai import OpenAI
import json, os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_contract(contract_text):
    prompt = f"""
You are an expert banking compliance analyst.

Analyze the following contract and:

1. Extract structured clauses:
- Payment Terms
- Liability Clause
- Compliance Requirements
- Renewal Terms
- Penalties
- Key Risks

2. Generate a short human-readable summary highlighting obligations, risks, and compliance.

Return JSON like:
{{
    "payment_terms": "...",
    "liability_clause": "...",
    "compliance_requirements": "...",
    "renewal_terms": "...",
    "penalties": "...",
    "key_risks": "...",
    "summary": "..."
}}
Contract:
{contract_text}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":prompt}]
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except:
        # Demo fallback if API fails
        return {
            "payment_terms":"Demo: 12 monthly installments, 5% interest",
            "liability_clause":"Demo: Limited liability to outstanding loan",
            "compliance_requirements":"Demo: Quarterly reports, AML/KYC compliance",
            "renewal_terms":"Demo: Auto-renewal with 90 days notice",
            "penalties":"Demo: Late payment penalty 2%",
            "key_risks":"Demo: Market volatility, currency fluctuations",
            "summary":"Demo summary: Borrower must follow payment and compliance obligations."
        }