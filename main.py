import datetime
import os
import random
import subprocess
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
    global reg_num
    reg_num= uniquenumber()

    # print(os.getcwd())

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
    # os.system('python Classifier.py --test %s.jpg' %(reg_num))

    result = getSVMResultForRegister()
    print(result.decode('utf-8').split(','))
    compare = result.decode('utf-8').split(',')

    # compare = result.decode('utf-8')
    # print(compare[1])
    # print(result)

    ##등록된 강아지 예외처리
    # if compare[1] == '등록된강아지':
    #     return jsonify({'message':'이미 등록된 강아지입니다.'})

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


        # 가장 최근 insert id 불러오기
        reg_send = "SELECT last_insert_id();"
        cursor.execute(reg_send)
        latestid = cursor.fetchone()

        # db등록 정보 가져오기
        fetchDB = "SELECT * FROM pet WHERE id ='%s'" % (latestid[0])
        cursor.execute(fetchDB)
        all = cursor.fetchall()
        # print(all)
        petname = all[0][1]
        petbirth = all[0][3]
        petgender = all[0][4]
        petprofile = all[0][5]
        petnumber = all[0][7]

        db.commit()

        cursor.close()

        return jsonify({'data': [{'반려견': petname, '등록번호': petnumber,
                                  '반려견태어난해': petbirth, '반려견성별': petgender, '프로필이미지': petprofile}],
                        'message': 'success'})

    #새로운 유저
    else:
        #registerant table에 insert
        reg_sql = "INSERT INTO registerant (regname,regphone,regemail) VALUES(%s,%s,%s)"
        val = (details['반려인'], details['연락처'], details['이메일'])

        cursor.execute(reg_sql, val)

        #primarykey
        pk = "select id from registerant WHERE regphone='%s'" %(phone)
        cursor.execute(pk)
        rows = cursor.fetchone()

        # 등록번호 생성
        reg_num = uniquenumber()

        #pet table에 insert
        pet_sql = "INSERT INTO pet (petname,petbreed,petbirth,petgender,petprofile,reg_id,uniquenumber) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        val1 = (details['반려견'], details['품종'], details['태어난해'], details['성별'], profile, rows,reg_num)

        cursor.execute(pet_sql, val1)

        #가장 최근 insert id 불러오기
        new_reg_send="SELECT last_insert_id();"
        cursor.execute(new_reg_send)
        new_latestid = cursor.fetchone()

        #db등록 정보 가져오기
        new_fetchDB="SELECT * FROM pet WHERE id ='%s'" %(new_latestid[0])
        cursor.execute(new_fetchDB)
        new_all = cursor.fetchall()
        # print(new_all)
        new_petname = all[0][1]
        new_petbirth= all[0][3]
        new_petgender=all[0][4]
        new_petprofile=all[0][5]
        new_petnumber=all[0][7]

        db.commit()

        cursor.close()

        return jsonify({'data': [{'반려견': new_petname, '등록번호': new_petnumber,
                                  '반려견태어난해':new_petbirth,'반려견성별':new_petgender,'프로필이미지':new_petprofile}], 'message': 'success'})


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
    # print(unique)
    reg_num = (str(date_time.year) + str(date_time.month) + str(date_time.day) + str(a)+unique)
    return reg_num



# [조회 API]
@app.route('/lookup', methods=['GET', 'POST'])
def lookup():
    if request.method == 'POST':
        global lookupimg
        lookupimg= request.files['img']
        # print(os.getcwd())
        lookupimg.save('./ML/Save-Pets-ML/SVM-Classifier/Dog-Data/test/'+lookupimg.filename)
        os.chdir('./ML/Save-Pets-ML/SVM-Classifier/')
        # print(os.getcwd())

        # os.system('python Classifier.py --test %s' % (lookupimg.filename))

        result= getSVMResult()
        SVMresult = result.decode('utf-8').split(',')

        # print(SVMresult[0])

        db = db_connector()
        cursor = db.cursor()

        if SVMresult[1] =='미등록강아지':
            return jsonify({'data':'조회된 비문이 없습니다','message':'success'})
        else :
            foundDog=SVMresult[0]
            accurancy=SVMresult[2]
            lookup_sql = "SELECT reg_id FROM pet WHERE uniquenumber='%s'" %(foundDog)
            cursor.execute(lookup_sql)
            rows = cursor.fetchone()
            # print(rows)
            registerData_sql="SELECT * FROM registerant WHERE id='%s'" %(rows)
            cursor.execute(registerData_sql)

            datas = cursor.fetchall()
            # print(datas)
            registername=datas[0][1]
            registerphone=datas[0][2]
            registeremail=datas[0][3]

            # for index,data in datas:
            #     if index == 1:
            #         registername=data
            #     elif index==2:
            #         registerphone=data
            #     else:
            #         registeremail=data
            db.commit()

            return jsonify({'data':[{'등록번호':foundDog,'등록자이름':registername,'등록자연락처':registerphone,'등록자이메일':registeremail,'일치율':accurancy}],
            'message':'success'})

    # return jsonify({'message':'success'})

def getSVMResult():
    cmd =['python','Classifier.py','--test','%s' %(lookupimg.filename)]
    fd_popen = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
    data = fd_popen.read().strip()
    fd_popen.close()
    return data

def getSVMResultForRegister():
    cmd =['python','Classifier.py','--test','%s.jpg' %(reg_num)]
    fd_popen = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
    data = fd_popen.read().strip()
    fd_popen.close()
    return data



#error handler
@app.errorhandler(400)
def badRequest(error):
    return jsonify({'message':'fail'})

if __name__ == "__main__":
    app.run(debug=True)
