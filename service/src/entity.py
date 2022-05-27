from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, JSON
from sqlalchemy.orm import declarative_base, relationship

from config.engine import InternalDatabaseConfiguration

Base = declarative_base()


class Bioobject(Base):
    __tablename__ = "bioobject"

    uuid = Column(String, nullable=False, primary_key=True)

    analysis = relationship("Analysis", lazy="immediate", backref="bioobject", uselist=False)


class Analysis(Base):
    __tablename__ = "analysis"
    id = Column(Integer, primary_key=True)
    bioobject_uuid = Column(String, ForeignKey("bioobject.uuid"), nullable=False)
    content = Column(JSON, nullable=False)


Base.metadata.create_all(InternalDatabaseConfiguration.get_engine())
