import pandas as pd
import os
import glob
global upload_path
global merge_path
upload_path='static/uploaded file/'
merge_path='static/merged file/'

def getCourseDetails(data):
    
    #course details
    course_title=data.columns[1]
    course_code=data[course_title][0]
    course_credit=data[course_title][1]
    
    #just taking class
    just_class_values=list(data.loc[2])[1:]
    
    #removing above course details
    attendance=data.loc[3:].copy()
    
    #taking only student id
    just_id_values=attendance['Course Title'].values
    
    #taking just attendace values
    just_attendance_values=attendance.loc[:, attendance.columns != 'Course Title'].values
    
    # Create data frame of id index, class column, attandance data
    index=just_id_values
    columns=just_class_values
    data_set =  just_attendance_values

    # Creates pandas DataFrame.
    dataframe = pd.DataFrame(data_set,index,columns)
    
    #reurn all these thing
    return {
        'Course_Title':course_title,
        'Course_Code':course_code,
        'Credit':course_credit,
        'Total_Class':len(dataframe.columns),
        'attendance_frame':dataframe
    }



def createSemester():
    _columns=['Cource_Title','Cource_Code','Credit','Total_Class']
    semester_dataframe=pd.DataFrame(columns=_columns)
    return semester_dataframe



def insertToSemester(details):     
    global new_semester
    # Creating the new row 
    data = [                
            {'Cource_Title': details['Course_Title'],
             'Cource_Code': details['Course_Code'],
             'Credit': details['Credit'],
             'Total_Class': details['Total_Class']
            }
           ]  
    new_row = pd.DataFrame(data)
    
    # for appending new_row at the end of semester_dataframe
    new_semester = new_semester.append(new_row, ignore_index = True) 




def mergeUploadedFile(all_uploaded_file):
    global new_semester
    new_semester=createSemester()
    for uploaded_file in all_uploaded_file:
        dataset=pd.read_excel(upload_path+uploaded_file)
        #getting course information and attendance sheet
        details=getCourseDetails(dataset)
        
        #saving the attendance sheet as csv file
        details['attendance_frame'].to_csv(merge_path+details['Course_Code']+".csv")
        
        #inserting course information new semester dataframe
        insertToSemester(details)
    return new_semester



def newStudentAttendance():
    columns=['Course Title','Course Code','Total Class','Present','Absent']

    new_student_attendace = pd.DataFrame(columns=columns)

    return new_student_attendace


def getAttendance(student_id):
    
    #reading new semester dataframe which is saved as csv file
    new_semester=pd.read_csv(merge_path+"new_semester.csv")
    
    #taking all course cose as list
    cource_code=list(new_semester['Cource_Code'])
    
    #create new attendance dataframe
    new_student_attendace=newStudentAttendance()

    for code in cource_code:
        
        #taking attendance dataframe of this coutce code
        cource_item_df=pd.read_csv(merge_path+code+".csv",index_col=0)

        #calculating total class, present, absent
        total_class=len(cource_item_df.columns)
        present=list(cource_item_df.loc[int(student_id)].values).count('P')  
        absent=total_class-present

        #taking course title and credit
        course_title=new_semester[new_semester.Cource_Code==code]['Cource_Title'].values[0]
        credit=new_semester[new_semester.Cource_Code==code]['Credit'].values[0]

        #creating new row of above data
        row_data = [              
                {'Course Title': course_title,'Course Code': code,'Credit':credit,'Total Class': total_class,'Present': present,'Absent':absent,'Present Percentage':int(present/total_class*100)}
               ]  
        new_row = pd.DataFrame(row_data)

        #appending in new_student_attendace
        new_student_attendace = new_student_attendace.append(new_row, ignore_index = True)
    
    return new_student_attendace



def clearPath(path):
    file_path = glob.glob(path+'*')
    if(len(file_path)):
        try:
            for f in file_path:
                os.remove(f)
            return True
        except:
            return False
    return True
    


def getExtension(name):
    return os.path.splitext(name)[1]


def isLoaded():
    path = './static/merged file/new_semester.csv'
    isExist = os.path.exists(path)
    
    if(isExist):
        return True
    else:
        return False