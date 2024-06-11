from fastapi import FastAPI

from src.routes import contacts, auth


app = FastAPI(debug=True)

app.include_router(contacts.router, prefix='/api')
app.include_router(auth.app, prefix='/api')


@app.get('/')
def read_root():
    return {'GoIT': 'Python web homework 12'}

