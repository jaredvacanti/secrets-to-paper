import subprocess
import base64
from pdf2image import convert_from_path, convert_from_bytes
from pyzbar.pyzbar import decode


def pdf_to_secret(pdf_file):
    pages = convert_from_path(pdf_file)

    print(pages)
    for page in pages:

        codes = decode(page)
        for code in codes:
            print(code.data.decode("ascii"))

