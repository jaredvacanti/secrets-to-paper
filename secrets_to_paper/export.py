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


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def write_secret_to_disk(output_file, paperkey_b16, qr_images=[]):

    templateLoader = jinja2.PackageLoader("secrets_to_paper", "templates")
    templateEnv = jinja2.Environment(loader=templateLoader, keep_trailing_newline=True)
    template = templateEnv.get_template("secret_output.html")

    options = {"quiet": ""}

    rendered = template.render(qr_images=qr_images, paperkey_b16=paperkey_b16)

    pdfkit.from_string(rendered, output_file, options=options)

    return None


def export_gpg_b64(key_id):
    """
    Export a gpg key using the paperkey subcommand
    """

    secret = subprocess.run(["gpg", "--export-secret-key", key_id], capture_output=True)

    paperkey_raw = subprocess.run(
        ["paperkey", "--output-type", "raw"], input=secret.stdout, capture_output=True
    )

    paperkey = subprocess.run(
        ["paperkey", "--output-type", "base16"],
        input=secret.stdout,
        capture_output=True,
    )
    paperkey_output = paperkey.stdout.decode("utf-8")

    qr_codes = []
    for chunk in grouper(paperkey_raw.stdout, 50):
        chunk = [x for x in chunk if x]

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        qr.add_data(chunk)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())

        qr_codes.append(img_str)

        # imgByteArr = buffered.getvalue()

        # with open("test.jpeg", "wb") as f:
        #     f.write(imgByteArr)
        #     f.close()

        # break

    write_secret_to_disk("output.pdf", paperkey_output, qr_images=qr_codes)
