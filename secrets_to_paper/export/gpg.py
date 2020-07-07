import subprocess
from secrets_to_paper.export import write_pdf_to_disk, get_qr_codes
from secrets_to_paper.export import templateEnv, templateLoader


def render_gpg_html(
    paperkey_b16,
    ascii_key,
    qr_images=[],
    public_qr_images=[],
    public_key_ascii="",
    key_id="",
):

    template = templateEnv.get_template("gpg_key.html")

    rendered = template.render(
        qr_images=qr_images,
        paperkey_b16=paperkey_b16,
        ascii_key=ascii_key,
        public_key_ascii=public_key_ascii,
        key_id=key_id,
        public_qr_images=public_qr_images,
    )

    return rendered


def export_gpg(key_id):
    """
    Export a gpg key using the paperkey subcommand
    """

    secret = subprocess.run(["gpg", "--export-secret-key", key_id], capture_output=True)
    secret_key_ascii = subprocess.run(
        ["gpg", "--export-secret-key", "--armor", key_id], capture_output=True
    ).stdout.decode("ascii")

    public_key = subprocess.run(
        ["gpg", "--export", "--armor", key_id], capture_output=True
    ).stdout

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

    qr_codes = get_qr_codes(paperkey_raw.stdout, 400)
    public_qr_codes = get_qr_codes(public_key, 400)

    filename = key_id + ".pdf"

    rendered = render_gpg_html(
        paperkey_output,
        secret_key_ascii,
        public_key_ascii=public_key.decode("ascii"),
        qr_images=qr_codes,
        public_qr_images=public_qr_codes,
        key_id=key_id,
    )

    write_pdf_to_disk(rendered, filename)
