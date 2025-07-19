#10 занятие
'''
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/users")
async def get_users():
    return [{"id" : 1, "name" : "Artem"}]

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0")

'''
#11 занятие
'''
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/users")
async def get_users():
    return [{"id" : 1, "name" : "Artem"}]

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0")
'''


#12 занятие
'''
from fastapi import Depends, FastAPI
from src.api import main_router


app = FastAPI()
app.include_router(main_router)


'''

#13 занятие

