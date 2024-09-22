import pymongo

from pymongo import MongoClient
client=MongoClient()


db=client.test_database
collection=db.test_collection

# connexion to the cluster
cluster=MongoClient('mongodb+srv://mrsamu35:Samuel35-@players.lahd6.mongodb.net/?retryWrites=true&w=majority&appName=Players')

#database
db=cluster['Ligues']
collection=db['ligues_info']
# results=collection.delete_many({})


# add something in the collection
post={"_id":0,'name':'tim','score':5}

collection.insert_one(post)


# insert multiple post
post1={"_id":2,'name':'joe','score':5}
post2={"_id":3,'name':'john','score':5}

collection.insert_many([post1,post2])


#access to element
results=collection.find_one({"_id":2})

print(results)

#if we went only certain attributes
for result in results:
    print(result["score"])


# return eveything
results=collection.find({})
for x in results:
    print(x)


# delete
results=collection.delete_one({'name':"tim"})
results=collection.delete_many({'name':"tim"})


#update
result=collection.update_one({'_id':2},{'$set':{'name':'tim'}})

#add new attribute
result=collection.update_one({'_id':2},{'$set':{'hello':5}})
# result=collection.update_many({'_id':2,...},{'$set':{'hello':'tim'}})


# add a number to a integer
result=collection.update_one({'_id':2},{'$inc':{'hello':5}})

# count number of document that meet a criteria

#everything
post_count=collection.count_documents({})
print(post_count)



