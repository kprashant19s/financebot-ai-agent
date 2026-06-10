from viz.chart_generator import generate_chart
from agent.agent import run_agent
import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


st.set_page_config(
    page_title="FinanceBot — AI Data Insights",
    page_icon="💰",
    layout="wide"
)

st.title("💰 FinanceBot — Autonomous Data Insights Agent")
st.markdown("Ask any question about your finance data in plain English.")

# Sidebar with example questions
with st.sidebar:
    st.header("💡 Example Questions")
    examples = [
        "What are the top 3 expense categories by total amount?",
        "Show total expenses by month for 2024",
        "Compare budget vs actual spending for groceries",
        "Which month had the highest savings in 2024?",
        "What percentage of income went to dining out in February 2024?",
        "Show me the top 5 largest transactions",
        "Which category overspent the budget in October 2024?",
        "What is the total balance across all accounts?"
    ]
    for example in examples:
        if st.button(example, use_container_width=True):
            st.session_state.question = example

    st.markdown("---")
    st.markdown("**Tech Stack**")
    st.markdown("🤖 LLaMA 3.3 70B via Groq")
    st.markdown("🗄️ MySQL 8.0")
    st.markdown("🐍 Python + LangChain")
    st.markdown("📊 Plotly")

# Main input
question = st.text_input(
    "Your question:",
    value=st.session_state.get("question", ""),
    placeholder="e.g. Which category had the highest spending in 2024?",
    key="input"
)

if st.button("Ask FinanceBot", type="primary", use_container_width=True):
    if not question:
        st.warning("Please enter a question.")
    else:
        with st.spinner("Generating SQL and fetching results..."):
            result = run_agent(question)

        if not result["success"]:
            st.error(f"❌ {result['error']}")
        else:
            # Show generated SQL
            with st.expander("🔍 Generated SQL Query"):
                st.code(result["sql"], language="sql")

            # Show results
            st.subheader("📋 Results")

            data = result["data"]

            if data.empty:
                st.info("No data found for this question.")
            else:
                # Single value answer
                rows, cols = data.shape
                if rows == 1 and cols == 1:
                    value = data.iloc[0, 0]
                    col_name = data.columns[0]
                    st.metric(label=col_name, value=f"{value:,.2f}")
                else:
                    # Show chart and table side by side
                    col1, col2 = st.columns([3, 2])

                    with col1:
                        st.subheader("📊 Chart")
                        fig = generate_chart(data, question)
                        if fig:
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.info("No chart available for this result.")

                    with col2:
                        st.subheader("📄 Data Table")
                        st.dataframe(data, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Built with LangChain · Groq · MySQL · Plotly · Streamlit")
