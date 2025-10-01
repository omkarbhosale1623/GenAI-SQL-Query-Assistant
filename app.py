import streamlit as st
from sqlalchemy import create_engine
from config import DATABASE_URI
from utills import get_db_schema, call_euri_llm, execute_sql
import speech_recognition as sr
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="SQL Assistant + Dashboard", layout="wide")
st.title("🧠 SQL-Powered Data Assistant & Dashboard")

# ----------------------------
# Step 1: Choose Input Language
# ----------------------------
st.sidebar.subheader("🌐 Choose Language")
language_map = {
    "English (US)": "en-US", "Hindi (India)": "hi-IN", "Spanish": "es-ES",
    "French": "fr-FR", "German": "de-DE", "Chinese": "zh-CN",
    "Arabic": "ar-SA", "Bengali": "bn-IN", "Japanese": "ja-JP",
    "Tamil": "ta-IN", "Telugu": "te-IN", "Marathi": "mr-IN"
}
selected_language = st.sidebar.selectbox("Language", list(language_map.keys()))
language_code = language_map[selected_language]

# ----------------------------
# Step 2: Speech Input
# ----------------------------
st.subheader("🎙️ Speak or Type Your Query")
nl_query = ""
if st.button("🎤 Start Listening"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info(f"Listening in {selected_language}... Speak now.")
        audio = recognizer.listen(source, timeout=7)

    try:
        nl_query = recognizer.recognize_google(audio, language=language_code)
        st.success(f"You said: {nl_query}")
    except sr.UnknownValueError:
        st.error("Sorry, I couldn't understand the audio.")
    except sr.RequestError as e:
        st.error(f"Speech Recognition API error: {e}")
else:
    nl_query = st.text_input("Or type your question here:")

# ----------------------------
# Step 3: Process NL → SQL → Results
# ----------------------------
if nl_query:
    engine = create_engine(DATABASE_URI)
    schema = get_db_schema(engine)

    with open("prompt_template.txt") as f:
        template = f.read()
    prompt = template.format(schema=schema, question=nl_query)

    with st.spinner("🧠 Generating SQL using EURI LLM..."):
        sql_query = call_euri_llm(prompt)

    st.code(sql_query, language="sql")

    try:
        results, columns = execute_sql(engine, sql_query)
        if results:
            df = pd.DataFrame(results, columns=columns)

            # ----------------------------
            # Step 4: Dashboard KPIs
            # ----------------------------
            st.subheader("📊 Dashboard KPIs")
            col1, col2, col3, col4 = st.columns(4)
            with col1: st.metric("Total Rows", f"{len(df):,}")
            with col2: 
                if "revenue" in df.columns: st.metric("Total Revenue", f"${df['revenue'].sum():,.2f}")
            with col3:
                if "customer" in df.columns: st.metric("Unique Customers", df['customer'].nunique())
            with col4:
                if "order_id" in df.columns: st.metric("Total Orders", df['order_id'].nunique())

            # ----------------------------
            # Step 5: Data Table
            # ----------------------------
            st.subheader("📋 Query Results")
            st.dataframe(df, use_container_width=True)

            # ----------------------------
            # Step 6: Visualization
            # ----------------------------
            st.subheader("📈 Visualization Dashboard")

            if "date" in df.columns[0].lower() or "time" in df.columns[0].lower():
                fig = px.line(df, x=df.columns[0], y=df.columns[1], title="Trend Over Time")
                st.plotly_chart(fig, use_container_width=True)
            elif df.shape[1] == 2:
                fig = px.bar(df, x=df.columns[0], y=df.columns[1], title="Bar Chart")
                st.plotly_chart(fig, use_container_width=True)
            elif df.shape[1] == 3:
                fig = px.scatter(df, x=df.columns[0], y=df.columns[1], color=df.columns[2], title="Scatter Plot")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Visualization not auto-detected — please refine your query.")

            # ----------------------------
            # Step 7: Personalized Custom Chart
            # ----------------------------
            st.subheader("🎨 Your Custom Chart")
            chart_type = st.selectbox("Pick a Chart Type", ["Bar", "Line", "Pie", "Scatter"])

            if chart_type == "Bar":
                fig = px.bar(df, x=df.columns[0], y=df.columns[1])
            elif chart_type == "Line":
                fig = px.line(df, x=df.columns[0], y=df.columns[1])
            elif chart_type == "Pie" and df.shape[1] >= 2:
                fig = px.pie(df, names=df.columns[0], values=df.columns[1])
            elif chart_type == "Scatter" and df.shape[1] >= 3:
                fig = px.scatter(df, x=df.columns[0], y=df.columns[1], color=df.columns[2])
            else:
                fig = None

            if fig: st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("✅ Query executed successfully. No data returned.")
    except Exception as e:
        st.error(f"❌ Error running query: {e}")
