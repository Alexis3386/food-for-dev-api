from fastapi import FastAPI
from fastapi_pagination import add_pagination

import auth.router
import category.router
import ingredients.router
import models
import recipes.router
import steps.router
import users.router
from database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router.router)
app.include_router(recipes.router.router)
app.include_router(users.router.router)
app.include_router(ingredients.router.router)
app.include_router(steps.router.router)
app.include_router(category.router.router)


add_pagination(app)
