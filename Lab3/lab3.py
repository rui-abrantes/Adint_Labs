from email import message
from fileinput import filename
from multiprocessing import context
import string
from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import os
import json
from werkzeug.utils import secure_filename
import shutil
import requests

#################################################################################
######################## DATABASE ###############################################
#################################################################################

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

import datetime
from datetime import date
from sqlalchemy.orm import sessionmaker
from os import path

DATABASE_FILE = "downloadedFiles.sqlite"
db_exists = False
if path.exists(DATABASE_FILE):
    db_exists = True
    print("\t database already exists")

engine = create_engine('sqlite:///%s'%(DATABASE_FILE), echo=False) #echo = True shows all SQL calls

Base = declarative_base()

class File(Base):
    __tablename__ = 'file'
    id = Column(Integer, primary_key=True)
    name=Column(String)
    ip = Column(String)
    date = Column(Date) # A type for datetime.date() objects.

def newFile(name, ip, date):
    file = File(name = name, date = datetime.date(date.year, date.month, date.day), ip = ip)
    session.add(file)
    session.commit()

def countAllFiles():
    return session.query(File).count()



Base.metadata.create_all(engine) #Create tables for the data models

Session = sessionmaker(bind=engine)
session = Session()

#################################################################################
######################## SITE ###################################################
#################################################################################

app = Flask(__name__)
     
@app.route("/")
def index():
    return render_template("index.html", message="Dynamic content!")   

@app.route("/listFiles")
def listFiles():
    
    listOfFiles = os.listdir(path = './files')
    numberOfDownloads = countAllFiles()
    print(numberOfDownloads)
    listOfFiles.append(numberOfDownloads)
    return listOfFiles

@app.route('/getFile/<path:filename>', methods=['GET', 'POST'])
def getFile(filename):
    if filename not in os.listdir(path = './files'):   
        return redirect(url_for('file_not_found', fileName=filename))

    newFile(filename, "127.0.0", date.today() )
    return send_from_directory(directory="./files/",
                               path=filename, as_attachment=True)


@app.route('/file_not_found/<fileName>')
def file_not_found(fileName):
    return render_template("fileNotFound.html", message=fileName)


@app.route("/files")
def files():
    listOfFiles = os.listdir(path = './files')
    return render_template("files.html", jsonfile=json.dumps(listOfFiles)) 



@app.route("/newFile")
def newFileForm():
    return render_template("newFile.html") 

@app.route("/createFile")
def createFile():
    return render_template("createFile.html") 

@app.route("/createFile/success", methods=['POST', 'GET'])
def createFileSucess():
    if request.method == 'POST':
        fileName=""
        context=""
        result = request.form
        print(result)
        for key, value in result.items():
            if key == 'fileName':
                fileName = value
            if key == 'context':
                context = value
            
        if fileName == "":
            return render_template("index.html", message="Error you cannot create file without name!") 
        
        #create file
        filepath = os.getcwd()
        filepath = os.path.join( filepath + "/files",fileName + ".txt")
        
        f = open( filepath, "x")
        f.write(context)
        f.close()

        return render_template("createFileSuccess.html", result = result)


@app.route('/uploadFiles')
def uploadFile():
   return render_template('uploadFiles.html')

@app.route('/uploadFiles/success', methods = ['GET', 'POST'])
def uploadFileSuccess():
    if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      shutil.move(os.getcwd()+"/" + secure_filename(f.filename), os.getcwd()+"/files/" + f.filename )
      return 'file has been uploaded successfully'

@app.route("/downloadAll")
def downloadAll():
    r = requests.get("http://127.0.0.1:8000/listFiles")
    print(r.status_code)
    data = r.json()
    for file in data:
        new_r = requests.get("http://127.0.0.1:8000/getFile/" + file)
        filepath = os.getcwd()
        filepath = os.path.join( filepath + "/downloads",file)
        open(filepath, 'wb').write(r.content)
        print(new_r.status_code)
    return "ALL WORKED"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)