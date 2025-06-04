import csv
import json

def convert_csv_to_training_format(input_csv, output_file):
    with open(input_csv, 'r', encoding='utf-8') as csvfile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header

        for row in reader:
            medical_report = row[0]
            extracted_json = row[1]

            training_example = {
                "input": f"Analyze the following Arabic sentence for a wide range of grammatical aspects and provide corrections along with explanations for each correction: {medical_report}",
                "output": extracted_json
            }
            outfile.write(json.dumps(training_example, ensure_ascii=False) + '\n')

# Prepare training data
convert_csv_to_training_format("Training Gemini test.csv", "Llama_training_data.jsonl")

pip install --upgrade lamini

import lamini
lamini.api_key = "api_key"
#Finetuning Model
#llm = lamini.Lamini("Llama-fintuned")

#Prompt Model
#llm = lamini.Lamini("meta-llama/Llama-3.2-3B-Instruct")

import csv

# Replace this with your function to interact with the model
def get_model_response(sentence):
    #Finetuning
    result = llm.generate(f"""<|begin_of_text|><|start_header_id|>user<|end_header_id|>Analyze the following Arabic sentence for a wide range of grammatical aspects and provide corrections along with explanations for each correction: {sentence} <|eot_id|><|start_header_id|>assistant<|end_header_id|>""")
    #Zeroshot Prompt
;     result = llm.generate(f"""<|begin_of_text|><|start_header_id|>user<|end_header_id|>correct the following Arabic sentence and provide only the following:
; ;       1. Corrected Sentence: 2. Number of errors found to be explained
; ;       3. For each error found,
; ;       write the 1. corrected word,
; ;       2. define the error type in English,
; ;       3. define error type in Arabic,
; ;       and 4. explain why do we need to correct the errors based on the error types for each error separately: {sentence} <|eot_id|><|start_header_id|>assistant<|end_header_id|>""")
    #Fewshot Prompt
;     result = llm.generate(f"""<|begin_of_text|><|start_header_id|>user<|end_header_id|> Correct the following Arabic sentence and provide only the following:
;       1. Corrected Sentence: 2. Number of errors found to be explained
;       3. For each error found,
;       write the 1. corrected word,
;       2. define the error type in English,
;       3. define error type in Arabic,
;       and 4. explain why do we need to correct the errors based on the error types for each error separately: كيف اطور مهارتيفي الاستماع؟.

;       Corrected Sentence: كيف أطور مهارتي في الاستماع؟
;       Number of Errors Found: 2
;       Errors Found
;         - Error ID	 1
;           Erroneous Word	 اطور
;           Error Types (English)	 Hamza error
;           Error Types (Arabic)	 أخطاء الهمزة
;           Correction	 أطور
;           Explanation	 The correction of ""اطور"" to ""أطور"" is necessary due to the rules governing the use of the Hamza in Arabic. In this case, the word should begin with a Hamza to indicate the proper pronunciation and to adhere to the grammatical structure of the language. The Hamza serves as a glottal stop and is essential for distinguishing the correct form of the verb, which in this instance is in the first-person singular present tense of ""to develop"" or ""to evolve."" Without the Hamza, the word not only loses its intended meaning but also becomes grammatically incorrect, highlighting the importance of proper Hamza usage in Arabic writing and communication.
;         - Error ID	 2
;           Erroneous Word	 مهاراتيفي
;           Error Types (English)	 forget press on space
;           Error Types (Arabic)	 حذف المسافة
;           Correction	 مهاراتي في
;           Explanation	 The correction from ""مهاراتيفي"" to ""مهاراتي في"" is necessary because the original phrase suffers from a spacing error where the words are incorrectly combined. In Arabic, proper spacing between words is crucial for clear communication and grammatical accuracy. ""مهاراتي"" means ""my skills,"" while ""في"" means ""in."" Without the appropriate space, the meaning becomes obscured, and the phrase loses its intended clarity. Ensuring correct spacing not only adheres to grammatical standards but also enhances readability and understanding in the Arabic language.


;     Correct the following Arabic sentence and provide only the following:
;       1. Corrected Sentence: 2. Number of errors found to be explained
;       3. For each error found,
;       write the 1. corrected word,
;       2. define the error type in English,
;       3. define error type in Arabic,
;       and 4. explain why do we need to correct the errors based on the error types for each error separately:  اللغة نظام كليّ يتكون من مجموعة من الانظمة الفرعية، وكل نظام فرعي يتكون من مجموعة من المستويات، وكلما كانت نظرتنا كلية شاملة الي اللغة تعلمناها بشكل افضل وشمولي.


;       Corrected Sentence	 اللغة نظام كليّ يتكون من مجموعة من الأنظمة الفرعية، وكل نظام فرعي يتكون من مجموعة من المستويات، وكلما كانت نظرتنا كلية شاملة إلى اللغة تعلمناها بشكل أفضل وشمولي.
;       Number of Errors Found: 3
;       Errors Found
;         - Error ID	 1
;           Erroneous Word	 الانظمة
;           Error Types (English)	 Hamza error
;           Error Types (Arabic)	 أخطاء الهمزة
;           Correction	 الأنظمة
;           Explanation	 The correction of ""الانظمة"" to ""الأنظمة"" addresses a common Hamza error in Arabic grammar. In this case, the word ""الأنظمة"" (the systems) requires the Hamza (ء) to indicate the proper pronunciation and grammatical structure, as it follows the definite article ""ال."" The absence of the Hamza in ""الانظمة"" leads to a misreading and misunderstanding of the word's form and meaning. Correctly placing the Hamza ensures that the word conforms to standard Arabic orthography and accurately reflects its intended meaning, maintaining the integrity of the language.
;         - Error ID	 2
;           Erroneous Word	 الى
;           Error Types (English)	 Hamza error
;           Error Types (Arabic)	 أخطاء الهمزة
;           Correction	 إلى
;           Explanation	 The correction from ""الى"" to ""إلى"" addresses a specific grammatical error related to the use of Hamza in Arabic. In this case, the proper spelling of the preposition ""إلى"" requires the Hamza at the beginning, which is crucial for maintaining the correct pronunciation and meaning of the word. The absence of the Hamza not only alters the phonetic integrity of the word but can also lead to misunderstandings in communication. Therefore, ensuring the correct usage of Hamza is essential for clarity and adherence to standard Arabic writing conventions.
;         - Error ID	 3
;           Erroneous Word	 افضل
;           Error Types (English)	 Hamza error
;           Error Types (Arabic)	 أخطاء الهمزة
;           Correction	 أفضل
;           Explanation	 The correction of ""افضل"" to ""أفضل"" is necessary due to the proper placement of the Hamza, which is a critical aspect of Arabic orthography. In Arabic, the word ""أفضل"" (meaning ""better"" or ""best"") requires a Hamza on the letter 'ا' to indicate the correct pronunciation and to distinguish it from similar words. The absence of the Hamza in ""افضل"" alters both the meaning and the grammatical correctness of the word, as it fails to adhere to the rules of Arabic script that dictate the use of Hamza in certain contexts. Thus, ensuring the proper placement of Hamza is essential for conveying the intended meaning accurately and maintaining the integrity of the language.

;       Now, correct the following Arabic sentence and provide only the following:
;       1. Corrected Sentence: 2. Number of errors found to be explained
;       3. For each error found,
;       write the 1. corrected word,
;       2. define the error type in English,
;       3. define error type in Arabic,
;       and 4. explain why do we need to correct the errors based on the error types for each error separately: {sentence}
;  <|eot_id|><|start_header_id|>assistant<|end_header_id|>
; """)
    return result

# Paths for input and output files
input_file = "sentences - Copy.txt"  # Text file with sentences (one per line)
output_file = "Actual Llama.csv"   # CSV file to save the results

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
