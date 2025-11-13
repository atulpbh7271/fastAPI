from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

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
