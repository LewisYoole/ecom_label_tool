from tinydb import TinyDB, Query

# Load the database
db = TinyDB('db.json')

# Get all table names
table_names = db.tables()

# Iterate through each table
for table_name in table_names:
    table = db.table(table_name)  # Access the table

    # Fetch all records in the table
    records = table.all()

    # Check if the table has more than 10 records
    if len(records) > 10:
        # If so, remove records starting from the 11th
        ids_to_remove = [record.doc_id for record in records[10:]]
        table.remove(doc_ids=ids_to_remove)

print("Database update complete. Each table now has a maximum of 10 records.")
