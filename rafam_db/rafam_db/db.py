from sqlalchemy import create_engine

SQLALCHEMY_URI_TMPL = 'oracle://%(username)s:%(password)s@%(host)s/%(sid)s'

def init_engine(username, password, host, sid, debug=False):
    uri = SQLALCHEMY_URI_TMPL % { 'username': username, 'password': password, 'host': host, 'sid': sid }
    engine = create_engine(uri, echo=debug)
    return engine
