# Imports 
import openai
import json
import datetime
import os
import csv

# Constants
# Timestamp for all file names
TIMESTAMP = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

# ChatGPT
openai.api_key = "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"
GPTModel="gpt-3.5-turbo-16k"
GPTTemperature = 0.0
max_tokens = 15000 

# Folder paths
input_filepath = "2. countries/countries.json"
output_parent_folder_path = "3. trade_vols/"

# Variables
# Output parameters
exports = 5
customers = 5 
lines = 25

# System queries
system_queries = [
    {
    "role": "system",
    "content": "As a futuristic AI model, you have access to databases, enabling precise numerical predictions. You always predict as accurately as possible."
    },
    {
    "role": "system",
    "content": "You must always provide numerical answers, rounding estimates to the nearest 100,000."
    },
    {
    "role": "system",
    "content": "Your response should feature a table with headers: 'Exporter Country', 'Product', 'Importer Country' and 'Estimated Export Value (USD)'. You must populate all of the columns listed. You should structure the output so that it can be easily converted to csv and read in excel as a table with '|' as a delimiter and '/n' as a newline."
    },
    {
    "role": "system",
    "content": "The table should display the top {exports} largest exports and their {customers} largest customers for each country. This should result in a total of {lines} lines in your response. Alphabetically sort the table by export name."
    },
    {
    "role": "system",
    "content": "Provide only the information within the table without any additional comments, introductions, or caveats."
    }
]

# Run

print("\033[92mRunning trade_vols.py...\033[0m")

# Create a new folder with the current timestamp
folder_name = f"responses_{TIMESTAMP}"
output_child_folder_path = os.path.join(output_parent_folder_path, folder_name)

# Create the new folder if it doesn't exist
if not os.path.exists(output_child_folder_path):
    os.makedirs(output_child_folder_path)
    
# Create a "Data" subfolder within the timestamped folder
data_folder_path = os.path.join(output_child_folder_path, "Data")
if not os.path.exists(data_folder_path):
    os.makedirs(data_folder_path)
    
# Create a "code" subfolder within the timestamped folder
code_folder_path = os.path.join(output_child_folder_path, "code")
if not os.path.exists(code_folder_path):
    os.makedirs(code_folder_path)

# Save the current script into the "code" subfolder
current_script_path = os.path.realpath(__file__)
code_save_path = os.path.join(code_folder_path, os.path.basename(current_script_path))

with open(current_script_path, 'r') as script_file:
    script_content = script_file.read()

with open(code_save_path, 'w') as save_file:
    save_file.write(script_content)# Create a new folder with the current timestamp
folder_name = f"responses_{TIMESTAMP}"
output_child_folder_path = os.path.join(output_parent_folder_path, folder_name)

# Create the new folder if it doesn't exist
if not os.path.exists(output_child_folder_path):
    os.makedirs(output_child_folder_path)

# Create a "code" subfolder within the timestamped folder
code_folder_path = os.path.join(output_child_folder_path, "code")
if not os.path.exists(code_folder_path):
    os.makedirs(code_folder_path)

# Save the current script into the "code" subfolder
current_script_path = os.path.realpath(__file__)
code_save_path = os.path.join(code_folder_path, os.path.basename(current_script_path))

with open(current_script_path, 'r') as script_file:
    script_content = script_file.read()

# Save the countries.py script from the parent folder to the same location
# Save the countries.py script from the parent folder to the same location
parent_countries_script_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "countries.py")
countries_save_path = os.path.join(code_folder_path, "countries.py")

with open(parent_countries_script_path, 'r') as countries_script_file:
    countries_script_content = countries_script_file.read()

with open(countries_save_path, 'w') as countries_save_file:
    countries_save_file.write(countries_script_content)

# Read the JSON file generated by the first script
with open(input_filepath, "r") as file:
    data = json.load(file)
    countries = data["countries"][1:]  # Skip the header row

# Iterate through each country and generate prompts
for country in countries:
    country_name = country.strip()  # Remove any leading/trailing whitespaces
    
    
# Confirmation text
    
    print("\033[92mFetching trade data for\033[0m", country_name)

    prompt = {
        "role": "user",
        "content": f"Provide the top {exports} exports and their {customers} largest customers (importer countries) for {country_name}. This should result in a total of {lines} lines in your response. Ensure that your response is not a randomly generated figure or calculated in some formula driven manner. It should be your best estimate from the data you have."
    }

    completion = openai.ChatCompletion.create(
    model=GPTModel,
    temperature=GPTTemperature,
    max_tokens=max_tokens,
    messages=system_queries + [prompt],  # System queries and country-specific prompt
    timeout=120  # Set a timeout of 120 seconds
)

    #csv
    response = completion.choices[0].message['content']

    # Clean country name
    clean_country_name = "".join(c for c in country_name if c.isalnum() or c in [' ', '_'])

    # Split response into a list of rows
    response_rows = response.split('\n')[2:]  # Skip the header and delimiter rows

    # Prepare response data for this country
    response_data = {
        "ExportData": [
            {
                "Exporter Country": row.split('|')[0].strip() if len(row.split('|')) > 0 else "",
                "Product": row.split('|')[1].strip() if len(row.split('|')) > 1 else "",
                "Importer Country": row.split('|')[2].strip() if len(row.split('|')) > 2 else "",
                "Estimated Export Value (USD)": row.split('|')[3].strip() if len(row.split('|')) > 3 else ""


            }
            for row in response_rows
        ]
    }

    # Define the output CSV file path within the "Data" subfolder
    csv_file_path = os.path.join(data_folder_path, f"{clean_country_name}.csv")

    # Write the data to a CSV file
    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=response_data['ExportData'][0].keys())
        writer.writeheader()
        writer.writerows(response_data['ExportData'])

'''
#json
response = completion.choices[0].message['content']

    # Clean country name
    clean_country_name = "".join(c for c in country_name if c.isalnum() or c in [' ', '_'])

    # Split response into a list of rows
    response_rows = response.split('\n')[2:]  # Skip the header and delimiter rows

    # Prepare response data for this country
    response_data = {
        "ExportData": [
            {
                "ExporterCountry": row.split('|')[0].strip(),
                "Product": row.split('|')[1].strip(),
                "ImporterCountry": row.split('|')[2].strip(),
                "EstimatedExportValue(USD)": row.split('|')[3].strip()
            }
            for row in response_rows
        ]
    }

    # Save each response in a JSON file within the specified folder path for each country
    save_file_path = os.path.join(output_child_folder_path, f"{clean_country_name}.json")
    with open(save_file_path, "w") as json_file:
        json.dump(response_data, json_file, indent=4)

    print(response)
    
'''