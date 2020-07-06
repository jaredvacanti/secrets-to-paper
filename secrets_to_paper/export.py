import subprocess
import base64
import os
import io
import errno
import jinja2
import pdfkit
import qrcode
from PIL import Image
from itertools import zip_longest

templateLoader = jinja2.PackageLoader("secrets_to_paper", "templates")
templateEnv = jinja2.Environment(loader=templateLoader, keep_trailing_newline=True)


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def render_gpg_html(paperkey_b16, ascii_key, qr_images=[]):

    template = templateEnv.get_template("gpg_key.html")

    rendered = template.render(
        qr_images=qr_images, paperkey_b16=paperkey_b16, ascii_key=ascii_key
    )

    return rendered


def render_rsa_html(ascii_key, qr_images=[], key_label=""):

    template = templateEnv.get_template("rsa_key.html")

    rendered = template.render(
        qr_images=qr_images, ascii_key=ascii_key, key_label=key_label
    )

    return rendered


def render_ecc_html(ascii_key, qr_images=[], key_label=""):

    template = templateEnv.get_template("ecc_key.html")

    rendered = template.render(
        qr_images=qr_images, ascii_key=ascii_key, key_label=key_label
    )

    return rendered


def write_pdf_to_disk(html, output_file):

    options = {"quiet": ""}
    pdfkit.from_string(html, output_file, options=options)

    return None


def export_ecc(pemdata, output, key_label=""):
    qr_codes = []
    for chunk in grouper(pemdata, 400):
        chunk = [x for x in chunk if x]

        # Set version to None and use the fit parameter when making the code to
        # determine this automatically.
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=2,
            border=4,
        )

        qr.add_data(chunk)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())

        qr_codes.append(img_str)

    filename = output + ".pdf"
    rendered = render_ecc_html(
        pemdata.decode("ascii"), qr_images=qr_codes, key_label=key_label
    )

    write_pdf_to_disk(rendered, filename)


def export_rsa(pemdata, output, key_label=""):
    qr_codes = []
    for chunk in grouper(pemdata, 400):
        chunk = [x for x in chunk if x]

        # Set version to None and use the fit parameter when making the code to
        # determine this automatically.
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=2,
            border=4,
        )

        qr.add_data(chunk)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())

        qr_codes.append(img_str)

    filename = output + ".pdf"
    rendered = render_rsa_html(
        pemdata.decode("ascii"), qr_images=qr_codes, key_label=key_label
    )

    write_pdf_to_disk(rendered, filename)


def export_gpg_b64(key_id):
    """
    Export a gpg key using the paperkey subcommand
    """

    secret = subprocess.run(["gpg", "--export-secret-key", key_id], capture_output=True)
    secret_key_ascii = subprocess.run(
        ["gpg", "--export-secret-key", "--armor", key_id], capture_output=True
    ).stdout.decode("ascii")

    # used for producing QR codes (paperkey pulls relevant secret bits)
    paperkey_raw = subprocess.run(
        ["paperkey", "--output-type", "raw"], input=secret.stdout, capture_output=True
    )

    # used for produces textual output
    paperkey = subprocess.run(
        ["paperkey", "--output-type", "base16"],
        input=secret.stdout,
        capture_output=True,
    )
    paperkey_output = paperkey.stdout.decode("utf-8")

    # split the private bits of the QR-code into 150-byte chunks

    qr_codes = []
    for chunk in grouper(paperkey_raw.stdout, 150):
        chunk = [x for x in chunk if x]

        # Set version to None and use the fit parameter when making the code to
        # determine this automatically.
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=2,
            border=4,
        )

        qr.add_data(chunk)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())

        qr_codes.append(img_str)

    filename = key_id + ".pdf"
    render_gpg_html()

    write_pdf_to_disk(filename, paperkey_output, secret_key_ascii, qr_images=qr_codes)
