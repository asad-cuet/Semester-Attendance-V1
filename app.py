from flask import Flask, render_template
import os
import glob
from flask import send_file
from fileinput import filename
from flask import request

import myModule
 
app = Flask(__name__)
 
 
# @app.route("/")
# def index():
#     return render_template("layout.html")

    
@app.route("/")
def home():
    return render_template("home.html")


@app.route('/demo-download',methods=['GET'])
def demo_download():
    return send_file(
        'static/demo/demo.xlsx',
        mimetype='text/xlsx',
        download_name='demo.xlsx',
        as_attachment=True
    )

extension=['.xlsx']
upload_path='static/uploaded file/'
merge_folder='static/merged file/'
@app.route('/load-file',methods=['POST'])
def load_file():
    if request.method == 'POST':
        res=myModule.clearPath(upload_path)   
        if(res!=True):
            return "Error in clearing uploaded file path" 
        res=myModule.clearPath(merge_folder)    
        if(res!=True):
            return "Error in clearing uploaded file path" 

        files = request.files.getlist('file[]')
        uploaded_file_names=[]



        for file in files:
            file_name=file.filename   #name
            
            if file_name != '':
                file_extension = myModule.getExtension(file_name)

                if file_extension not in extension:
                    return "Invalid Extension"
                else:
                    try:
                        file.save(upload_path+file.filename) #uploaded
                        uploaded_file_names.append(file_name)
                    except:
                        return "Error in file uploading"
            else:
                return "Invalid file"
        
        if(len(uploaded_file_names)):
            new_semester=myModule.mergeUploadedFile(uploaded_file_names)
            new_semester.to_csv(merge_folder+"new_semester.csv",index=False)
            return new_semester.to_html()

 


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404


if __name__ == "__main__":
    app.run()