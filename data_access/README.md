# Connect using Python Presto connector
- Use the following steps to connect to Presto DB

### 1. Download the certificate for the server

```
cd path/to/MetricReconciliationBackend/data_access
bash get_pem.sh

ls  # verify that query.comcast.com.pem is created
```

### 2. Test presto_connect.py
```
python3 presto_connect.py
```