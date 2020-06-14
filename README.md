# secrets-to-paper

A command-line tool to convert secret keys to printable PDFs and to parse those
PDFs back to usable secret keys.

Note: Python 3.8+ is required to use this simple package. Python 3.8 introduced
a new computation for
[modular inverses](https://docs.python.org/3/library/functions.html#pow).

> Changed in version 3.8: For int operands, the three-argument form of pow now
> allows the second argument to be negative, permitting computation of modular
> inverses.

## Dependencies

[Paperkey](http://www.jabberwocky.com/software/paperkey/) is a command line tool
to export GnuPG keys on paper. It reduces the size of the exported key, by
removing the public key parts from the private key. Paperkey also includes
CRC-24 checksums in the key to allow the user to check whether their private key
has been restored correctly.

- paperkey (for GPG keys)
- zbar/libzbar0


## Development

#### Initializing a virtual environment:

```
pyenv shell 3.8.3
python -m venv .venv
pip install --upgrade pip
pip install poetry
poetry install
```

This makes an executable `secrets-to-paper` available in your `$PATH` after poetry
installations. During development, it's often more convenient to run

```
poetry run secrets-to-paper <private-key-path>
```


## Testing

You can generate a private and public key for testing purposes using `openssl`.

```
poetry run tox
```
