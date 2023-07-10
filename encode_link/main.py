from fastapi import FastAPI
from urllib.parse import quote

app = FastAPI()


@app.get("/encode_url/{url}")
def encode_url(url: str):
    encoded_url = quote(url)
    return {"encoded_url": encoded_url}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
