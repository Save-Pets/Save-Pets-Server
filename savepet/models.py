from savepet import db


#regname,regphone,regemail
#petname,petbreed,petbirth,petgender,petprofile,reg_id,uniquenumber

class Registrant(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    regName=db.Column(db.String(200),nullable=False)
    regPhone=db.Column(db.String(200),nullable=False)
    regEmail=db.Column(db.String(200),nullable=False)

class Pet(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    petName=db.Column(db.String(200),nullable=False)
    petBreed=db.Column(db.String(200),nullable=False)
    petBirth=db.Column(db.String(200),nullable=False)
    petProfile=db.Column(db.String(400),nullable=False)
    regId=db.Column(db.Integer,db.ForeignKey('registrant.id',ondelete='CASCADE'))
    registrant=db.relationship('Registrant',backref=db.backref('pet_set'))
    uniqNum=db.Column(db.String(200),nullable=False)