# app1.py
import streamlit as st
import os
from contract_analyzer import analyze_contract
from risk_engine import calculate_risk
from utils import extract_text, highlight_clauses
from dotenv import load_dotenv
import pandas as pd
import plotly.express as px

# -------------------------
# Load environment variables for local testing
load_dotenv()

# -------------------------
# OpenAI client with fallback
try:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception:
    client = None
    st.warning("OpenAI API key not found. Running in demo mode.")

# -------------------------
# Password protection
PASSWORD = "Demo2026!"  # change as needed

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    # Display password input
    pwd_input = st.text_input("Enter demo password:", type="password")
    if pwd_input == PASSWORD:
        st.session_state.authenticated = True
        st.success("✅ Access Granted")
        st.experimental_rerun()  # Immediately rerun app to load main pages
    elif pwd_input != "":
        st.error("❌ Incorrect password")
else:
    # -------------------------
    # Main App Layout
    st.set_page_config(page_title="AI Banking Contract Risk Platform", layout="wide")
    st.title("🔒 AI Banking Contract Risk & Compliance Platform")

    # Sidebar menu
    menu = st.sidebar.selectbox(
        "Navigation",
        ["Upload Contract", "AI Analysis", "Risk Dashboard", "Portfolio Insights"]
    )

    # Initialize session state variables
    for key in ["contract_text", "analysis_result", "risk_score", "highlights"]:
        if key not in st.session_state:
            st.session_state[key] = None

    # -------------------------
    # Upload Contract Page
    if menu == "Upload Contract":
        st.header("Upload Contract")
        uploaded_file = st.file_uploader("Upload PDF or Word file", type=["pdf", "docx"])
        if uploaded_file:
            text = extract_text(uploaded_file)
            st.session_state.contract_text = text
            st.session_state.highlights = highlight_clauses(text)
            st.subheader("Contract Preview (First 1500 chars)")
            st.write(text[:1500])

    # -------------------------
    # AI Analysis Page
    elif menu == "AI Analysis":
        st.header("AI Contract Analysis")
        if not st.session_state.contract_text:
            st.warning("Upload a contract first.")
        else:
            # Run analysis automatically without button click
            result = analyze_contract(st.session_state.contract_text)
            st.session_state.analysis_result = result
            st.subheader("Structured Contract Data")
            st.json(result)
            st.session_state.risk_score = calculate_risk(result)

    # -------------------------
    # Risk Dashboard
    elif menu == "Risk Dashboard":
        st.header("Risk Dashboard")
        risk = st.session_state.risk_score or 0
        st.metric("Overall Risk Score", risk)
        if risk >= 70:
            st.error("High Risk Contract")
        elif risk >= 40:
            st.warning("Medium Risk Contract")
        else:
            st.success("Low Risk Contract")

        # Risk Breakdown Chart
        categories = ["Legal", "Financial", "Compliance"]
        values = [risk * 0.4, risk * 0.3, risk * 0.3]
        df = pd.DataFrame({"Category": categories, "Score": values})
        fig = px.bar(df, x="Category", y="Score", color="Category", text="Score")
        st.plotly_chart(fig)

    # -------------------------
    # Portfolio Insights Page
    elif menu == "Portfolio Insights":
        st.header("Contract Portfolio Monitoring")
        portfolio_data = pd.DataFrame({
            "Client": ["Startup A", "Startup B", "Startup C"],
            "Industry": ["Fintech", "Healthcare", "SaaS"],
            "Risk Score": [45, 72, 30]
        })
        st.dataframe(portfolio_data)

        dist = pd.DataFrame({"Risk Level": ["Low", "Medium", "High"], "Contracts": [5, 3, 2]})
        fig2 = px.bar(dist, x="Risk Level", y="Contracts", color="Risk Level", text="Contracts")
        st.plotly_chart(fig2)