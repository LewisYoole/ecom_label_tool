from tinydb import TinyDB, Query
from tqdm import tqdm

# Initialize TinyDB and select your table
db = TinyDB('db.json')
products_table = db.table('products')

# Retrieve all documents in the table
documents = products_table.all()

# Initialize a list to store doc_ids of documents with the specified label
doc_ids_with_pants = []

# Iterate over the documents
for doc in tqdm(documents, desc="generating related products"):
    if 'labels' in doc:
        for label in doc["labels"]:
            # Check if the label matches the specified criteria
            if label == {'attribute': 'garment_type', 'value': 'pants'}:
                # Append the doc_id to the list
                # Assuming `doc_id` is part of the document itself; adjust according to your schema
                doc_ids_with_pants.append(doc.doc_id)  # Use doc['doc_id'] if doc_id is within the document
                break  # Break the loop since we found a matching label

#iterate over the list of doc_ids_with_pants to display product names
print("\nRelated Products:\n")
for doc_id in doc_ids_with_pants:
    # Retrieve each document by its ID
    doc = products_table.get(doc_id=doc_id)
    # Assuming the product name is stored under the key 'name'
    product_name = doc.get('title', 'No name available')  # Provide a default value in case 'name' is not found
    print(f"Product Name: {product_name}")