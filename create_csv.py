import csv
import re
import os

def convert_to_csv(input_file, output_file):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_directory, input_file)

    with open(input_path, 'r') as file:
        lines = file.read().split('\n')

    data = []
    i = 0

    print(f'Total lines in file: {len(lines)}')  # print total number of lines in the input file

    while i < len(lines):
        print(f'Processing line {i}: {lines[i]}')  # print the index and line being processed

        # Check if line is not empty and is not local time
        if lines[i] and 'Local time:' not in lines[i]:
            time = lines[i].strip()

            if i + 1 < len(lines) and 'request' in lines[i+1] and ',' not in lines[i+1]:
                model = 'Missing'
                requests = re.findall(r"(\d+) request", lines[i+1])[0]
                prompt = completion = total_tokens = 'NA'
                i += 2
            elif i + 2 < len(lines) and ',' in lines[i+2] and 'request' in lines[i+2]:
                model_requests = re.findall(r"([^,]+), (\d+) request", lines[i+2])
                if model_requests:
                    model, requests = model_requests[0][0], model_requests[0][1]
                    i += 3
                else:
                    model = 'Missing'
                    requests = 'NA'
                    i += 2
                if i < len(lines) and 'prompt' in lines[i] and 'completion' in lines[i]:
                    tokens = re.findall(r"([0-9,]+) prompt \+ ([0-9,]+) completion = ([0-9,]+) tokens", lines[i])
                    if tokens:
                        prompt, completion, total_tokens = tokens[0]
                        i += 1
                    else:
                        prompt = completion = total_tokens = 'NA'
                else:
                    prompt = completion = total_tokens = 'NA'
            else:
                i += 1
                continue

            # Only add data to list if all fields are present
            if model != 'Missing' and 'NA' not in [prompt, completion, total_tokens]:
                data.append([time, model, requests, prompt.replace(',', ''), completion.replace(',', ''), total_tokens.replace(',', '')])
        else:
            i += 1

    print(f'Total lines processed: {i}')  # print total number of lines processed

    output_path = os.path.join(script_directory, output_file)
    with open(output_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Time', 'Model', 'Requests', 'Prompt', 'Completion', 'Tokens'])
        writer.writerows(data)

    print("CSV file generated successfully.")



# Usage example
input_file = './data/raw_data.txt'  # Replace with your input file name
output_file = './data/output.csv'  # Replace with your desired output file name
convert_to_csv(input_file, output_file)
