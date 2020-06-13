# secrets-to-paper

A command-line tool to convert secret keys to printable PDFs and to parse those
PDFs back to usable secret keys.

Note: Python 3.8+ is required to use this simple package. Python 3.8 introduced
a new computation for
[modular inverses](https://docs.python.org/3/library/functions.html#pow).

> Changed in version 3.8: For int operands, the three-argument form of pow now
> allows the second argument to be negative, permitting computation of modular
> inverses.

## Usage

```
secrets-to-paper 
```

## Development

#### Initializing a virtual environment:

```
pyenv local 3.8.3
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