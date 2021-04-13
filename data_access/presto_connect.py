import prestodb
from getpass import getpass
# import query_builder


def get_presto_conn(host, port, user, catalog, schema):
    conn=prestodb.dbapi.connect(
        host=host,
        port=port,
        user=user,
        catalog=catalog,
        schema=schema,
    )
    return conn

conn = get_presto_conn(
    host='query.comcast.com',
    port=4443,
    user='dmirza509',
    catalog='test_catalog',
    schema='test_schema',
    http_scheme='https',
    auth=prestodb.auth.BasicAuthentication("dmirza509", getpass("password:"))
    )
cur = conn.cursor()

try:
    # TODO: get query from query_builder
    query = "SELECT * FROM test_db"

    cur.execute(query)
    rows = cur.fetchall()

finally:
    cur.close()
    conn.close()

# TODO: return rows to react application for visuals
