# from sqlalchemy import create_engine , MetaData , Table
# engine = create_engine('sqlite:///census_nyc.sqlite')

# connection = engine.connect()

# metadata = MetaData()
# census = Table('census', metadata, autoload=True, autoload_with=engine)
# print(repr(census))




## --------------------------------------------
from sqlalchemy import * 
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Todo(Base):
	__tablename__ = 'todos'

	id = Column(Integer, primary_key=True)
	name = Column(String(255), unique=True)
	created_ts = Column(DateTime)

if __name__ == "__main__":
	engine = create_engine('sqlite:///./database.db')
	Base.metadata.create_all(bind=engine)