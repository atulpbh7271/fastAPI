from fastapi import FastAPI

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