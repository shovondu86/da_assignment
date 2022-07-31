# Import flask dependencies
import os
from flask import Blueprint, request, g, session, redirect, url_for , abort, jsonify, g, url_for,make_response
from app import db
from app import app
from app.mod_da.models import  DataCases, DiseaseList
from werkzeug.utils import secure_filename
import csv
import re
from datetime import datetime
#Func for sum, avg 
from sqlalchemy import func
import json


# Define the blueprint: 'da' Data Analysis
mod_da = Blueprint('dataAnalysis', __name__, url_prefix='/')

#Index Route
@mod_da.route('/')
def index():

    return "Assignment for a Software Engineer position July 2022" 

#File Upload Allowed file types only csv
ALLOWED_EXTENSIONS = {'csv'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#In this cases each time table data will be deleted when upload the CSV and last one wil be stored in to databse 
def deleteData(table)->None:
    db.session.query(table).delete()
    db.session.commit()   

## Start Disease List Upload and Load in into database

#Disease list upload  
@mod_da.route("/diseaselistload", methods=['POST'])
def diseaselist_upload():
    if request.method == 'POST':
        # check if the post request has the file 
        if 'file' not in request.files:
           
            return 'No file part'

        file = request.files['file']
        if file.filename == '':
            
            return 'No file selected for uploading'
         #Only csv allowed    
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #File save into uploads folder
            filepathname=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepathname)
            
            fields=[]   
            # Open file and read disease List  
            with open(filepathname, 'r') as csvfile:
                # creating a csv reader object
                csvreader = csv.reader(csvfile)
                #Header 
                fields = next(csvreader)
                #print(fields)
                #Delete existing diseas list
                deleteData(DiseaseList)
                # extracting each data row one by one and insert into databse one by one 
                for row in csvreader:
                    diseaseList = DiseaseList(id = row[0],
                    name = row[1],     
                    )
                    db.session.add(diseaseList)   
                db.session.commit()
            #Return DiseaseList when sucessfully upload and load data into database
            return diseaseListJson()
        else:
            
            return 'Allowed file types only csv'  

# Disease List        
def diseaseListJson():
    # Disease List model Query throgu SQLAlchemy 
    diseaseList = DiseaseList.query.all()
    diseaseListarry = [i.as_dict() for i in diseaseList]
    
    return jsonify(diseaseListarry)

# Disease List in a route 
@mod_da.route('/diseaseListInfos')
def diseaseList():

    return diseaseListJson()    

## End Disease List Upload and Load in into database

## Start data cases upload and data analysis

#Funtion for cleaning corrupted data
def cleanCorruptedRow(row):
    #Convert to comma separated string
    s = ",".join(row)
    #Find out corrupted string
    corruptedS=re.search(r'[^-][A-Z]\w+,',s)
    corruptedS=corruptedS.group()
    #Remove corrupted string from the row 
    cleanRow = s.replace(corruptedS,'')
    #Convert comma separated string to list object
    cleanRow = cleanRow.split(",")
    return cleanRow

#Funtion for cases data insert in to database
def casesdataintoDb(row)-> None:
    #print(row[0])
    dataCases = DataCases(uuid = row[0],
                    datetime = datetime.fromisoformat(row[1]),
                    species = row[2],
                    number_morbidity = row[3],
                    disease_id = row[4],
                    number_mortality = row[5],
                    total_number_cases = row[6],
                    location=row[7]
                    )
    db.session.add(dataCases)   
    db.session.commit()

@mod_da.route("/datacasesload", methods=['POST']) 
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:

            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            
            return 'No file selected for uploading'
            #File save into uploads folder
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filenamewithPath=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filenamewithPath)

            #csv file  Read
            # initializing the titles  list
            fields = []
            # Open the cases file to read 
            with open(filenamewithPath, 'r') as csvfile:
                # creating a csv reader object
                csvreader = csv.reader(csvfile)
                # extracting field names through first row
                fields = next(csvreader)
                #print(len(fields))
                #Delete Existing data before inserting new data
                deleteData(DataCases)
                # extracting each cases data row one by one insert in to databse 
                for row in csvreader:
                    if len(fields)==len(row):
                        #print(len(row))
                        casesdataintoDb(row)
                    else:
                        #len(fields)!=len(row):
                        #if corrupted then clean it
                        row=cleanCorruptedRow(row)
                        casesdataintoDb(row)
                        #print(len(row))

            #return 'file successfully uploaded' 
            return getIndicator()
        else:
            
            return 'Allowed file types only csv'

# Data analysis
def getIndicator():
    #Initializing Indicator dictionary
    indic = {}
    #Total number of deaths reported at each location
    deathReportLoc=db.session.query(DataCases.location, func.sum(DataCases.number_mortality)).group_by(DataCases.location).all()

    #Total number of reported cases 
    totalCases=db.session.query(0,func.sum(DataCases.total_number_cases)).all()
    
    #Total number of reported cases update into Indicator
    #Convert to dictionary
    totalCasesDic=dict(totalCases)
    totalCasesDic["total number of reported cases is"] = totalCasesDic.pop(0)
    indic.update(totalCasesDic)
    
    #Total number of deaths reported at each location insert into Indicator
    #Convert to dictionary
    deathReportLocDic=dict(deathReportLoc)
    indic["total number of deaths reported at each location"] = deathReportLocDic
    
    #Indicator Json 
    indicJson= json.dumps(indic, indent=4)

    return indicJson

@mod_da.route('/getIndicatorInfos')
def indicator():
    

    return getIndicator()

   
@mod_da.route('/getAdvIndicatorInfos')
def getAdvIndicator():
    #species from parameter 
    speciesV = request.args.get('species')
    # Default species
    if not speciesV:
        speciesV='cat'

    #Initializing advanced indicator dictionary 
    advIndic = {}

    #Total number of deaths from each disease
    deathDis=db.session.query(DiseaseList.name, func.sum(DataCases.number_mortality)).filter(DataCases.disease_id == DiseaseList.id).group_by(DataCases.disease_id).order_by(DiseaseList.name).all()
    #Average number of sick species reported in reports from villages up to two decimal points
    avgcatV=db.session.query(0,func.round(func.avg(DataCases.number_morbidity),2)).filter(DataCases.species==speciesV).filter(DataCases.location.ilike('%Village%')).all()
    
    #Average number of sick species report to advanced indicator dictionary
    #Convert to dictionary
    avgcatVD=dict(avgcatV)
    avgcatVD["Average number of sick "+speciesV+ " reported in reports from villages up to two decimal points"] = avgcatVD.pop(0)
    advIndic.update(avgcatVD)
    
    #Total number of deaths from each disease insert into advanced indicator dictionary
    #Convert to dictionary
    deathDisD=dict(deathDis)
    advIndic["total number of deaths from each disease"] = deathDisD
  
    #Indicator Json 
    advIndicJson= json.dumps(advIndic, indent=4)
    
    return advIndicJson

## End data cases upload and data analysis
