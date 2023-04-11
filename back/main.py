from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from supabase import create_client, Client
from qa import answer
import uvicorn
import os

app = FastAPI()
limiter = Limiter(key_func=get_remote_address, default_limits=["5/minute"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# connect to supabase
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase_client = create_client(url, key)

SUPABASE_TABLE_NAME = "qa_log"


@app.get("/")
async def root():
    return {"code": 200, "msg": "I am alive"}


@app.get("/qa")
async def qa(req: Request):
    try:
        q = req.query_params["q"]
        a = answer(q)
        supabase_client.table(SUPABASE_TABLE_NAME).insert({
            "question": q,
            "answer": a,
            "success": True,
        }).execute()
        return {
            "code": 200,
            "answer": a,
        }
    except Exception as err:
        try:
            print(err)
            supabase_client.table(SUPABASE_TABLE_NAME).insert({
                "question": q,
                "answer": "",
                "success": False,

            }).execute()
        finally:
            return {
                "code": 500,
                "answer": "Failed to process the question"
            }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0",  port=8989, log_level="info")
