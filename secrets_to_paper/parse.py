import subprocess
import base64
import ast
from pdf2image import convert_from_path, convert_from_bytes
from pyzbar.pyzbar import decode


def pdf_to_secret(pdf_file):
    pages = convert_from_path(pdf_file)

    qr_codes = []
    for page in pages:

        codes = decode(page)
        for code in codes:
            qr_codes += ast.literal_eval(code.data.decode("ascii"))

    print(qr_codes)
