from flask import Flask, render_template,flash,redirect, url_for
import os
import glob
from flask import send_file
from fileinput import filename
from flask import request

import myModule
 
app = Flask(__name__)
app.secret_key = "super secret key"
upload_path='static/uploaded file/'
merge_folder='static/merged file/' 
 
# @app.route("/")
# def index():
#     return render_template("layout.html")

    
@app.route("/")
def home():
    return render_template("home.html")
    


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
        extension=['.xlsx']


        for file in files:
            file_name=file.filename   #name
            
            if file_name != '':
                file_extension = myModule.getExtension(file_name)

                if file_extension not in extension:
                    flash('Invalid Extension','bg-danger')
                    return redirect(url_for('home'))
                else:
                    try:
                        file.save(upload_path+file.filename) #uploaded
                        uploaded_file_names.append(file_name)
                    except:
                        flash('Error in file uploading')
                        return redirect(url_for('home'))
            else:
                flash('Invalid File','bg-danger')
                return redirect(url_for('home'))
        
        if(len(uploaded_file_names)):
            new_semester=myModule.mergeUploadedFile(uploaded_file_names)
            new_semester.to_csv(merge_folder+"new_semester.csv",index=False)
            flash('System Loaded Successfully','bg-success')
            return redirect(url_for('loaded_file'))



@app.route("/loaded-file")
def loaded_file():
    file_path = glob.glob(upload_path+'*')
    file_names=[]
    try:
        for f in file_path:
            file_names.append(f)
        return render_template("loaded_file.html",files=file_names)
    except:
        return render_template("loaded_file.html")


@app.route("/get-attendance")
def get_attendance():
    return render_template("find_attendance.html")

@app.route("/find-attendance",methods=['POST'])
def find_attendance():
    if request.method == 'POST':
        res=myModule.isLoaded()
        if(res!=True):
            flash('System not Loaded','bg-danger')
            return redirect(url_for('home'))

        student_id = request.form['student_id']
        attendance=myModule.getAttendance(student_id)
        attendance=attendance.to_dict('records')
        # return attendance
    return render_template("find_attendance.html",attendance=attendance,student_id=student_id)

@app.route('/demo-download')
def demo_download():
    return send_file(
        'static/demo/demo.xlsx',
        mimetype='text/xlsx',
        download_name='demo.xlsx',
        as_attachment=True
    )
@app.route('/reset-system')
def reset_system():
    res=myModule.clearPath(upload_path)   
    if(res!=True):
        return "Error in clearing uploaded file path" 
    res=myModule.clearPath(merge_folder)    
    if(res!=True):
        return "Error in clearing uploaded file path" 
    flash('System Reseted Successfully','bg-success')
    return redirect(url_for('loaded_file'))




 


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404


if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0')