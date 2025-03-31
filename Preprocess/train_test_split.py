import pandas as pd
import json
import os
from sklearn.model_selection import train_test_split

def create_json_datasets(csv_path, source_col, target_col, output_dir, train_ratio=0.8, val_ratio=0.1, test_ratio=0.1):
    """
    Reads a CSV file, splits it into train, validation, and test datasets, 
    and saves them in JSON format.
    
    Args:
        csv_path (str): Path to the CSV file containing source and target language columns.
        source_col (str): Name of the column with the source language text.
        target_col (str): Name of the column with the target language text.
        output_dir (str): Directory where the JSON files will be saved.
        train_ratio (float): Proportion of the dataset to use for training.
        val_ratio (float): Proportion of the dataset to use for validation.
        test_ratio (float): Proportion of the dataset to use for testing.
    """
    # Load the CSV file
    df = pd.read_csv(csv_path)
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Split the data into train, validation, and test sets
    train_data, temp_data = train_test_split(df, test_size=(1 - train_ratio), random_state=42)
    val_data, test_data = train_test_split(temp_data, test_size=(test_ratio / (test_ratio + val_ratio)), random_state=42)
    
    # Function to save data to JSON Lines format
    def save_to_json(data, filename):
        records = data.apply(lambda row: {"translation": {source_col: row[source_col], target_col: row[target_col]}}, axis=1).tolist()
        with open(filename, 'w', encoding='utf-8') as f:
            for record in records:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
    
    # Save each split
    save_to_json(train_data, os.path.join(output_dir, "train.json"))
    save_to_json(val_data, os.path.join(output_dir, "dev.json"))
    save_to_json(test_data, os.path.join(output_dir, "test.json"))

    print(f"JSON files saved in {output_dir}")

# Example Usage
if __name__ == "__main__":
    # Replace these with your CSV path and column names
    csv_file_path = "./Preprocess/STEMsmall.csv"  # Path to your CSV file
    source_language_column = "source"  # Source language column name
    target_language_column = "target"  # Target language column name
    output_directory = "./Preprocess/splits/SmallSplit"  # Directory to save JSON files

    create_json_datasets(csv_file_path, source_language_column, target_language_column, output_directory)