from fastapi import FastAPI
from mydns import router as dns_router

app = FastAPI()
app.include_router(dns_router)

@app.get("/")
def root():
    return {"형식": "measure?domain=ticket.melon.com&count=5"}
