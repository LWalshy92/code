# Imports
import openai
import json
import datetime
import subprocess

# Constants
# ChatGPT
openai.api_key = ""
GPTModel="gpt-3.5-turbo-16k"
GPTTemperature = 0.0
max_tokens = 15000 

# Folder paths
output_folder_path = "2. countries/"
subprocess_filepath = "trade_vols.py"

# Variables
region = "Europe"
run_subprocess = "Y"
    
# System queries
system_queries = [
    {"role": "system", "content": "You have access to detailed geographic information."},
    {"role": "system", "content": "You must provide a clear and concise tabular response within a single column headered as 'Country' and each individual constituent country listed below. You should not number each row or add any other additional information than what has been expressly requested."},
]

# Confirmation text
print("\033[92mRunning countries.py...\033[0m")

# countries-related question
prompt = [
    {"role": "user", "content": "List the individual constituent countries that are part of the " + region + "."},
]

# Run
# Confirmation text
print("\033[92mFetching country data for\033[0m", region)
    
# Make the API calls in chunks
offset = 0
while offset < len(system_queries) + len(prompt):
    messages = system_queries + prompt[offset:]
    completion = openai.ChatCompletion.create(
        model=GPTModel,
        temperature=GPTTemperature,
        max_tokens=max_tokens,
        messages=messages
    )
    response_data = {"countries": []}
    response = completion.choices[0].message['content']
    responses = response.split("\n")  # Split the response into lines

    # Extract the list of countries
    countries = [c for c in responses if c.strip() != '']
    response_data["countries"] = countries

    # Save the country list to a JSON file within the specified folder
    with open(f"{output_folder_path}countries.json", "w") as json_file:
        json.dump(response_data, json_file, indent=4)
    
    # Print the list of countries
    print(countries)

    offset += completion.usage['total_tokens']
    
if run_subprocess == "Y":
    try:
        # Confirmation text
        print("\033[92mCalling " + subprocess_filepath + "...\033[0m")
        subprocess.run(["python", subprocess_filepath])
    except Exception as e:
        # Error text
        print("\033[31mError calling " + subprocess_filepath + ":", e, "\033[0m")

