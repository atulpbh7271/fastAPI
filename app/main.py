# main.py
from typing import Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from itertools import count

app = FastAPI(title="Simple Posts API (CRUD)")

# ---------- Models ----------
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

# Output model (includes id)
class PostOut(Post):
    id: int

# Model for partial updates (all fields optional)
class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None
    rating: Optional[int] = None

#In-memory "DB" 
my_posts: list[dict] = [
    {"title": "title of posts 1", "content": "content of posts 1", "id": 1},
    {"title": "favorite food", "content": "i like pizza", "id": 2},
]

# simple incremental id generator (starts at 3 because 1 and 2 exist)
id_counter = count(start=3)


# Helpers
def find_post_index(post_id: int) -> Optional[int]:
    for i, p in enumerate(my_posts):
        if p["id"] == post_id:
            return i
    return None


#CRUD Endpoints 

# CREATE
@app.post("/posts", response_model=PostOut, status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.model_dump()            # Pydantic v2
    post_dict["id"] = next(id_counter)
    my_posts.append(post_dict)
    return post_dict


# READ ALL
@app.get("/posts", response_model=list[PostOut])
def get_posts():
    return my_posts


# READ by ID
@app.get("/posts/{id}", response_model=PostOut)
def get_post(id: int):
    idx = find_post_index(id)
    if idx is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    return my_posts[idx]


# UPDATE (PUT) - full replace (client must send all required fields)
@app.put("/posts/{id}", response_model=PostOut)
def update_post_put(id: int, post: Post):
    idx = find_post_index(id)
    if idx is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    updated = post.model_dump()
    updated["id"] = id  # preserve id
    my_posts[idx] = updated
    return updated


# PATCH - partial update (only provided fields are changed)
@app.patch("/posts/{id}", response_model=PostOut)
def update_post_patch(id: int, post_update: PostUpdate):
    idx = find_post_index(id)
    if idx is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    existing = my_posts[idx]
    update_data = post_update.model_dump()
    for key, value in update_data.items():
        # update only non-None values (allows setting e.g. published=False)
        if value is not None:
            existing[key] = value
    my_posts[idx] = existing
    return existing


# DELETE
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    idx = find_post_index(id)
    if idx is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist")
    my_posts.pop(idx)
    return  # 204 No Content — nothing returned








# from typing import Optional
# from fastapi import FastAPI
# from fastapi.params import Body
# from pydantic import BaseModel

# app = FastAPI()

# #validation on data
# # title as string and content as also string
# class Post(BaseModel):
#     title : str
#     content : str
#     #default value
#     published : bool = True
#     #optional 
#     rating : Optional[int] = None


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


# @app.get("/posts")
# def get_posts():
#     return {"message":"This is your posts"}

# @app.post("/createposts")
# def create_posts():
#     return {"message":"Successfully created the posts"}

# @app.post("/createNewposts")
# def create_posts(payload: dict = Body(...)):
#     print(payload)
#     return {"new_post": f"title : {payload['title']} content : {payload['content']}"}


# @app.post("/createPostsWithVali")
# def create_posts(posts : Post):
#     print(posts)
#     print(posts.dict())
#     print(posts.title)
#     print(posts.content)
#     print(posts.published)
#     print(posts.rating)
#     return {"Data ":posts}