import pymongo

conn_str = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn_str)

db = client.the_small_bookstore

if db.books.count() == 0:
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


db.books.update({'isbn': '181819884728473'}, {'$addToSet': {'favorited_by': 120}})
book = db.books.find_one({'isbn': '181819884728473'})
print(book)
