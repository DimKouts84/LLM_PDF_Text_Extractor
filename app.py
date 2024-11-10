# This script will take a PDF as input and extract the text from the images in the PDF file.
# Then it will structure the data and outpu a Markdown file.

import base64, json, os, requests
import fitz  # PyMuPDF
from dotenv import load_dotenv

# Define Variables:
load_dotenv()
ollama_completions_url = os.getenv("OLLAMA_COMPLETIONS_URL")
ollama_chat_completions_url = os.getenv("OLLAMA_CHAT_COMPLETIONS_URL")
model = "llama3.2-vision:11b"

# Example usage
pdf_path = "book.pdf"

# Keeping track of Tokens used
tokens_used = 0
number_of_pages = 0

# Functions to read the PDF file and extract the text from the images.
# Then extract the data and finally structure them based on instructions.

# Function to encode the image in base64
def convert_pdf_to_images(pdf_path, output_folder='images'):

    # Ensure the output directory exists
    os.makedirs(output_folder, exist_ok=True)

    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    image_paths = []

    # Iterate over each page
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)  # Load the page
        pix = page.get_pixmap()  # Render page to an image
        output_path = os.path.join(output_folder, f"page_{page_num + 1}.png")
        pix.save(output_path)  # Save the image
        image_paths.append(output_path)

    pdf_document.close()
    return image_paths


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Function to extract text from multiple images using an LLM model
def extract_text_from_images(base64_images):
    global tokens_used  # Declare global variable
    
    # Initialize an empty list to accumulate the results
    extracted_texts = []
    
    # Call the Ollama API individually for each image
    for image in base64_images:
        # Ollama URL
        url = ollama_chat_completions_url
        
        # Payload to send to the API for each image
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are responsible for reading through books, essays, and articles and extracting necessary information from their images."
                               "You are accurate in your extraction, you **FOLLOW** and you **DO NOT** hallucinate."
                },
                {
                    "role": "user", 
                    "content": ("You will read the images and extract the text from them. You will have to structure it using markdown. "
                               + "Feel free to create tables whenever necessary."
                               + "The output must be ONLY the extracted text in a markdown format> NOTHING ELSE, only the text from the images in a structured format."
                               ),
                    "images": [image]
                }
            ],
            "stream": False,
            "options": {
                "temperature": 0
            }
        }
        headers = {
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()  # Raise an error for bad status codes
            extracted_texts.append(response.json()['message']['content'])
        except requests.exceptions.RequestException as e:
            print(f"Error extracting text from image: {e}")
            extracted_texts.append("")  # Append empty if there's an error
    
    # Join all extracted texts
    return "\n".join(extracted_texts)


# Function to extract text from images in batches
def extract_text_from_images_in_batches(base64_images, batch_size=6):
    all_extracted_text = []
    for i in range(0, len(base64_images), batch_size):
        batch = base64_images[i:i + batch_size]
        batch_text = extract_text_from_images(batch)
        all_extracted_text.append(batch_text)
    return '\n'.join(all_extracted_text)

# Final function that uses the `convert_pdf_to_images`, `encode_image`, `extract_text_from_images` functions 
# To process the PDF file and extract all the text
def process_pdf(pdf_path):
    images = convert_pdf_to_images(pdf_path)
    base64_images = [encode_image(image_path) for image_path in images]
    all_text = extract_text_from_images_in_batches(base64_images)
    
    for image_path in images:
        os.remove(image_path)  # Clean up image files

    # save the extracted text to a text file
    # txt_file_path = os.path.join(os.path.dirname(pdf_path), "extracted_text.txt")
    
    # Save the extracted text to a markdown file
    txt_file_path = os.path.join(os.path.dirname(pdf_path), "extracted_text.md")
   
    with open(txt_file_path, "w", encoding='utf-8') as text_file:
        text_file.write(all_text)


    return all_text

# Call the function to process the PDF file
process_pdf(pdf_path)
# save the extracted text to a markdown file
