from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

#validation on data
# title as string and content as also string
class Post(BaseModel):
    title : str
    content : str
    #default value
    published : bool = True
    #optional 
    rating : Optional[int] = None


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"message":"This is your posts"}

@app.post("/createposts")
def create_posts():
    return {"message":"Successfully created the posts"}

@app.post("/createNewposts")
def create_posts(payload: dict = Body(...)):
    print(payload)
    return {"new_post": f"title : {payload['title']} content : {payload['content']}"}


@app.post("/createPostsWithVali")
def create_posts(posts : Post):
    print(posts)
    print(posts.dict())
    print(posts.title)
    print(posts.content)
    print(posts.published)
    print(posts.rating)
    return {"Data ":posts}