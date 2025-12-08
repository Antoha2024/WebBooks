from fastapi import FastAPI, Request
from typing import Dict
import subprocess

app = FastAPI()

@app.post("/execute/")
async def execute_python_code(request: Request):
    body = await request.body()
    code = body.decode("utf-8")

    try:
        result = subprocess.check_output(["python", "-c", code], stderr=subprocess.STDOUT, timeout=30)
        return {"output": result.decode("iso-8859-1")}  # Меняем utf-8 на iso-8859-1
    except subprocess.CalledProcessError as err:
        return {"error": err.output.decode("iso-8859-1")}
    except UnicodeDecodeError as ude:
        return {"error": str(ude)}