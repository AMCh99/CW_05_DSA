from typing import Annotated
import shutil
from fastapi import FastAPI, File, UploadFile

from CW_05_DSA import podpisz_plik

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    file_location = f"./uploaded_files/{file.filename}"
    
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    
    L,p,q,g,x,y,file_path,signature,is_valid = podpisz_plik(file_location)
    
    return {"filename": file.filename, "location": file_location, "signature":signature,"is_valid":is_valid,"L":L, "p":p,"q":q,"g":g,"x":x,"y":y,"file_path":file_path}