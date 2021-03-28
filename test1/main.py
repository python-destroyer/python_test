import csv
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://dbUser:mypassword@cluster0.fq8xs.mongodb.net/db?retryWrites=true&w=majority")
db = cluster['randomdata']
collection = db['randomcoll']

def ConvertToCollection(row):
    doc = {'one': row[0], 'two': row[1], 'three': row[2], 'four': row[3],'five': row[4],'six': row[5]}
    return doc

def main():
    #uploading data from csv file
    csv_file = 'random_data.csv'
    with open(csv_file, 'r') as f:
        read = csv.reader(f)
        collection.delete_many({})
        post = map(ConvertToCollection, read)
        collection.insert_many(post,ordered=False)

    #delete docs where "three" field starts with a letter
    collection.delete_many({"three": {"$regex" : "^[a-zA-Z]"}})
    #в случае если под удалением записи имеется в виду запись пробела в третье поле документа
    #закоментировать предыдущую строку и раскоментировать нижнюю
    # collection.update_many({"three": {"$regex" : "^[a-zA-Z]"}}, {"$set": { "three" : " " }})

    cluster.close()

if __name__ == "__main__":
   main()