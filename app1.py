# app.py
import streamlit as st
from utils import extract_text, highlight_clauses
from contract_analyzer import analyze_contract
from risk_engine import calculate_risk

# --- Password protection ---
st.set_page_config(page_title="AI Banking Contract Risk Platform", layout="wide")
st.title("🔒 Secure AI Banking Contract Demo")

# Simple password
PASSWORD = "Demo2026!"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    pwd_input = st.text_input("Enter demo password:", type="demo123")
    if st.button("Login"):
        if pwd_input == PASSWORD:
            st.session_state.authenticated = True
            st.success("✅ Access Granted")
        else:
            st.error("❌ Incorrect password")
else:
    # --- Main App ---
    menu = st.sidebar.selectbox(
        "Navigation",
        ["Upload Contract", "AI Analysis", "Risk Dashboard", "Portfolio Insights"]
    )

    # Session State
    for key in ["contract_text","analysis_result","risk_score","highlights"]:
        if key not in st.session_state:
            st.session_state[key] = None

    # Upload Page
    if menu=="Upload Contract":
        st.header("Upload Contract")
        uploaded_file = st.file_uploader("Upload PDF or Word", type=["pdf","docx"])
        if uploaded_file:
            text = extract_text(uploaded_file)
            st.session_state.contract_text = text
            st.session_state.highlights = highlight_clauses(text)
            st.subheader("Contract Preview")
            st.write(text[:1500])

    # AI Analysis Page
    elif menu=="AI Analysis":
        st.header("AI Contract Analysis")
        if not st.session_state.contract_text:
            st.warning("Upload a contract first.")
        else:
            if st.button("Run AI Analysis"):
                result = analyze_contract(st.session_state.contract_text)
                st.session_state.analysis_result = result
                st.subheader("Structured Contract Data")
                st.json(result)
                st.session_state.risk_score = calculate_risk(result)

    # Risk Dashboard
    elif menu=="Risk Dashboard":
        st.header("Risk Dashboard")
        risk = st.session_state.risk_score or 0
        st.metric("Overall Risk Score", risk)
        if risk>=70:
            st.error("High Risk Contract")
        elif risk>=40:
            st.warning("Medium Risk Contract")
        else:
            st.success("Low Risk Contract")
        # Risk Breakdown Chart
        import pandas as pd
        import plotly.express as px
        categories = ["Legal","Financial","Compliance"]
        values = [risk*0.4, risk*0.3, risk*0.3]
        df = pd.DataFrame({"Category":categories,"Score":values})
        fig = px.bar(df, x="Category", y="Score", color="Category", text="Score")
        st.plotly_chart(fig)

    # Portfolio Insights
    elif menu=="Portfolio Insights":
        st.header("Contract Portfolio Monitoring")
        portfolio_data = pd.DataFrame({
            "Client":["Startup A","Startup B","Startup C"],
            "Industry":["Fintech","Healthcare","SaaS"],
            "Risk Score":[45,72,30]
        })
        st.dataframe(portfolio_data)
        dist = pd.DataFrame({"Risk Level":["Low","Medium","High"],"Contracts":[5,3,2]})
        fig2 = px.bar(dist, x="Risk Level", y="Contracts", color="Risk Level", text="Contracts")
        st.plotly_chart(fig2)