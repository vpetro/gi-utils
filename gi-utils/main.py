import sys
import os
import csv
import pypdf
import argparse


def search_pdf(pdf_path: str, search_text: str) -> list[int]:
    """
    Search a PDF file for specific text and return page numbers
    where the text is found.

    Args:
        pdf_path: Path to the PDF file
        search_text: Text to search for (case-sensitive)

    Returns:
        List of page numbers (1-based) containing the search text
    """

    matching_pages = []

    with open(pdf_path, "rb") as file:
        reader = pypdf.PdfReader(file)

        for page_num, page in enumerate(reader.pages, 1):
            if search_text in page.extract_text():
                matching_pages.append(page_num)

    return matching_pages


def search_with_csv(pdf_path: str, csv_path: str):
    output_csv = os.path.join(
        os.path.dirname(os.path.abspath(csv_path)), "search_result.csv"
    )

    with open(output_csv, "w") as output:
        writer = csv.DictWriter(
            output, fieldnames=["search_term", "pages"], dialect=csv.excel_tab
        )

        with open(csv_path) as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                search_term = row["search_term"]
                result = [str(i) for i in search_pdf(pdf_path, search_term)]

                writer.writerow({"search_term": search_term, "pages": ",".join(result)})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "pdf_filename", help="The path to the PDF document to be searched"
    )
    parser.add_argument("csv_filename", help="The term to search in the PDF document")
    args = parser.parse_args()

    if not os.path.isfile(args.pdf_filename):
        print(f"Error: path '{args.pdf_filename}' is not a file.")
        sys.exit()

    if not os.path.isfile(args.pdf_filename):
        print(f"Error: path '{args.csv_filename}' is not a file.")
        sys.exit()

    results = search_with_csv(args.pdf_filename, args.csv_filename)
    print("DONE! Results are in 'search_results.csv' file")
