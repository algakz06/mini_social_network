from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
