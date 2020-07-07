from secrets_to_paper.export import templateEnv, templateLoader


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

        qr.add_data(bytes(chunk))
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
    for chunk in grouper(pemdata, 600):
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

    filename = output + ".pdf"
    rendered = render_rsa_html(
        pemdata.decode("ascii"), qr_images=qr_codes, key_label=key_label
    )

    write_pdf_to_disk(rendered, filename)

