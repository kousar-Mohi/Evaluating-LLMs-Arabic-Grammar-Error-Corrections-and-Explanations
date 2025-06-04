# Evaluating-LLMs-Arabic-Grammar-Error-Corrections-and-Explanations

##	Description.
This paper evaluates the performance of LLMs in correcting and explaining Arabic grammatical errors. In addition, the paper explores different techniques such as fine-tuning, zero-shot prompting, and few-shot prompting techniques. Also, we used two datasets, a Manual Arabic Spelling Error Correction corpus and the Hugging Face Arabic GEC dataset. 

##	Dataset Information.
First dataset is [Manual Arabic spelling-errors correction](https://d1wqtxts1xzle7.cloudfront.net/108712620/IJCDS1301116-libre.pdf?1702274347=&response-content-disposition=inline%3B+filename%3DA_new_spell_checking_approach_based_on_t.pdf&Expires=1749046646&Signature=eKt-EBQcTBSaqEjElrz1zeoh0LMqHRtn-Rl6UPj~N3btvbLYkLOtv5b1ZurWWMqMgBAh0zJpdR2~Bgp6trjVGI4nfCFieyZQufAD4qNXNuV7tfqb~BN1Lt9JfXt1QADg6U9iAAlrCWZGh-t~lzClQTpB-fnsR51O3MsJ-yHfSpWihQHm1y4bJpIIAzdER5EeqfMIfYr0pICtaGkuIVAs41JwU9~kbMoWBf80G4~ualzAXSfuKDu3NMVvFCZLg47i-5-keT7viAjpJgsHS7Pz43Hv678kXeYPLeUqyDOVLEbQHhRVUCatT-GsAv3qvTHe0fPmEqIWvgXKkjWmFWoE4g__&Key-Pair-Id=APKAJLOHF5GGSLRBV4ZA) which is a text corpus designed for Arabic spell-checking; it was compiled from various files edited by a group of individuals and published by the Sudan University of Science and Technology. It is an [XML File](https://lindat.mff.cuni.cz/repository/xmlui/handle/11372/LRT-4763) that contains the following:
It has tags such as <persons>, <documents>, <errorType>, <errorWord>, etc. where each section contains data that elaborate on its content, which assists researchers in extracting valuable insights.
- Persons section contains basic information about each person and its relationship of using the computer
- Documents section clarifies all sentences in each document with the numbering of each sentence to be used in the errors section that was committed.
- Type of errors section lists all the possible errors with their description in the Arabic language and give an illustrative example.

Second dataset is [Arabic GEC dataset shared on the Hugging Face platform](https://huggingface.co/datasets/s3h/arabic-grammar-corrections). It has over 390,000 Arabic erroneous sentences and their corrections (baseline). We chose the first 2,000 records to evaluate the ability of both base and fine-tuned models in correcting erroneous sentences and explaining the purpose of corrections. Figure \ref{fig:dataset2} presents a sample of the dataset.

##	Code Information.

##	Usage Instructions – How to use or load the dataset and code.

##	Requirements – Any dependencies (e.g., Python libraries).

##	Methodology (if applicable) – Steps taken for data processing or modeling.

##	Citations (if applicable) – If this dataset was used in research, provide references.

##	License & Contribution Guidelines (if applicable).

##	Materials & Methods

##	Computing infrastructure (operating system, hardware, etc)

##	Describe any data preprocessing steps (or state in the Methods if this is not applicable)

##	Evaluation method: The evaluation method used to evaluate the proposed technique. Evaluation methods (e.g., ablation study, cross-validation, cross-dataset testing) refer to the APPROACH or PROCEDURE used to validate the model’s effectiveness
