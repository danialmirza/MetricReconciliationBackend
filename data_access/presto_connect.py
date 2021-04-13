# Reference: https://etwiki.sys.comcast.net/display/DX/Python+Clients

import prestodb
from getpass import getpass

# import query_builder


server = {
    "host": "query.comcast.com",
    "port": 4443,
    "ca_bundle": "./query.comcast.com.pem",
}

user_credentials = {
    "user": getpass.getuser(),
    "pass": getpass("password:"),  # TODO: verify if password can be retrieved properly
}


class enhancedAuth(presto.auth.BasicAuthentication):
    def __init__(
        self,
        username,
        password,
        ca_bundle=None,  # type: Optional[Text]
    ):
        super().__init__(username, password)
        self._ca_bundle = ca_bundle

    def set_http_session(self, http_session):
        http_session = super().set_http_session(http_session)
        if self._ca_bundle:
            http_session.verify = self._ca_bundle
        return http_session


def get_presto_conn(host, port, user, catalog, schema, http_scheme, auth):
    conn = prestodb.dbapi.connect(
        host=host,
        port=port,
        user=user,
        catalog=catalog,
        schema=schema,
        http_scheme=http_scheme,
        auth=auth,
    )
    return conn


if __name__ == "__main__":
    # authenticate
    _auth = enhancedAuth(
        username=user_credentials["user"],
        password=user_credentials["pass"],
        ca_bundle=server["ca_bundle"],
    )

    # connect to presto db
    conn = get_presto_conn(
        host=server["host"],
        port=server["port"],
        user=user_credentials["user"],
        catalog="test_catalog",
        schema="test_schema",
        http_scheme="https",
        auth=_auth,
    )
    cur = conn.cursor()

    # query presto db
    try:
        # TODO: get query from query_builder
        query = "SELECT * FROM test_db"

        cur.execute(query)
        rows = cur.fetchall()

    finally:
        cur.close()
        conn.close()

    # return query data
    # TODO: return rows to react application for visuals
