from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
import bcrypt
import datetime

from compiler.models import user

# Create your views here.

class Userserializer(serializers.ModelSerializer):
	class Meta:
		model=user
		fields=('name','username','email')

@api_view(['GET'])
def welcome(request):

	message = {"status": 200}

	return Response(message)


@api_view(['GET'])
def getUsers(request):

	users=user.objects.all()
	w=list()

	for u in users:
		k=dict()
		k["name"]=u.name 
		k["username"]=u.username
		k["email"]=u.email
		w.append(k)
	##serializer=Userserializer(users,many=True)

	return Response(w)

@api_view(['POST'])
def signup(request):

	message={"status": 100}
	name=request.data.get("name")
	username=request.data.get("username")
	password=request.data.get("password")
	salt = bcrypt.gensalt()
	hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
	email=request.data.get("email")

	if(not all([name,username,password,email])):
		return Response(message)

	if(user.objects.filter(username=username).exists()):
		return Response(message)

	user1=user(name=name,username=username,email=email,password=hashed_password.decode('utf-8'))
	user1.save()

	return Response({"status": 200})

@api_view(['POST'])
def login(request):
	message={"status": 400}
	username=request.data.get("username")
	password=request.data.get("password")

	if(not all([username,password])):
		message["status"]=300
		return Response(message)

	if(not(user.objects.filter(username=username).exists())):
		message["status"]=100
		return Response(message)

	if not(bcrypt.checkpw(password.encode('utf-8'),user.objects.filter(username=username)[0].password.encode('utf-8'))):
		message["staus"]=90
		return Response(message)

	jwt_token=user.objects.filter(username=username).first().generateJWT()
	message["status"]=200
	message["jwt"]=jwt_token

	return Response(message)

@api_view(['POST'])
def coderunner(request):

	message={"status": 100}
	code_data=request.data.get("code")
	user_input=request.data.get("user_input")
	language=request.date.get("language")
	
	if not all([code_data,language]):
		return Response(message)
