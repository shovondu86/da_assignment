#author= "Mohiuddin Shovon"
#date = "30 th July,2022"
#email = "shovon.du86@gmail.com"

from app import db
#Disease List model
class DiseaseList(db.Model):
    __tablename__ = 'disease_list'
    id = db.Column(db.Integer, primary_key = True)
    name= db.Column(db.String(32))

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}  
#Data Cases model
class DataCases(db.Model):
    __tablename__ = 'data_cases'
    uuid = db.Column(db.String(36), primary_key = True)
    datetime = db.Column(db.DateTime)
    species = db.Column(db.String(32))
    number_morbidity = db.Column(db.Integer)
    #disease_id = db.Column(db.Integer,db.ForeignKey('DiseaseList.id'))
    disease_id = db.Column(db.Integer)
    number_mortality = db.Column(db.Integer)
    total_number_cases = db.Column(db.Integer)
    location= db.Column(db.String(32))
    
   

