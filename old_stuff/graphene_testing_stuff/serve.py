import trio_asyncio
import uvicorn

from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp

from .schema import schema

app = FastAPI()

app.add_route("/", GraphQLApp(schema=schema))

if __name__ == "__main__":
    config = uvicorn.Config(app=app)
    server = uvicorn.Server(config=config)
    trio_asyncio.run(trio_asyncio.aio_as_trio(server.serve))

