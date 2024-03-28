import csv

def process_csv_data(input_filename):
    output_filename = 'cleaned_csv'
    with open(input_filename, newline='', encoding='utf-8') as csvfile, open(output_filename, 'w', encoding='utf-8') as outfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            question = row['Question']
            correct_option_index = int(row['Answer']) - 1  # Adjust for 0-indexing
            correct_option_key = f'Option {row["Answer"]}'
            correct_answer = row[correct_option_key]
            
            # Write the question and correct answer to the output file
            outfile.write(f'Question: {question}\nCorrect Answer: {correct_answer}\n\n')

        return output_filename
