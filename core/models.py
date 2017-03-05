import bcrypt as bcrypt

from core import config_path
import mongoengine
import configparser
import datetime


config = configparser.RawConfigParser()
config.read(config_path)
mongoengine.connect(config.get('mongoconfig', 'db_name'))


class HospitalModel(mongoengine.Document):
    name = mongoengine.StringField(max_length=100, required=True)
    email = mongoengine.EmailField(max_length=50,required=True )
    address = mongoengine.StringField(max_length=200,required=True )
    speciality = mongoengine.StringField(max_length=500, required=True)
    logo = mongoengine.ImageField(size=(800, 600, True), thumbnail_size=(200, 100))
    description = mongoengine.StringField(max_length=1000, required=True)
    date_joined = mongoengine.DateTimeField(default=datetime.datetime.now())
    patient_data = mongoengine.FileField()
    is_active = mongoengine.BooleanField(default=False)
    is_logged_in = mongoengine.BooleanField(default=False)
    is_admin = mongoengine.BooleanField(default=False)
    password = mongoengine.StringField(required=True)

    @property
    def hash_password(self):
        return self.password

    @hash_password.setter
    def set_hash_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


class UserFacebookModel(mongoengine.Document):
    name = mongoengine.StringField(max_length=100, )
    email = mongoengine.EmailField(max_length=50, )
    fb_id = mongoengine.StringField(max_length=100)


class UserHospitalModel(mongoengine.Document):
    pass
