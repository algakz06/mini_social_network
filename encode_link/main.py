from fastapi import FastAPI
from urllib.parse import quote
from pydantic import BaseModel


app = FastAPI()


class EncodeUrl(BaseModel):
    url: str


@app.post("/encode_url")
def encode_url(url_for_encode: EncodeUrl):
    encoded_url = quote(url_for_encode.url)
    return {"encoded_url": encoded_url}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=2323)
