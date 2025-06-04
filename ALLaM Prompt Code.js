const XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;
const fs = require('fs'); // File system module

// Enter your IBM Cloud API Key
const API_KEY = "API_KEY";

// Function to get authentication token
function getToken(errorCallback, loadCallback) {
    const req = new XMLHttpRequest();
    req.addEventListener("load", loadCallback);
    req.addEventListener("error", errorCallback);
    req.open("POST", "https://iam.cloud.ibm.com/identity/token");
    req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    req.setRequestHeader("Accept", "application/json");
    req.send("grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=" + API_KEY);
}

// Function to send API request
function apiPost(scoring_url, token, payload, loadCallback, errorCallback) {
    const oReq = new XMLHttpRequest();
    oReq.addEventListener("load", loadCallback);
    oReq.addEventListener("error", errorCallback);
    oReq.open("POST", scoring_url);
    oReq.setRequestHeader("Accept", "application/json");
    oReq.setRequestHeader("Authorization", "Bearer " + token);
    oReq.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    oReq.send(JSON.stringify(payload));
}

// Read sentences from the file
const words = fs.readFileSync('Dataset/runningData.txt', 'utf8')
    .split('\n')
    .map(word => word.trim())
    .filter(word => word.length > 0); // Remove empty lines

// Prepare CSV file with header
const csvFilePath = 'Actual Allam Runs.csv';
fs.writeFileSync(csvFilePath, 'Input,Output\n', { flag: 'w' });

// Function to write responses to CSV
function writeToCSV(input, response) {
    const formattedResponse = `"${response.replace(/"/g, '""')}"`; // Escape quotes but keep newlines
    const row = `"${input.replace(/"/g, '""')}",${formattedResponse}\n`; // Ensure input is also properly quoted
    fs.appendFileSync(csvFilePath, row, 'utf8');
}

// Get authentication token and process sentences
getToken(
    (err) => console.log("Token retrieval error:", err),
    function () {
        let tokenResponse;
        try {
            tokenResponse = JSON.parse(this.responseText);
        } catch (ex) {
            console.log("Error parsing token response:", ex);
            return;
        }

        const token = tokenResponse.access_token;
        const scoring_url = "https://eu-de.ml.cloud.ibm.com/ml/v4/deployments/a4b71560-6778-4bce-994e-ae90287d284a/ai_service?version=2021-05-01";

        // Function to process each word with delay
        function processWordWithDelay(index) {
            if (index >= words.length) return; // Stop when all words are processed

            const word = words[index];
            if (!word) return;

            const payload = {
                "messages": [
                    {
                        "role": "user",
                        // "content": `Correct the following Arabic sentence and provide only the following: 
                        //             1. Corrected Sentence: 
                        //             2. Number of errors found to be explained 
                        //             3. For each error found, write the 1. corrected word, 
                        //                2. define the error type in English, 
                        //                3. define error type in Arabic, and 
                        //                4. explain why do we need to correct the errors 
                        //                   based on the error types for each error separately: ${word}`
                        "content": `Correct the following Arabic sentence and provide only the following: 
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
                                    and 4. explain why do we need to correct the errors based on the error types for each error separately: ${word}`
                    },
                ],
            };

            apiPost(scoring_url, token, payload, function () {
                try {
                    const parsedResponse = JSON.parse(this.responseText);
                    console.log("parsedResponse", parsedResponse);
                    const responseContent = parsedResponse.choices[0]?.message?.content || "No response";

                    console.log(`Processed: ${index + 1}/${words.length}`);
                    writeToCSV(word, responseContent);
                } catch (ex) {
                    console.log(`Error parsing response for word "${word}":`, ex);
                }

                // Wait 200ms (or whatever delay you need) before processing the next word
                setTimeout(() => processWordWithDelay(index + 1), 200);
            }, function (err) {
                console.log(`API call error for word "${word}":`, err);
            });
        }

        // Start processing words with a delay between each API call
        processWordWithDelay(0);
    }
);

