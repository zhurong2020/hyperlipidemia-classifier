import os
from PIL import Image
import pytesseract

def ocr_images_to_markdown(images_dir, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Iterate over all jpg files in the images directory
    for filename in os.listdir(images_dir):
        if filename.endswith('.jpg'):
            image_path = os.path.join(images_dir, filename)
            # Open the image file
            with Image.open(image_path) as img:
                # Use pytesseract to do OCR on the image
                text = pytesseract.image_to_string(img, lang='chi_sim+eng')  # Adjust language as needed

            # Create a markdown filename
            markdown_filename = os.path.splitext(filename)[0] + '.md'
            markdown_path = os.path.join(output_dir, markdown_filename)

            # Write the OCR text to a markdown file
            with open(markdown_path, 'w', encoding='utf-8') as md_file:
                md_file.write(text)

            print(f"Processed {filename} to {markdown_filename}")

if __name__ == "__main__":
    images_directory = os.path.join('docs', 'images')
    output_directory = os.path.join('docs', 'ocr_output')
    ocr_images_to_markdown(images_directory, output_directory) 