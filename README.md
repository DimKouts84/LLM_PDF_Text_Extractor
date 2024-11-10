# Local LLM PDF Text Extractor

This script extracts text from images embedded within a PDF file, structures the data, and outputs it in a Markdown format.
The extracted text is structured based on the formatting instructions and saved as a Markdown file.

## Features

- Converts each page of a PDF into an image.
- Extracts text from each image using a Large Language Model (LLM) API (specifically `Ollama API`).
- Structures the extracted text in Markdown format.
- Outputs the structured text as a `.md` file.

## Requirements

- Python 3.8+
- Libraries: `requests`, `fitz` (from PyMuPDF), `dotenv`

Install the required libraries using:

```bash
pip install requests pymupdf python-dotenv
```

## Setup

1. Clone the repository.
2. Install the required libraries.
3. Add `.env` file with the following environment variables:

```makefile
OLLAMA_COMPLETIONS_URL=`<Your Ollama API URL>`
OLLAMA_CHAT_COMPLETIONS_URL=`<Your Ollama Chat API URL>`
```


4. Place your PDF file in the root directory or specify the correct path in the `pdf_path` variable.

## Usage

To run the script, simply execute:

```python
python script.py
```


### Parameters

* **`pdf_path`** : Set this variable to the path of the PDF file you wish to process.
* **`output_folder`** (optional): Directory where page images will be temporarily saved.

### Workflow

1. **Convert PDF to Images** : Each page in the PDF is converted to an image and stored in the specified output folder.
2. **Encode Images** : Each image is converted to base64 for API transmission.
3. **Extract Text** : Using the Ollama API, text is extracted from each image.
4. **Structure Output** : The extracted text is structured in Markdown format and saved as a `.md` file.

## Example Output

The output is saved as a Markdown file (`extracted_text.md`) with structured text extracted from the PDF images.

## Important Notes

* **API Requirements** : Ensure that your API keys and URLs for the Ollama API are set correctly in the `.env` file.
* **File Cleanup** : Temporary images created during the process are automatically deleted.
