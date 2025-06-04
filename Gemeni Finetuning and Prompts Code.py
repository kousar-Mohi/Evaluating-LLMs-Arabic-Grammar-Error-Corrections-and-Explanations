# Gemeni

!pip install -q google-generativeai

#Setup model
import csv
import json
import pandas as pd
import google.generativeai as genai
from google.colab import userdata
genai.configure(api_key=userdata.get('GOOGLE_API_KEY'))

base_model = [
    m for m in genai.list_models()
    if "createTunedModel" in m.supported_generation_methods and
    "flash" in m.name][0]

#prepare data training 

def convert_csv_to_training_format(input_csv, output_file):
    # Initialize an array to store all training examples
    all_training_examples = []

    # Read the CSV file and process each row
    with open(input_csv, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header

        for row in reader:
            medical_report = row[0]
            extracted_json = row[1]

            # Create a training example
            training_example = {
                "text_input": medical_report,
                "output": extracted_json
            }
            # Append to the list
            all_training_examples.append(training_example)

    # Write all training examples to the output file as a JSON array
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(all_training_examples, outfile, ensure_ascii=False, indent=4)

convert_csv_to_training_format("output.csv", "training_data.json")
convert_csv_to_training_format("output.csv", "validation_data.json")


# Load the CSV file
file_path = "Testing Data.csv"  # Replace with your actual file path
data = pd.read_csv(file_path)

# Function to clean, extract, and format as a paragraph with all details
def extract_and_format(row):
    try:
        obj = json.loads(row)  # Convert the JSON string into a Python dictionary

        # Start with basic details
        paragraph = (
            f"Final Corrected Sentence: {obj.get('final_corrected_sentence', '')}\n\n"
            f"Number of Errors Found: {obj.get('number_of_errors_found', 0)}\n"
            f"Errors Found:\n"
        )
        # Add details from the errors array
        i = 1
        for error in obj.get('errors_found', []):
            error_details = (
                f"  - Error ID: {i}\n"
                f"    Erroneous Word: {error.get('errornuos_word', '')}\n"
                f"    Error Types (English): {', '.join(error.get('errorType_English', []))}\n"
                f"    Error Types (Arabic): {', '.join(error.get('errorType_Arabic', []))}\n"
                f"    Correction: {error.get('correction', '')}\n"
                f"    Explanation: {error.get('explanation', '')}\n"
            )
            paragraph += error_details
            i+=1

        return paragraph
    except json.JSONDecodeError:
        return "Invalid JSON data"

# Apply the cleaning and formatting function to the specific column
column_name = "Final Explanation"  # Replace with the name of your column containing JSON objects
formatted_data = data[column_name].apply(extract_and_format)

# Save the formatted data to a new CSV file
output_df = pd.DataFrame({"Formatted Paragraph": formatted_data})
output_df.to_csv("Training Data Gemini.csv", index=False)
print("Data formatted and saved to formatted_data_with_details.csv")

"""for adding the sentence before input"""

# Input and output file paths
input_file = "Training Gemini test.csv"  # Your input CSV file
output_file = "output.csv"  # The modified output CSV file

# Prefix to add to each sentence
prefix = "Analyze the following Arabic sentence for a wide range of grammatical aspects and provide corrections along with explanations for each correction: "

# Open the input file for reading and output file for writing
with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8", newline="") as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Write the header row (assumes the input file has a header)
    headers = next(reader)  # Read header row
    writer.writerow(headers)  # Write the same header row to the output file

    # Process each row
    for row in reader:
        row[0] = prefix + row[0]  # Prepend the prefix to the first column
        writer.writerow(row)  # Write the modified row to the output file

print(f"Updated file saved as {output_file}")


def read_json_array_from_file(input_file):
    # Open the JSON file and load the array into a variable
    with open(input_file, 'r', encoding='utf-8') as infile:
        data_array = json.load(infile)  # Load the JSON array from the file
    return data_array

# Example usage
trainingData = read_json_array_from_file("training_data.json")

# Print the data to verify
print(trainingData)

# prepare finetuned model
name = 'finetuned-gemini3'
operation = genai.create_tuned_model(
    # You can use a tuned model here too. Set `source_model="tunedModels/..."`
    source_model=base_model.name,
    training_data = trainingData,
    id = name,
    epoch_count = 5,
    batch_size=4,
    learning_rate=0.001,
)

name = 'finetuned-gemini3'
model = genai.get_tuned_model(f'tunedModels/{name}')

from google import genai
client = genai.Client(api_key="GOOGLE_API_KEY")


# the following code is used for finetuning and running the prompts 
# just replace the model with the respective prompt 
def get_model_response(sentence):
    #Finetuning
    #result = model.generate_content(f"Analyze the following Arabic sentence for a wide range of grammatical aspects and provide corrections along with explanations for each correction: {sentence}")
    #model="finetuned-gemini3"
    
    #Fewshot Prompt
    #result = client.models.generate_content(
    #   model="gemini-pro",
    #   contents=f"""Correct the following Arabic sentence and provide only the following: 
    #     1. Corrected Sentence: 
    #     2. Number of errors found to be explained 
    #     3. For each error found, write the
    #     1. corrected word, 
    #     2. define the error type in English, 
    #     3. define error type in Arabic, 
    #     and 4. explain why do we need to correct the errors based on the error types for each error separately: كيف اطور مهارتيفي الاستماع؟.

    #     Corrected Sentence: كيف أطور مهارتي في الاستماع؟
    #     Number of Errors Found: 2
    #     Errors Found	
    #       - Error ID	 1
    #         Erroneous Word	 اطور
    #         Error Types (English)	 Hamza error
    #         Error Types (Arabic)	 أخطاء الهمزة
    #         Correction	 أطور
    #         Explanation	 The correction of ""اطور"" to ""أطور"" is necessary due to the rules governing the use of the Hamza in Arabic. In this case, the word should begin with a Hamza to indicate the proper pronunciation and to adhere to the grammatical structure of the language. The Hamza serves as a glottal stop and is essential for distinguishing the correct form of the verb, which in this instance is in the first-person singular present tense of ""to develop"" or ""to evolve."" Without the Hamza, the word not only loses its intended meaning but also becomes grammatically incorrect, highlighting the importance of proper Hamza usage in Arabic writing and communication.
    #       - Error ID	 2
    #         Erroneous Word	 مهاراتيفي
    #         Error Types (English)	 forget press on space
    #         Error Types (Arabic)	 حذف المسافة
    #         Correction	 مهاراتي في
    #         Explanation	 The correction from ""مهاراتيفي"" to ""مهاراتي في"" is necessary because the original phrase suffers from a spacing error where the words are incorrectly combined. In Arabic, proper spacing between words is crucial for clear communication and grammatical accuracy. ""مهاراتي"" means ""my skills,"" while ""في"" means ""in."" Without the appropriate space, the meaning becomes obscured, and the phrase loses its intended clarity. Ensuring correct spacing not only adheres to grammatical standards but also enhances readability and understanding in the Arabic language.
    

    #     Correct the following Arabic sentence and provide only the following: 
    #     1. Corrected Sentence: 
    #     2. Number of errors found to be explained 
    #     3. For each error found, write the
    #     1. corrected word, 
    #     2. define the error type in English, 
    #     3. define error type in Arabic, 
    #     and 4. explain why do we need to correct the errors based on the error types for each error separately: اللغة نظام كليّ يتكون من مجموعة من الانظمة الفرعية، وكل نظام فرعي يتكون من مجموعة من المستويات، وكلما كانت نظرتنا كلية شاملة الي اللغة تعلمناها بشكل افضل وشمولي.

    #     Corrected Sentence	 اللغة نظام كليّ يتكون من مجموعة من الأنظمة الفرعية، وكل نظام فرعي يتكون من مجموعة من المستويات، وكلما كانت نظرتنا كلية شاملة إلى اللغة تعلمناها بشكل أفضل وشمولي.
    #     Number of Errors Found: 3	
    #     Errors Found	
    #       - Error ID	 1
    #         Erroneous Word	 الانظمة
    #         Error Types (English)	 Hamza error
    #         Error Types (Arabic)	 أخطاء الهمزة
    #         Correction	 الأنظمة
    #         Explanation	 The correction of ""الانظمة"" to ""الأنظمة"" addresses a common Hamza error in Arabic grammar. In this case, the word ""الأنظمة"" (the systems) requires the Hamza (ء) to indicate the proper pronunciation and grammatical structure, as it follows the definite article ""ال."" The absence of the Hamza in ""الانظمة"" leads to a misreading and misunderstanding of the word's form and meaning. Correctly placing the Hamza ensures that the word conforms to standard Arabic orthography and accurately reflects its intended meaning, maintaining the integrity of the language.
    #       - Error ID	 2
    #         Erroneous Word	 الى
    #         Error Types (English)	 Hamza error
    #         Error Types (Arabic)	 أخطاء الهمزة
    #         Correction	 إلى
    #         Explanation	 The correction from ""الى"" to ""إلى"" addresses a specific grammatical error related to the use of Hamza in Arabic. In this case, the proper spelling of the preposition ""إلى"" requires the Hamza at the beginning, which is crucial for maintaining the correct pronunciation and meaning of the word. The absence of the Hamza not only alters the phonetic integrity of the word but can also lead to misunderstandings in communication. Therefore, ensuring the correct usage of Hamza is essential for clarity and adherence to standard Arabic writing conventions.
    #       - Error ID	 3
    #         Erroneous Word	 افضل
    #         Error Types (English)	 Hamza error
    #         Error Types (Arabic)	 أخطاء الهمزة
    #         Correction	 أفضل
    #         Explanation	 The correction of ""افضل"" to ""أفضل"" is necessary due to the proper placement of the Hamza, which is a critical aspect of Arabic orthography. In Arabic, the word ""أفضل"" (meaning ""better"" or ""best"") requires a Hamza on the letter 'ا' to indicate the correct pronunciation and to distinguish it from similar words. The absence of the Hamza in ""افضل"" alters both the meaning and the grammatical correctness of the word, as it fails to adhere to the rules of Arabic script that dictate the use of Hamza in certain contexts. Thus, ensuring the proper placement of Hamza is essential for conveying the intended meaning accurately and maintaining the integrity of the language.


    #       Correct the following Arabic sentence and provide only the following: 
    #       1. Corrected Sentence: 
    #       2. Number of errors found to be explained 
    #       3. For each error found, write the
    #       1. corrected word, 
    #       2. define the error type in English, 
    #       3. define error type in Arabic, 
    #       and 4. explain why do we need to correct the errors based on the error types for each error separately: ${sentence}""",
    # )
       
    #Zeroshot Prompt
    result = client.models.generate_content(
      model="gemini-pro",
      contents=f"Correct the following Arabic sentence and provide only the following: 1. Corrected Sentence: 2. Number of errors found to be explained 3. For each error found, write the 1. corrected word, 2. define the error type in English, 3. define error type in Arabic, and 4. explain why do we need to correct the errors based on the error types for each error separately: {sentence}",
    )
    return result.text

# Paths for input and output files
input_file = "sentences2.txt"  # Text file with sentences (one per line)
output_file = "Actual Gemini.csv"   # CSV file to save the results

# Read sentences from the text file
with open(input_file, "r", encoding="utf-8") as file:
    sentences = file.readlines()

# Open CSV file for writing
with open(output_file, "w", encoding="utf-8", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Input", "Output"])  # Write header row

    # Process each sentence
    for sentence in sentences:
        sentence = sentence.strip()  # Remove leading/trailing whitespace
        if sentence:  # Skip empty lines
            try:
                response = get_model_response(sentence)
                writer.writerow([sentence, response])
                print(f"Processed: {sentence}")  # Optional: show progress
            except Exception as e:
                print(f"Error processing sentence: {sentence}, Error: {e}")

print(f"Results saved to {output_file}")