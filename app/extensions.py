import pymongo, os

uri = 'mongodb+srv://'+os.getenv('username')+':'+os.getenv('password')+'@testdb.qdtpetw.mongodb.net/?retryWrites=true&w=majority&appName=TestDB'

client = pymongo.MongoClient(uri)