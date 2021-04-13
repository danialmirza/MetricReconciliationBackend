import prestodb
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

# TODO: provide presto db configurations
conn = get_presto_conn(
    host='localhost',
    port=8080,
    user='test_user',
    catalog='test_catalog',
    schema='test_schema',
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

# TODO: transform rows into desired data structure to be stored in mongodb
