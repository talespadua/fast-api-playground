from sqlalchemy import Column, Integer, String, Index  # type: ignore[import]
from ._base import Base


class RetailerModel(Base):  # type: ignore
    __tablename__ = "retailers"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(100))
    document = Column(String(30))
    email = Column(String(50))
    password = Column(String(100))
    __table_args__ = (
        Index("document", "document", unique=True),
        Index("email", "email", unique=True),
    )
