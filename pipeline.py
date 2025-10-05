import pandas as pd
from llm_utils import classify_message, extract_scam_type, generate_explanation


def analyze_message(message: str):
    classification = classify_message(message)
    scam_type = extract_scam_type(message) if classification == "scam" else "N/A"
    explanation = generate_explanation(message)
    return {
        "message": message,
        "classification": classification,
        "scam_type": scam_type,
        "explanation": explanation
    }


def process_csv(input_csv_path='dataset.csv', output_csv_path='scam_analysis_results.csv', max_entries=10):
    # Read the CSV file that contains the messages
    df = pd.read_csv(input_csv_path)

    # Ensure the CSV has a column named 'message_text' containing messages
    if 'message_text' not in df.columns:
        raise ValueError("CSV file must have a 'message_text' column with the messages to analyze.")

    # Limit processing to max_entries rows
    df = df.head(max_entries)

    results = []
    for index, row in df.iterrows():
        message = row['message_text']
        result = analyze_message(message)
        results.append(result)
        print(f"Processed message {index + 1}/{len(df)}: {message[:50]}...")  # show preview

    # Save results to a new CSV file
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_csv_path, index=False)
    print(f"\nAnalysis complete! Results saved to '{output_csv_path}'.")


if __name__ == "__main__":
    # Only process first 10 entries by default to save API usage
    process_csv(max_entries=10)
