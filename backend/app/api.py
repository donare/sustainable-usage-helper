from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import greyscale
from . import applications

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/", tags=["root"])
async def root() -> dict:
    return {"message": "Hello world!"}


@app.get("/set_greyscale_on")
async def set_greyscale_on() -> dict:
    greyscale.set_greyscale_on()
    return {"message": "Activated Greyscale Filter."}


@app.get("/set_greyscale_off")
async def set_greyscale_off() -> dict:
    greyscale.set_greyscale_off()
    return {"message": "Deactivated Greyscale Filter."}

@app.get("/running_processes")
async def get_running_processes() ->dict:
    return applications.get_process_list()

