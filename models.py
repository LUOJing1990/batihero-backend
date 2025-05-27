from sqlalchemy import create_engine, Column, Integer, Float, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class WindowType(Base):
    __tablename__ = 'window_types'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)    # 窗户类型名称，例如 'CF'
    entries = relationship("PriceEntry", back_populates="window_type")

class PriceEntry(Base):
    __tablename__ = 'price_entries'
    id = Column(Integer, primary_key=True)
    window_type_id = Column(Integer, ForeignKey('window_types.id'))
    width = Column(Integer)               # 宽度 (mm)
    height = Column(Integer)              # 高度 (mm)
    price = Column(Float)                 # 价格 (€)
    window_type = relationship("WindowType", back_populates="entries")

engine = create_engine('sqlite:///batihero.db', echo=False)
Session = sessionmaker(bind=engine)
