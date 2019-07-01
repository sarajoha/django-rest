from django.shortcuts import render
from django.http import HttpResponse
import json
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login as login_user
from .serializers import UserSerializer
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication


# Create your views here.
@require_POST
@csrf_exempt
def login(request):
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    username = request.POST.get('username', '')
    if not email:
        data = {'message': 'Hey, falta el email'}
        return HttpResponse(json.dumps(data), status=400)
    if not password:
        data = {'message': 'Hey, falta la contraseña'}
        return HttpResponse(json.dumps(data), status=400)
    if not username:
        data = {'message': 'Hey, falta el usuario'}
        return HttpResponse(json.dumps(data), status=400)

    #create user
    try:
        User.objects.get(username=username)
        data = {'message': 'El usuario ya existe'}
        return HttpResponse(json.dumps(data), status=400)
    except:
        if User.objects.filter(email=email):
            data = {'message': 'Ya se ha registrado un usuario con este correo'}
            return HttpResponse(json.dumps(data), status=400)
        else:
            User.objects.create(email=email, password=password, username=username)

    user = authenticate(email=email, password=password)
    if user:
        login_user(request, user)
        data = {'message': 'El usuario se ha logueado'}
        return HttpResponse(json.dumps(data), status=200)

    data = {'message': 'hola'}
    return HttpResponse(json.dumps(data), status=200)


class LoginView(APIView):
    permission_classes = (AllowAny,)

    @csrf_exempt
    def post(self, request, **kwargs):
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        username = request.POST.get('username', '')
        if not email:
            data = {'message': 'Hey, falta el email'}
            return HttpResponse(json.dumps(data), status=400)
        if not password:
            data = {'message': 'Hey, falta la contraseña'}
            return HttpResponse(json.dumps(data), status=400)
        if not username:
            data = {'message': 'Hey, falta el usuario'}
            return HttpResponse(json.dumps(data), status=400)

        #create user
        User.objects.create(email=email, password=password, username=username)

        user = authenticate(email=email, password=password)
        if user:
            login_user(request, user)
            data = {'message': 'El usuario se ha logueado'}
            return HttpResponse(json.dumps(data), status=200)

        data = {'message': 'hola'}
        return HttpResponse(json.dumps(data), status=200)


class UserViewset(viewsets.ModelViewSet):

   queryset = User.objects.all()
   serializer_class = UserSerializer
   permission_classes = (IsAuthenticated,)
   #permission_classes = (AllowAny,)

   @action(detail=False, methods=['post'], url_path='recent-users', permission_classes=[AllowAny])
   def recent_users(self, request):
       recent_users = User.objects.all().order_by('-last_login')

       page = self.paginate_queryset(recent_users)


       serializer = self.get_serializer(recent_users, many=True)
       return Response(serializer.data)


class InstagramView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, **kwargs):
        image_url = request.data.get('image_url', '')
        link = request.data.get('link', '')
        if not link:
            data = {'message': 'Hey, falta el link'}
            return HttpResponse(json.dumps(data), status=400)
        if not image_url:
            data = {'message': 'Hey, falta la imagen'}
            return HttpResponse(json.dumps(data), status=400)

        data = {'image': image_url}
        return HttpResponse(json.dumps(data), status=200)
