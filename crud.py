from typing import Optional
from fastapi import FastAPI, HTTPException,status
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    #default value
    published : bool = True
    #optional 
    rating : Optional[int] = None


my_posts = [{"title":"title of posts 1","content":"content of posts 1","id" : 1},{"title":"favorite food","content":"i like pizza","id" : 2}]

#show all posts
@app.get("/posts")
def get_posts():
    return {"data": my_posts}

#create a post
@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    # dict() on a Pydantic model is deprecated in Pydantic v2
    #Pydantic v1	Pydantic v2
    #model.dict()	model.model_dump()
    #model.json()	model.model_dump_json()
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0,100)
    my_posts.append(post_dict)
    return {"data": my_posts}

#get by id 
@app.get("/posts/{id}")
def get_pots(id:int):
    # find the post with matching id
    post= next((p for p in my_posts if p["id"] == id ),None)
    if post is None:
        # return 404 if not found
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    return {"data": post}

#delete a posts
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    # Find the index of the post with matching id
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            my_posts.pop(i)
            return  # 204 No Content → nothing to return

    # If we reach here → post not found
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id {id} does not exist"
    )