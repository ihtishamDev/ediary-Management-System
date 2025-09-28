from sqlalchemy import create_engine, inspect

engine = create_engine("sqlite:///C:/Users/dell/Desktop/ediary-project/data.db")
insp = inspect(engine)

for col in insp.get_columns("users"):
    print(col["name"], col["type"])
