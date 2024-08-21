from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Database setup
conn = sqlite3.connect('job_applications.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS applications
                  (id INTEGER PRIMARY KEY, title TEXT, company TEXT, status TEXT)''')
conn.commit()


class Application(BaseModel):
    title: str
    company: str
    status: str


@app.post("/applications/")
def create_application(application: Application):
    cursor.execute("INSERT INTO applications (title, company, status) VALUES (?, ?, ?)",
                   (application.title, application.company, application.status))
    conn.commit()
    return application


@app.get("/applications/", response_model=List[Application])
def read_applications():
    cursor.execute("SELECT title, company, status FROM applications")
    applications = cursor.fetchall()
    return [Application(title=app[0], company=app[1], status=app[2]) for app in applications]


@app.delete("/applications/", response_model=List[Application])
def clear_applications():
    cursor.execute("DELETE FROM applications")
    conn.commit()
    return {"message": "All applications have been cleared."}
