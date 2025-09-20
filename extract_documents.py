import os
from pathlib import Path
from unstructured.partition.auto import partition

def extract_and_save(input_folder: str, output_folder: str):
    """
    Extracts text from documents in the input_folder and saves them as .txt files
    in the output_folder, using robust settings for the unstructured library.
    """
    # Ensure the output directory exists
    Path(output_folder).mkdir(exist_ok=True, parents=True)

    # Get a list of all files in the input directory
    try:
        files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]
    except FileNotFoundError:
        print(f"Error: The input directory '{input_folder}' was not found.")
        return

    if not files:
        print(f"No files found in the '{input_folder}' directory.")
        return

    for filename in files:
        input_path = os.path.join(input_folder, filename)
        output_filename = os.path.splitext(filename)[0] + ".txt"
        output_path = os.path.join(output_folder, output_filename)

        print(f"Processing {filename}...")
        try:
            # Partition the document using recommended high-quality settings
            # This uses the most current arguments to avoid deprecation issues.
            elements = partition(
                filename=input_path,
                strategy="hi_res",  # Use the high-resolution strategy for better layout detection
                languages=["eng"],     # Specify language for OCR; critical for accuracy
                infer_table_structure=True # This is a key parameter for quality table extraction
            )

            # Convert the extracted elements into a single text string
            text = "\n\n".join([str(el) for el in elements])

            # Write the extracted text to the output file
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)

            print(f"Successfully saved extracted text to {output_path}")

        except Exception as e:
            # Catch and print any error during processing to help with debugging
            print(f"--- ERROR processing {filename}: {e} ---")
            # This will help identify if the issue is with a specific file or a general setup problem.

if __name__ == "__main__":
    # It's good practice to define these as variables for easy changes
    documents_directory = "documents"
    output_directory = "output"
    extract_and_save(documents_directory, output_directory)
    print("\nExtraction process finished.")
