import * as readline from "readline";
import * as fs from "fs";
import { OpenAI } from "openai"; // Assume openai package is configured properly.

const inputFile = "Dataset/test.json";
const outputFile = "Dataset/errorsTest.json"; // Path to save the processed errors

const openai = new OpenAI({
  apiKey: "piKey",
});

const readStream = readline.createInterface({
  input: fs.createReadStream(inputFile),
  crlfDelay: Infinity,
});

let dataBuffer = "";

// Read file line by line to handle large JSON
readStream.on("line", (line) => {
  dataBuffer += line;
});

readStream.on("close", async () => {
  try {
    const jsonData = JSON.parse(dataBuffer);

    for (const element of jsonData) {
      console.log("error start");
      for (const error of element.errors_found) {
        try {
          const response = await openai.chat.completions.create({
            model: "ft:gpt-4o-mini-2024-07-18:personal::AWlwXusM",
            messages: [
              {
                role: "user",
                content: `Explain why do we need to correct ${error.errornuos_word} to this ${error.correction}, where the Arabic grammatical error type is related to ${error.errorType_English} (${error.errorType_Arabic}). Summarize the explanation in one paragraph without points`,
              },
            ],
            temperature: 0.7,
          });

          // Safely access response
          error.explanation = response.choices[0].message.content;
          console.log("error done");
        } catch (apiError) {
          console.error(
            `API error for error: ${error.errornuos_word}:`,
            apiError.message || apiError
          );
          error.explanation =
            "Failed to fetch explanation due to an API error.";
        }
      }
    }

    // Write updated JSON data to output file
    fs.writeFileSync(outputFile, JSON.stringify(jsonData, null, 2), "utf8");
    console.log(`Updated JSON data has been written to ${outputFile}`);
  } catch (err) {
    console.error("Error processing JSON data:", err.message);
  }
});
