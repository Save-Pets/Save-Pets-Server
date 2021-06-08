#ORM적용하기 위한 설정파일
import os
BASE_DIR=os.path.dirname(__file__)
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR,'savepet.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
