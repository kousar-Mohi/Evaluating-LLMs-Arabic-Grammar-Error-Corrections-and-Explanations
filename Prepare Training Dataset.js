import * as readline from "readline";
import * as fs from "fs";
import { createObjectCsvWriter } from "csv-writer"; // Install with `npm install csv-writer`

const inputFile = "Dataset/json.txt";
const outputCsvFile = "Dataset/errors.csv"; // Path to save the CSV file

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
    // Parse the accumulated JSON
    const jsonData = JSON.parse(dataBuffer);
    const documents = jsonData.TEI.documents.document;
    const errorTypes = jsonData.TEI.errorTypes.errorType.map(
      ({ "_xml:id": errId, ...rest }) => ({
        errId,
        ...rest,
      })
    );
    const errors = jsonData.TEI.errors.error.map((item) => {
      let causes = item.causes.errorTypeId;

      // Ensure causes is always an array
      causes = Array.isArray(causes) ? causes : [causes];

      return {
        ...item,
        causes,
      };
    });

    // Create mappings for documents and error types
    const documentMap = documents.reduce((map, doc) => {
      map[doc.docId] = doc.statements.statement.reduce((stmtMap, stmt) => {
        stmtMap[stmt["_xml:id"]] = stmt.text;
        return stmtMap;
      }, {});
      return map;
    }, {});

    const errorTypeMap = errorTypes.reduce(
      (map, { errId, causeDesc, causeArabicDes }) => {
        map[errId] = { causeDesc, causeArabicDes };
        return map;
      },
      {}
    );

    // Group errors by docId and statementId
    const groupedErrors = errors.reduce((result, error) => {
      const { docId, statementId, errorId, errorWord, correctWord, causes } =
        error;

      // Get the statement text
      const statementText = documentMap[docId]?.[statementId] || "Unknown";

      // Add error to the corresponding group
      if (!result[docId]) result[docId] = {};
      if (!result[docId][statementId]) {
        result[docId][statementId] = {
          number_of_errors_found: 0,
          final_corrected_sentence: statementText,
          errors_found: [],
        };
      }

      const errorTypesEnglish = causes.map(
        (causeId) => errorTypeMap[causeId]?.causeDesc || "Unknown"
      );
      const errorTypesArabic = causes.map(
        (causeId) => errorTypeMap[causeId]?.causeArabicDes || "Unknown"
      );

      result[docId][statementId].errors_found.push({
        errorID: errorId,
        errornuos_word: errorWord,
        errorType_English: errorTypesEnglish,
        errorType_Arabic: errorTypesArabic,
        correction: correctWord,
      });

      result[docId][statementId].number_of_errors_found += 1;

      return result;
    }, {});

    // Convert grouped errors to CSV data
    const csvData = Object.entries(groupedErrors).flatMap(
      ([docId, statements]) =>
        Object.entries(statements).map(([statementId, details]) => {
          const { final_corrected_sentence, errors_found } = details;

          // Start with the corrected sentence
          let erroneousSentence = final_corrected_sentence;

          // Replace corrections with error words
          errors_found.forEach(({ correction, errornuos_word }) => {
            const escapedCorrection = correction.replace(
              /[.*+?^${}()|[\]\\]/g,
              "\\$&"
            ); // Escape special characters
            const regex = new RegExp(escapedCorrection, "g"); // Remove \\b to match all occurrences
            console.log(
              `Trying to replace '${correction}' with '${errornuos_word}'`
            );
            console.log(`Regex used: ${regex}`);
            console.log("Before replacement:", erroneousSentence);

            if (regex.test(erroneousSentence)) {
              erroneousSentence = erroneousSentence.replace(
                regex,
                errornuos_word
              );
              console.log("After replacement:", erroneousSentence);
            } else {
              console.warn(
                `No match found for '${correction}' in '${erroneousSentence}'`
              );
            }
          });

          return {
            erroneous_sentence: erroneousSentence,
            output: JSON.stringify({
              docId,
              statementId,
              ...details,
            }),
          };
        })
    );

    // Write to CSV
    const csvWriter = createObjectCsvWriter({
      path: outputCsvFile,
      header: [
        { id: "erroneous_sentence", title: "erroneous_sentence" },
        { id: "output", title: "output" },
      ],
    });

    await csvWriter.writeRecords(csvData);
    console.log(`CSV file saved to ${outputCsvFile}`);
  } catch (err) {
    console.error("Error processing JSON data:", err.message);
  }
});
