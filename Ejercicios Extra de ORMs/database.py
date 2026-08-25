from sqlalchemy import create_engine, inspect
from sqlalchemy.schema import CreateSchema
from sqlalchemy.orm import sessionmaker
from models import Base

DB_URL = 'postgresql://postgres:280596@localhost:5432/postgres'
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)


SCHEMA_NAME = 'sqlalchemy'

def validate_connection():
    try:
        with engine.connect() as connection:
            print("Connection to the database was successful.")
    except Exception as e:
        print(f"An error occurred while connecting to the database: {e}")

def validate_and_create_schema():
    try:
        with engine.begin() as connection:
            # Check if the schema exists
            inspector = inspect(engine)
            if SCHEMA_NAME not in inspector.get_schema_names():
                print(f"Schema '{SCHEMA_NAME}' does not exist. Creating schema...")
                connection.execute(CreateSchema(SCHEMA_NAME))
                print(f"Schema '{SCHEMA_NAME}' created successfully.")
            else:
                print(f"Schema '{SCHEMA_NAME}' already exists.")
    except Exception as e:
        print(f"An error occurred while validating/creating the schema: {e}")

def validate_and_create_tables():
    try:
        inspector = inspect(engine)
        # Check if the required tables exist in the schema
        required_tables = ['users', 'addresses', 'cars']
        existing_tables = inspector.get_table_names(schema=SCHEMA_NAME)

        missing_tables = [table for table in required_tables if table not in existing_tables]

        if missing_tables:
            print(f"Missing tables in schema '{SCHEMA_NAME}': {missing_tables}")
            Base.metadata.create_all(engine)
            print("Tables created successfully.")
        else:
            print(f"All required tables already exist in schema '{SCHEMA_NAME}'.")


    except Exception as e:
        print(f"An error occurred while creating tables: {e}")


# if __name__ == "__main__":
#     validate_connection()
#     validate_and_create_schema()
#     validate_and_create_tables()