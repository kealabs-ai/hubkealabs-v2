from fastapi import FastAPI

app = FastAPI(title="HubKealex v2", version="2.0.0")


@app.get("/v2/lex/health")
def health():
    return {"status": "ok", "service": "hubkealex-v2"}


@app.get("/v2/lex/test")
def test():
    return {"message": "Endpoint de teste funcionando", "version": "v2"}
