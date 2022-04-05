from fastapi.responses import HTMLResponse
from fastapi import FastAPI, File
from pydantic import BaseModel
from typing import List
from pymongo import MongoClient
import src.flowers_db as fldb
import os
from urllib.parse import quote_plus

from src.model import Model

app = FastAPI()
model = Model()
mongo_client = None


def get_client():
    """
    Setup a mongo client for the site
    :return:
    """
    global mongo_client
    if bool(mongo_client):
        return mongo_client
    host = os.getenv('MONGODB_HOST', '')
    username = os.getenv('MONGODB_USER', '')
    password = os.getenv('MONGODB_PASSWORD', '')
    port = int(os.getenv('MONGODB_PORT', 27017))
    endpoint = 'mongodb://{0}:{1}@{2}'.format(quote_plus(username),
                                              quote_plus(password), host)
    mongo_client = MongoClient(endpoint, port)
    return mongo_client


class ComicIssue(BaseModel):
    number: str
    series_name: str
    on_sale_date: str
    price: str
    publisher_name: str


@app.get("/")
async def main():
    get_client()
    content = """
<body>
<form action="/file/" enctype="multipart/form-data" method="post">
<input name="file" type="file">
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)


@app.get('/comics/{title}/{issue_number}', response_model=List[ComicIssue])
async def get_comic_issues(title: str, issue_number: str): 
    criteria = {'series_name': title, 'number': issue_number}
    client = get_client()
    db = client.farmdemo
    issues = db.issues.find(criteria)
    data = list()
    for issue in issues:
        data.append(ComicIssue(**issue))
    return data

@app.post("/file/")
async def create_file(file: bytes = File(...)):
    group_num, group_prob = model.make_predict(file)
    answer = fldb.get_img_class(group_num, group_prob, conn=mongo_client, num_img_out=model.config['amount_image_in_answer'])
    content = """
    <body>
    <form action="/" method="get">
    <h9>
    """ + str(answer) + """
    </h9>
    <input type="submit">
    </form>
    </body>
        """
    return HTMLResponse(content=content)

