import sqlalchemy as sql


class Schema:
    def __init__(self, name, engine):
        self.engine = engine
        self.MD = sql.MetaData(schema=name)

    def __getattr__(self, name):
        setattr(self, name, sql.Table(
            name, self.MD, autoload=True, autoload_with=self.engine
        ))
        return getattr(self, name)


class DB:
    def __init__(self, conn_url):
        self.engine = sql.create_engine(conn_url)

    @property
    def conn(self):
        return self.engine.connect()

    def execute(self, *args, **kwargs):
        return self.conn.execute(*args, **kwargs)

    def select(self, *args):
        return sql.select(args)

    def __getattr__(self, name):
        setattr(self, name, Schema(name, self.engine))
        return getattr(self, name)


