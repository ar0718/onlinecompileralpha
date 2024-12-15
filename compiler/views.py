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

