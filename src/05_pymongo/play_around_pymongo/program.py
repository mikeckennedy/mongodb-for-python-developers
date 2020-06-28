import pymongo

conn_str = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn_str)

db = client.the_small_bookstore

# NOTE: In the video we use db.books.count(), it's been deprecated for more explicit
# versions. See
# https://api.mongodb.com/python/current/api/pymongo/collection.html#pymongo.collection.Collection.estimated_document_count
# for details

if db.books.estimated_document_count() == 0:
    print("Inserting data")
    # insert some data...
    r = db.books.insert_one({'title': 'The third book', 'isbn': '73738584947384'})
    print(r, type(r))
    r = db.books.insert_one({'title': 'The forth book', 'isbn': '181819884728473'})
    print(r.inserted_id)
else:
    print("Books already inserted, skipping")

# book = db.books.find_one({'isbn': '73738584947384'})
# # print(book, type(book))
# # book['favorited_by'] = []
# book['favorited_by'].append(100)
# db.books.update({'_id': book.get('_id')}, book)
# book = db.books.find_one({'isbn': '73738584947384'})
# print(book)

# NOTE: In the video we use db.books.update(), migrated to update_one() as update() is deprecated.
db.books.update_one({'isbn': '181819884728473'}, {'$addToSet': {'favorited_by': 120}})
book = db.books.find_one({'isbn': '181819884728473'})
print(book)
