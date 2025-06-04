# OpenAI

import csv
import json

def convert_csv_to_training_format(input_csv, output_file):
    system_message = {
        "role": "system",
        "content": "Analyze the Arabic sentence for a wide range of grammatical aspects and provide corrections along with explanations for each correction"
    }

    with open(input_csv, 'r', encoding='utf-8') as csvfile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header

        for row in reader:
            medical_report = row[0]
            extracted_json = row[1]

            training_example = {
                "messages": [
                    system_message,
                    {"role": "user", "content": medical_report},
                    {"role": "assistant", "content": extracted_json}
                ]
            }
            outfile.write(json.dumps(training_example, ensure_ascii=False) + '\n')

# Prepare training data
convert_csv_to_training_format("Training GPT.csv", "training_data.jsonl")

# Prepare validation data
convert_csv_to_training_format("Training GPT.csv", "validation_data.jsonl")

"""### **Open AI Connection**"""

open_ai_key = "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"

"""Initial Setup with OpenAI"""

import os
from openai import OpenAI
from time import sleep

# Initialize OpenAI client
client = OpenAI(api_key = open_ai_key)

"""Uploading Training Files"""

def upload_training_file(file_path):
    with open(file_path, "rb") as file:
        response = client.files.create(
            file=file,
            purpose="fine-tune"
        )
        return response.id

# Upload both training and validation files
training_file_id = upload_training_file("training_data.jsonl")
validation_file_id = upload_training_file("validation_data.jsonl")
training_file_id, validation_file_id

"""Creating a Fine-Tuning Job"""

def create_fine_tuning_job(training_file_id, validation_file_id=None, model="gpt-4o-2024-08-06"):
    response = client.fine_tuning.jobs.create(
        training_file=training_file_id,
        validation_file=validation_file_id,
        model=model
    )
    return response.id

# Start the fine-tuning job
model="gpt-4o-2024-08-06"
job_id = create_fine_tuning_job(training_file_id, validation_file_id, model)
job_id

"""Monitoring Training Progress"""

def monitor_job(job_id):
    while True:
        job = client.fine_tuning.jobs.retrieve(job_id)
        print(f"Status: {job.status}")

        if job.status in ["succeeded", "failed"]:
            return job

        # List latest events
        events = client.fine_tuning.jobs.list_events(
            fine_tuning_job_id=job_id,
            limit=5
        )
        for event in events.data:
            print(f"Event: {event.message}")

        sleep(30)  # Check every 30 seconds

# Monitor the job until completion
job = monitor_job(job_id)
if job.status == "succeeded":
    fine_tuned_model = job.fine_tuned_model
    print(f"Fine-tuned model ID: {fine_tuned_model}")
else:
    print("Fine-tuning failed.")

"""### **Testing Model**"""

def test_model(model_id, test_input):
    completion = client.chat.completions.create(
        model=model_id,
        messages=[
            {
                "role": "system",
                "content": "Analyze the Arabic sentence for a wide range of grammatical aspects and provide corrections along with explanations for each correction"
            },
            {"role": "user", "content": test_input}
        ]
    )
    return completion.choices[0].message

test_report = "الخناس"

# Get prediction
result = test_model("ft:gpt-4o-2024-08-06:personal::AhJHHUDF", test_report)

print(result.content)