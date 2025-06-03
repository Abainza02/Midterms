from sqlalchemy import create_engine, inspect, text

DATABASE_URL = "postgresql://bisan_unsa_user:Du1q6HeIUWxIqL4qSK4nNO6BegSMoDsm@dpg-d05n0c3uibrs73fs4eo0-a.oregon-postgres.render.com/bisan_unsa"
engine = create_engine(DATABASE_URL, client_encoding="utf8")

# Connect and inspect
connection = engine.connect()
inspector = inspect(engine)

# Get and print all table names
tables = inspector.get_table_names()
print("Tables in the database:")
for table in tables:
    print(f"- {table}")

# Print contents of each table
for table in tables:
    print(f"\nContents of table '{table}':")
    try:
        result = connection.execute(text(f"SELECT * FROM {table} LIMIT 10")) 
        rows = result.fetchall()
        if rows:
            for row in rows:
                print(dict(row._mapping))

        else:
            print("  (empty table)")
    except Exception as e:
        print(f"  Error reading table '{table}': {e}")