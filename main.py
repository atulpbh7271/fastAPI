from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

#validation on data
# title as string and content as also string
class Post(BaseModel):
    title : str
    content : str

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
def create_posts(new_posts : Post):
    print(new_posts)
    return {"Data ":"new posts"}