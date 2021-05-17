import datetime
import os
import random

import pymysql
import json
import shutil
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

#db
def db_connector():
    connector = pymysql.connect(host='localhost',
                                  user='root',
                                  password='anstnfla25',
                                  db='savepet',
                                  charset='utf8')
    return connector


#중복없이 reg_num 생성
alist=[]

# [등록 API]
# 이미지,정보 -> 이미지 서버에 저장 후 return 파싱된 정보, 등록번호
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        files= request.files
        global details
        details= request.form
        profile = request.files['profile']
        # imgs = files.to_dict(flat=False)['filename[]']
    reg_num = uniquenumber()

    print(os.getcwd())

    os.chdir('./ML/Save-Pets-ML/SVM-Classifier/image/')
    createFolder('./%s' %(reg_num))

    #이미지 5장, key = filename[] 저장 for preprocess
    for index,f in enumerate (files.to_dict(flat=False)['filename[]']):
        f.save('./%s/' % (reg_num) + str(index)+'.jpg')

    #preprocess
    os.chdir('../')
    os.system('python preprocess.py --dir %s' %(reg_num))
    # print(os.getcwd())

    #5장 중에 첫번째 장 사진 복사 -> 조회
    source ='./image/%s/0.jpg' %(reg_num)
    destination = './Dog-Data/test/%s.jpg' %(reg_num)
    shutil.copyfile(source, destination)

    # print(os.getcwd())

    # 등록된 강아지인지 조회
    os.system('python Classifier.py --test %s.jpg' %(reg_num))

    db = db_connector()
    cursor = db.cursor()

    #연락처 중복일 때 (기존 등록된 유저 일때)
    phone = request.form['연락처']
    phone_confirm = "SELECT 1 FROM registerant WHERE regphone = '%s' " % (phone)
    cursor.execute(phone_confirm)
    data = cursor.fetchall()

    if data:
        pk = "select id from registerant WHERE regphone = '%s'" %(phone)
        cursor.execute(pk)
        pk1 = cursor.fetchone()

        # 등록번호 생성
        reg_num = uniquenumber()

        pet_sql = "INSERT INTO pet (petname,petbreed,petbirth,petgender,petprofile,reg_id,uniquenumber) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        val1 = (details['반려견'], details['품종'], details['태어난해'], details['성별'], profile, pk1,reg_num)

        cursor.execute(pet_sql, val1)

        db.commit()
        cursor.close()


        return jsonify({'data': [{'반려견': details['반려견'], '등록번호': reg_num}], 'message': 'success'})

    #새로운 유저
    else:
        reg_sql = "INSERT INTO registerant (regname,regphone,regemail) VALUES(%s,%s,%s)"
        val = (details['반려인'], details['연락처'], details['이메일'])

        cursor.execute(reg_sql, val)
        pk = "select id from registerant WHERE regphone='%s'" %(phone)
        cursor.execute(pk)
        rows = cursor.fetchone()
        # 등록번호 생성
        reg_num = uniquenumber()
        pet_sql = "INSERT INTO pet (petname,petbreed,petbirth,petgender,petprofile,reg_id,uniquenumber) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        val1 = (details['반려견'], details['품종'], details['태어난해'], details['성별'], profile, rows,reg_num)

        cursor.execute(pet_sql, val1)

        db.commit()

        cursor.close()

        return jsonify({'data': [{'반려견': details['반려견'], '등록번호': reg_num}], 'message': 'success'})


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)

def uniquenumber():
    date_time = datetime.datetime.now()
    for i in range(1):
        a = random.randint(1, 100)
        while a in alist:
            a = random.randint(1, 100)
    alist.append(a)
    unique = details['반려견'][0] + str(details['연락처'][7:11])
    print(unique)
    reg_num = (str(date_time.year) + str(date_time.month) + str(date_time.day) + str(a)+unique)
    return reg_num



# [조회 API]
@app.route('/lookup', methods=['GET', 'POST'])
def lookup():
    if request.method == 'POST':
        files = request.files['img']
        print(os.getcwd())
        files.save('./ML/Save-Pets-ML/SVM-Classifier/Dog-Data/test/'+files.filename)
        os.chdir('./ML/Save-Pets-ML/SVM-Classifier/')
        print(os.getcwd())
        os.system('python Classifier.py --test %s' % (files.filename))


    return jsonify({'message':'success'})

#error handler
@app.errorhandler(400)
def badRequest(error):
    return jsonify({'message':'fail'})

if __name__ == "__main__":
    app.run(debug=True)
