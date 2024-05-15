from fastapi import FastAPI

app = FastAPI()


@app.get("/home")
async def delete_customer_by_id():
    return "Hello"