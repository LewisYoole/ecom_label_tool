from tinydb import TinyDB, Query
from tqdm import tqdm
from open_ai_image_labelling import open_api_image_reader

# Initialize TinyDB and select your table
db = TinyDB('db.json')
products_table = db.table('products')

categories_table = db.table('categories')


# Retrieve all documents in the table
documents = products_table.all()

# Iterate over the documents and print the "title" of each one
for doc in tqdm(documents, desc="Updating Products"):
    if 'image_link' in doc:
        if doc['image_link'] != 'None':  # Check if the 'title' field exists
            #runs the image URL thru, downloading and Open AI processing
            labels_return = open_api_image_reader(doc['image_link'])
            #updates table with new ai generated labels
            products_table.update({'labels': labels_return}, doc_ids=[doc.doc_id])