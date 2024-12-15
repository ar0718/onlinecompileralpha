from django.db import models
import jwt
import datetime

# Create your models here.

JWT_SECRET_KEY = "jhvaskjnsdkbddkis@#"

class user(models.Model):

	name = models.CharField(max_length=255)
	username = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)

	def __str__(self):
		return self.username
		
	def generateJWT(self):
		expiration_time = datetime.datetime.utcnow()+datetime.timedelta(minutes=30)

		payload = {
			'username': self.username,
			'email': self.email,
			'exp': expiration_time
		}
		token = jwt.encode(payload,JWT_SECRET_KEY, algorithm='HS256')
		return token
