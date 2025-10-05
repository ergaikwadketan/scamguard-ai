# If you get 'ModuleNotFoundError: No module named "pandas"', run:
# pip install pandas

import pandas as pd

def load_dataset(path="dataset.csv"):
    df = pd.read_csv(path)
    print(df.head())  # Shows first few rows
    return df

if __name__ == "__main__":
    load_dataset()
