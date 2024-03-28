import csv


def process_csv_data(filename):
    quiz_data = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            question = row['Question']
            correct_option_index = int(row['Answer']) - 1  # Adjust for 0-indexing
            correct_option_key = f'Option {row["Answer"]}'
            correct_answer = row[correct_option_key]
            
            quiz_data.append({'Question': question, 'Correct Answer': correct_answer})
    
    return quiz_data
