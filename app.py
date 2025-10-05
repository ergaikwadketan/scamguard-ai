import streamlit as st
import pandas as pd
from llm_utils import classify_message, extract_scam_type, generate_explanation

st.title("ScamGuard AI - Scam Message Detection")

# Single message analysis
user_message = st.text_area("Enter a message to analyze:")

if st.button("Analyze Message"):
    if not user_message.strip():
        st.warning("Please enter a message for analysis.")
    else:
        with st.spinner("Analyzing..."):
            classification = classify_message(user_message)
            scam_type = extract_scam_type(user_message) if classification == "scam" else "N/A"
            explanation = generate_explanation(user_message)
        st.write(f"**Classification:** {classification.capitalize()}")
        st.write(f"**Scam Type:** {scam_type.capitalize()}")
        st.write(f"**Explanation:** {explanation}")

st.markdown("---")

# Batch CSV analysis
uploaded_file = st.file_uploader("Upload CSV file with a 'message_text' column for batch processing", type=["csv"])

max_entries = st.number_input("Max messages to analyze from CSV", min_value=1, max_value=1000, value=10, step=1)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    if 'message_text' not in df.columns:
        st.error("CSV file must contain 'message_text' column with messages.")
    else:
        if st.button(f"Analyze up to {max_entries} messages in CSV"):
            results = []
            with st.spinner(f"Analyzing up to {max_entries} messages..."):
                limited_df = df.head(max_entries)
                for message in limited_df['message_text']:
                    classification = classify_message(message)
                    scam_type = extract_scam_type(message) if classification == "scam" else "N/A"
                    explanation = generate_explanation(message)
                    results.append({
                        "message": message,
                        "classification": classification,
                        "scam_type": scam_type,
                        "explanation": explanation
                    })
            results_df = pd.DataFrame(results)
            st.dataframe(results_df)
            csv = results_df.to_csv(index=False).encode('utf-8')
            st.download_button(label="Download results as CSV", data=csv, file_name='scam_analysis_results.csv', mime='text/csv')
