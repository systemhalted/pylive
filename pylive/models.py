from sqlalchemy import create_engine, Column, BigInteger, String, Sequence,\
                       Integer, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from db_test_constants import db_username, db_password, db_name, db_server
from datetime import datetime

engine = create_engine('postgresql://%s:%s@%s/%s'%(db_username, db_password,\
                                                  db_server, db_name))
Base = declarative_base()

class CodeSnippets(Base):
     __tablename__ = 'code_snippets'

     code_id = Column(BigInteger, Sequence('code_id_seq'), primary_key=True)
     code = Column(String, nullable=False)
     output = Column(String, nullable=False)
     created_at = Column(DateTime, default=datetime.now, nullable=False)

     def __init__(self, code, output):
         self.code = code
         self.output = output

     def __repr__(self):
         return "<CodeSnippets: code: %s, output: %s, code_id: %s>"%(self.code,\
                                                      self.output, self.code_id)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
db_session = Session()
