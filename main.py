from fastapi import FastAPI

from src.routes import contacts


app = FastAPI(debug=True)

app.include_router(contacts.router, prefix='/api')


@app.get('/')
def read_root():
    return {'GoIT': 'Python web homework 11'}

