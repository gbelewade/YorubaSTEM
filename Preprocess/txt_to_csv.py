import csv

def convert_txt_to_csv(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as txt_file:
            lines = txt_file.readlines()
        
        with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["source", "target"])  # Write header
            
            for line in lines:
                parts = line.strip().split('\t')  # Split by tab
                if len(parts) == 2:  # Ensure valid pair
                    csv_writer.writerow(parts)
        
        print(f"CSV file successfully created: {output_file}")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
input_txt = "Dataset 2.0.txt"  # Change to your input file name
output_csv = "english_yoruba.csv"  # Output file name
convert_txt_to_csv(input_txt, output_csv)
