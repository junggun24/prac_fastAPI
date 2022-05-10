
from fastapi import FastAPI

from enum import Enum

from fastapi import FastAPI,Query

from typing import List,Optional

from pydantic import BaseModel

######

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

#######

app = FastAPI()

@app.get("/")
async def root():
	return { "message" : "Hello World" }

#path variable

@app.get("/items/{item_id}")
async def read_item(item_id:int):
	return { "message" : {item_id} }


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

#query string
## uri 정의시 path variable , 정의하지 않을시 query string
@app.get("/items2/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


@app.get("/items2/{item_id}")
async def read_item2(item_id: str, q: Optional[str] = None, short: bool = False):

    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

#
@app.get("/items3/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item

#body
@app.post("/items4/")
async def create_item(item: Item):
    return item

# ALL
@app.put("/items5/{item_id}")
async def create_item(item_id: int, item: Item, q: Optional[str] = None):
    result = {"item_id": item_id,  **item.dict()}
    if q:
        result.update({"q": q})
    return result

#query max size length, min size length , regex
@app.get("/items6/")

async def read_items(q: Optional[str] = Query(None,min_length=3, max_length=50, regex="^fixedquery$")):

    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

#default value
@app.get("/items7/")
async def read_items(q: str = Query("aaaa", min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

#List value
@app.get("/items8/")
async def read_items(q: Optional[List[str]] = Query(['foo','bar'])):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

#List other
@app.get("/items9/")
async def read_items(q: list = Query([])):
    query_items = {"q": q}
    return query_items
    
#description
@app.get("/items/")
async def read_items(
    q: Optional[str] = Query(
        None,
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

#query string alias
@app.get("/items10/")

async def read_items(q: Optional[str] = Query(None, alias="item-query")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

#Deprecated
@app.get("/items11/")
async def read_items(
    q: Optional[str] = Query(
        None,
        alias="item-query",
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
        max_length=50,
        regex="^fixedquery$",
        
        deprecated=True, 

    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results