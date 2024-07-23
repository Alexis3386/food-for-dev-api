from fastapi import FastAPI
from fastapi_pagination import add_pagination
import models
from database import engine

import recipes.router, users.router, ingredients.router, steps.router, auth.router


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router.router)
app.include_router(recipes.router.router)
app.include_router(users.router.router)
app.include_router(ingredients.router.router)
app.include_router(steps.router.router)

add_pagination(app)
