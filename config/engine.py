import os
from sqlalchemy import create_engine


class InternalDatabaseConfiguration:
    DB_URL = os.environ.get('DB_URL')
    BATCH_SIZE = 1000

    engine = None

    @classmethod
    def get_engine(cls):
        if cls.engine is None:
            cls.engine = create_engine(
                cls.DB_URL,
                echo=False,
                executemany_mode='values',
                executemany_values_page_size=cls.BATCH_SIZE
            )
        return cls.engine
