from email import message
from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import os
import json
app = Flask(__name__)
     
@app.route("/")
def index():
    return render_template("index.html", message="Dynamic content!")   

@app.route("/listFiles")
def listFiles():
    #get dir listing
    listOfFiles = os.listdir(path = './files')
    return render_template("listFiles.html", message = listOfFiles) 

@app.route('/getFile/<path:filename>', methods=['GET', 'POST'])
def getFile(filename):
    #TODO 3
    # file verification
    if filename not in os.listdir(path = './files'):   
        return redirect(url_for('file_not_found'), 400, filename)


    #TODO 5
    # send file
    return send_from_directory(app.config['./files/'],
                               filename, as_attachment=True)

# TODO 4
# redirected page
@app.route('/file_not_found')
def file_not_found(fileName):
    return render_template("fileNotFound.html", message=fileName)


# TODO 6
#/files
@app.route("/files")
def files():
    listOfFiles = os.listdir(path = './files')
    return render_template("files.html", jsonfile=json.dumps(listOfFiles)) 



@app.route("/newFile")
def newFileForm():
    return render_template("newFile.html") 

#TODO 7
#createFile

#TODO 8
#upload files

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)