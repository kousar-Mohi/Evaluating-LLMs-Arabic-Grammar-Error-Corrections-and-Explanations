import { OpenAI } from "openai";
import * as readline from 'readline';
import * as fs from 'fs';
import { createObjectCsvWriter as createCsvWriter } from 'csv-writer';

const openai = new OpenAI({ apiKey: "apiKey"});


const filePath = 'Dataset/runningData.txt';

const readStream = fs.createReadStream(filePath, { encoding: 'utf8' });
const rl = readline.createInterface({
  input: readStream,
  crlfDelay: Infinity,
});

const csvWriter = createCsvWriter({
  path: 'Actual GPT 4o Runs - Fewshot.csv',
  header: [
    { id: 'ES', title: 'Input'}, // es = d
    { id: 'EXP', title: 'Output'} // exp = dToMsa
  ]
});

const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

const processLine = async (line) => {
  let sentence = line;
/*
Correct the following Arabic sentence and provide only the following: 
        1. Corrected Sentence: 
        2. Number of errors found to be explained 
        3. For each error found, write the
        1. corrected word, 
        2. define the error type in English, 
        3. define error type in Arabic, 
        and 4. explain why do we need to correct the errors based on the error types for each error separately: كيف اطور مهارتيفي الاستماع؟.

        Corrected Sentence: كيف أطور مهارتي في الاستماع؟
        Number of Errors Found: 2
        Errors Found	
          - Error ID	 1
            Erroneous Word	 اطور
            Error Types (English)	 Hamza error
            Error Types (Arabic)	 أخطاء الهمزة
            Correction	 أطور
            Explanation	 The correction of ""اطور"" to ""أطور"" is necessary due to the rules governing the use of the Hamza in Arabic. In this case, the word should begin with a Hamza to indicate the proper pronunciation and to adhere to the grammatical structure of the language. The Hamza serves as a glottal stop and is essential for distinguishing the correct form of the verb, which in this instance is in the first-person singular present tense of ""to develop"" or ""to evolve."" Without the Hamza, the word not only loses its intended meaning but also becomes grammatically incorrect, highlighting the importance of proper Hamza usage in Arabic writing and communication.
          - Error ID	 2
            Erroneous Word	 مهاراتيفي
            Error Types (English)	 forget press on space
            Error Types (Arabic)	 حذف المسافة
            Correction	 مهاراتي في
            Explanation	 The correction from ""مهاراتيفي"" to ""مهاراتي في"" is necessary because the original phrase suffers from a spacing error where the words are incorrectly combined. In Arabic, proper spacing between words is crucial for clear communication and grammatical accuracy. ""مهاراتي"" means ""my skills,"" while ""في"" means ""in."" Without the appropriate space, the meaning becomes obscured, and the phrase loses its intended clarity. Ensuring correct spacing not only adheres to grammatical standards but also enhances readability and understanding in the Arabic language.
    

        Correct the following Arabic sentence and provide only the following: 
        1. Corrected Sentence: 
        2. Number of errors found to be explained 
        3. For each error found, write the
        1. corrected word, 
        2. define the error type in English, 
        3. define error type in Arabic, 
        and 4. explain why do we need to correct the errors based on the error types for each error separately: اللغة نظام كليّ يتكون من مجموعة من الانظمة الفرعية، وكل نظام فرعي يتكون من مجموعة من المستويات، وكلما كانت نظرتنا كلية شاملة الي اللغة تعلمناها بشكل افضل وشمولي.

        Corrected Sentence	 اللغة نظام كليّ يتكون من مجموعة من الأنظمة الفرعية، وكل نظام فرعي يتكون من مجموعة من المستويات، وكلما كانت نظرتنا كلية شاملة إلى اللغة تعلمناها بشكل أفضل وشمولي.
        Number of Errors Found: 3	
        Errors Found	
          - Error ID	 1
            Erroneous Word	 الانظمة
            Error Types (English)	 Hamza error
            Error Types (Arabic)	 أخطاء الهمزة
            Correction	 الأنظمة
            Explanation	 The correction of ""الانظمة"" to ""الأنظمة"" addresses a common Hamza error in Arabic grammar. In this case, the word ""الأنظمة"" (the systems) requires the Hamza (ء) to indicate the proper pronunciation and grammatical structure, as it follows the definite article ""ال."" The absence of the Hamza in ""الانظمة"" leads to a misreading and misunderstanding of the word's form and meaning. Correctly placing the Hamza ensures that the word conforms to standard Arabic orthography and accurately reflects its intended meaning, maintaining the integrity of the language.
          - Error ID	 2
            Erroneous Word	 الى
            Error Types (English)	 Hamza error
            Error Types (Arabic)	 أخطاء الهمزة
            Correction	 إلى
            Explanation	 The correction from ""الى"" to ""إلى"" addresses a specific grammatical error related to the use of Hamza in Arabic. In this case, the proper spelling of the preposition ""إلى"" requires the Hamza at the beginning, which is crucial for maintaining the correct pronunciation and meaning of the word. The absence of the Hamza not only alters the phonetic integrity of the word but can also lead to misunderstandings in communication. Therefore, ensuring the correct usage of Hamza is essential for clarity and adherence to standard Arabic writing conventions.
          - Error ID	 3
            Erroneous Word	 افضل
            Error Types (English)	 Hamza error
            Error Types (Arabic)	 أخطاء الهمزة
            Correction	 أفضل
            Explanation	 The correction of ""افضل"" to ""أفضل"" is necessary due to the proper placement of the Hamza, which is a critical aspect of Arabic orthography. In Arabic, the word ""أفضل"" (meaning ""better"" or ""best"") requires a Hamza on the letter 'ا' to indicate the correct pronunciation and to distinguish it from similar words. The absence of the Hamza in ""افضل"" alters both the meaning and the grammatical correctness of the word, as it fails to adhere to the rules of Arabic script that dictate the use of Hamza in certain contexts. Thus, ensuring the proper placement of Hamza is essential for conveying the intended meaning accurately and maintaining the integrity of the language.


          Correct the following Arabic sentence and provide only the following: 
          1. Corrected Sentence: 
          2. Number of errors found to be explained 
          3. For each error found, write the
          1. corrected word, 
          2. define the error type in English, 
          3. define error type in Arabic, 
          and 4. explain why do we need to correct the errors based on the error types for each error separately: ${sentence}
*/
  try {
    const EXP = await openai.chat.completions.create({
      model: "gpt-4o",
      messages: [{ role: "user", content: `Correct the following Arabic sentence and provide only the following: 
          1. Corrected Sentence: 
          2. Number of errors found to be explained 
          3. For each error found, write the
          1. corrected word, 
          2. define the error type in English, 
          3. define error type in Arabic, 
          and 4. explain why do we need to correct the errors based on the error types for each error separately: ${sentence}`}],
      temperature: 0.7
    });

    // Introduce delay before the next API request
    await delay(1500);

    const data = { ES: sentence, EXP: EXP.choices[0].message.content};
    csvWriter.writeRecords([data])
      .then(() => console.log('CSV record written successfully'));
  } catch (error) {
    console.error('Error processing line:', error.message);
  }
};

rl.on('line', async (line) => {
  if (line) {
    await processLine(line);
  }
});

rl.on('close', () => {
  console.log("Done");
});
