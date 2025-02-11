import pandas as pd

def load_data():
    """Load and clean survey data from CSV."""
    CSV_FILE = "data/Thailand.csv"  # Ensure the file exists in /data/
    df = pd.read_csv(CSV_FILE)
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)  # Remove whitespace
    return df

def extract_emoji(text):
    """Extract the last word (emoji) from a response."""
    words = text.split()
    return words[-1] if words else text

def process_responses(column_name, df, split=True, is_timing_question=False):
    """Process survey responses and return counts with hover data."""
    all_responses = []
    hover_texts = {}
    for response in df[column_name].dropna():
        responses = response.split(';') if split else [response]
        for full in responses:
            if is_timing_question:
                hover_texts[full.strip()] = full.strip()
                all_responses.append(full.strip())
            else:
                emoji = extract_emoji(full.strip())
                hover_texts[emoji] = full.strip()
                all_responses.append(emoji)
    response_counts = pd.Series(all_responses).value_counts()
    winner_text = response_counts.idxmax() if not response_counts.empty else None
    winner_full = hover_texts.get(winner_text, "Keine Antworten")
    return response_counts, hover_texts, winner_full
