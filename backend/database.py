from model import Todo

#mongoDB driver
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
#creating a database and a collection(table)
database = client.TodoList
collection = database.todo

'''
the insert_one, find_one, find are the mongoDB methods inside our python file
where the motor module helps us to link with the mongoDB 

'''
#fetch one the details by todo list title name
async def fetch_one_todo(title):
    document = await collection.find_one({"title":title})
    return document

#to get all the todo 's 
async def fetch_all_todos():
    todos =[]
    cursor = collection.find({})
    async for document in cursor:
        todos.append(Todo(**document))
    return todos

#to create a todo
async def create_todo(todo):
    document = todo
    #in order to wait for the collection to insert into that collection
    result = await collection.insert_one(document)
    return document

#update-> which item we want to update , choose by title , and update it with actual desc to update
async def update_todo(title, desc):
    await collection.update_one({"title":title},{"$set":{
        "description":desc
    }})
    document = await collection.find_one({"title":title})
    return document

#delete a todo
async def remove_todo(title):
    await collection.delete_one({"title":title})
    return True
