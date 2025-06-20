# Evaluating-LLMs-Arabic-Grammar-Error-Corrections-and-Explanations

##	Description.
This paper evaluates the performance of LLMs in correcting and explaining Arabic grammatical errors. In addition, the paper explores different techniques such as fine-tuning, zero-shot prompting, and few-shot prompting techniques. Also, we used two datasets, a Manual Arabic Spelling Error Correction corpus and the Hugging Face Arabic GEC dataset. 

##	Dataset Information.
First dataset is Manual Arabic spelling-errors correction which is a text corpus designed for Arabic spell-checking; it was compiled from various files edited by a group of individuals and published by the Sudan University of Science and Technology. The corpus consists of 11,098 words containing 1,888 errors and 20 error types, structured into several sections. It is an [XML File](https://lindat.mff.cuni.cz/repository/xmlui/handle/11372/LRT-4763) that contains the following:
It has tags such as `<persons>`, `<documents>`, `<errorType>`, `<errorWord>`, etc. where each section contains data that elaborate on its content, which assists researchers in extracting valuable insights.
- Persons section contains basic information about each person and its relationship of using the computer
- Documents section clarifies all sentences in each document with the numbering of each sentence to be used in the errors section that was committed.
- Type of errors section lists all the possible errors with their description in the Arabic language and give an illustrative example.
This dataset will be used as training data to finetune the models.

Second dataset is [Arabic GEC dataset shared on the Hugging Face platform](https://huggingface.co/datasets/s3h/arabic-grammar-corrections). It has over 390,000 Arabic erroneous sentences and their corrections (baseline). We chose the first 2,000 records to evaluate the ability of both base and fine-tuned models in correcting erroneous sentences and explaining the purpose of corrections.
This dataset will be used to evaluate LLM's performance.

##	Code Information.
All the following code files are uploaded in the repositry.

- **Prepare Training Dataset.js**: this Javascript file is used to go over the XML file and convert it to a JSON object for easier usage.
- **Add Explanation Code.js**: this Javascript file is used to add an explanation key to the JSON object in addition to asking GPT to explian the need of correcting the erroneous words.    
- **ALLaM Prompt Code.js**: this Javascript file is used to prompt ALLaM through prompting techniques (already mentioned in the file).
- **Gemeni Finetuning and Prompts Code.py**: this Python file is used to finetune Gemeni, then evaluate the finetuned and baseline models through prompting techniques (already mentioned in the file).
- **GPT Finetuning Code.py**: this Python file is used to finetune GPT.
- **GPT Prompts Code.js**: this Javascript file is used to prompt GPT through prompting techniques (already mentioned in the file).
- **LLama Finetuning and Prompts Code.py**: this Python file is used to finetune Llama, then evaluate the finetuned and baseline through prompting techniques (already mentioned in the file).

##	Usage Instructions
The Javascript files are ran in Visual Studio Code

The Python files are ran in Google Colab Notebook

##	Requirements.
All the libraries needed for Python files are mentioned in the files.

All the libraries needed for Javascript files are mentioned in the files. But for Visual Studio Code, you have to install node.js as an additional step. 

##	Citations.
If you find the datasets useful in your research, please cite the following:
- A New Spell-Checking Approach Based on the User Profile (Saty et al., 2023).
- This is the Arabic GEC dataset shared on the Hugging Face platform [Link](https://huggingface.co/datasets/s3h/arabic-grammar-corrections).

##	Materials & Methods
We aimed to prompt and finetune the chosen LLMs (GPT, Gemini, Llama, and ALLaM) to evaluate their capabilities for Arabic Grammar Error Correction and Explanation tasks. The following image shows the pipeline of our full approach:

![pipeline](https://github.com/user-attachments/assets/97e9cba3-5799-4fc8-b3ec-8dcb6fe8dc26)

### Data Preprocessing
For fine-tuning, we first preprocessed the Manual Arabic Spelling Errors Correction corpus. Specifically, we adopted its output structure while excluding the first three keys: `documentID`, `statementID`, and `PersonID`. To enhance the training data, we prompted GPT-4o-mini to include an additional key called `"explanation"` that provides the rationale behind each correction. This makes the output both informative, comprehensive and offers a complete understanding of the error correction process. 

### Model Fine-Tuning and Prompting Techniques 
After preparing the training data, we fine-tuned GPT4o and Gemini through API requests. For Llama, we used Laminai third-party application to fine-tune the model. Finally, we used the Hugging Face Arabic GEC dataset to evaluate the performance and accuracy of the fine-tuned models. For prompting, we employed two common techniques: zero-shot and few-shot prompting. The zero-shot approach prompts LLMs without providing examples to measure their natural capabilities. We asked each LLM to correct the erroneous sentence and provide the corrected sentence, the number of errors found in the sentence (and for each error, the corrected word and the type of error, identified in English and Arabic), and finally, a detailed explanation for the corrections applied.

###	Computing infrastructure
we used a Lenovo YOGA 9i with 16 GB RAM and 1T storage using a Windows operating system. Additionally, we utilized Python3 on Google Colab, running data on both CPU and T4 GPU environments.

###	Evaluation method: 
We have used Cross-dataset testing to validate the LLM’s effectiveness in addition to the following evaluation metrics: Cosine Similarity, BLEU (Bilingual Evaluation Understudy), Levenshtein Distance, WER (Word Error Rate), CER (Charachter Error Rate), CLEME (Chunk-LEvel Multi-reference Evaluation), GLEU (Generalized Language Evaluation Understanding), and ROUGE (Recall-Oriented Understudy for Gisting Evaluation)..
