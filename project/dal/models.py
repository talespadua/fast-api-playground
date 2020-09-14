from sqlalchemy import (  # type: ignore[import]
    Column,
    Integer,
    ForeignKey,
    Numeric,
    BigInteger,
    TIMESTAMP,
    String,
    Index,
)
from sqlalchemy.ext.declarative import declarative_base  # type: ignore[import]

from datetime import datetime


Base = declarative_base()


class OrderModel(Base):  # type: ignore
    __tablename__ = "orders"

    id = Column(BigInteger, primary_key=True)
    code = Column(Integer, nullable=False)
    value = Column(Numeric, nullable=False)
    retailer_document = Column(
        String(30), ForeignKey("retailers.document"), nullable=False
    )
    status = Column(String(80), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow(), nullable=False)
    cashback = Column(Numeric, nullable=True)


class RetailerModel(Base):  # type: ignore
    __tablename__ = "retailers"

    id = Column(Integer, primary_key=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    document = Column(String(30), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)

    __table_args__ = (
        Index("document", "document", unique=True),
        Index("email", "email", unique=True),
    )
