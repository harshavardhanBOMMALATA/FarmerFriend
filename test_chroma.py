import chromadb

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection("paddy_knowledge")

print(collection.count())