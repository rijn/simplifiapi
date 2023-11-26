# simplifiapi
An unofficial API for Quicken Simplifi

## Python API

The `Client` class allows accessing from python script and making custom analysis.

```
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