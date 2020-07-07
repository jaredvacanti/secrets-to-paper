import subprocess
import base64
import os
import io
import errno
import jinja2
import qrcode
from PIL import Image
from itertools import zip_longest
from weasyprint import HTML, CSS


templateLoader = jinja2.PackageLoader("secrets_to_paper", "templates")
templateEnv = jinja2.Environment(loader=templateLoader, keep_trailing_newline=True)


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def write_pdf_to_disk(rendered_html, output_file):

    html = HTML(string=rendered_html)
    css = templateEnv.get_template("main.css").render()

    css = CSS(string=css)

    html.write_pdf(
        output_file, stylesheets=[css],
    )

    return None


def get_qr_codes(data, chunk_size):
    """
    Expects binary data to be chunked into a list of base64 image strings
    """

    qr_codes = []
    for chunk in grouper(data, chunk_size):
        chunk = [x for x in chunk if x]

        # Set version to None and use the fit parameter when making the code to
        # determine this automatically.
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=2,
            border=4,
        )

        qr.add_data(bytes(chunk))
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())

        qr_codes.append(img_str)

    return qr_codes
