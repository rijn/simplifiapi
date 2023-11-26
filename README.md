# simplifiapi
An unofficial API for Quicken Simplifi

## CLI

This package provides a command-line tool that could access and save data to local files.

```shell
usage: __main__.py [-h] [--email [EMAIL]] [--password [PASSWORD]] [--token [TOKEN]] [--transactions] [--filename FILENAME] [--format {json,csv}]

optional arguments:
  -h, --help            show this help message and exit
  --email [EMAIL]       The e-mail address for your Quicken Simplifi account
  --password [PASSWORD]
                        The password for your Quicken Simplifi account
  --token [TOKEN]       Use existing token to bypass MFA check
  --transactions        Retrieve transactions
  --filename FILENAME   Write results to file this prefix
  --format {json,csv}   The format used to return data.

examples:
> python3 -m simplifiapi --token="..." --transactions
> python3 -m simplifiapi --token="..." --transactions --filename=20231125 --format=csv
```

## Python API

The `Client` class allows accessing from python script and making custom analysis.

```python
from simplifiapi.client import Client

client = Client()

# Provide either token or email/password
token = "..."
token = client.get_token(email=options.email, password=options.password)

assert client.verify_token(token)

# Datasets own transactions and accounts
datasets = client.get_datasets()
datasetId = datasets[0]["id"]

# Access transactions
transactions = client.get_transactions(datasetId)
```