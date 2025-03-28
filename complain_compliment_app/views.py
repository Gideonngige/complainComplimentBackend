from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Users, Feedbacks, AdminResponse, Report
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pyrebase
from django.views.decorators.csrf import csrf_exempt
from requests.auth import HTTPBasicAuth
import json
from .serializers import FeedbacksSerializer


config = {
  "apiKey": "AIzaSyAz8Ka9y8fAdidaB2RMYCNWiehOVupE5R0",
  "authDomain": "complaincompliment-aa841.firebaseapp.com",
  "databaseURL": "https://complaincompliment-aa841-default-rtdb.firebaseio.com/",
  "projectId": "complaincompliment-aa841",
  "storageBucket": "complaincompliment-aa841.firebasestorage.app",
  "messagingSenderId": "649355734540",
  "appId": "1:649355734540:web:dd48dc996f179f912c0829",
  "measurementId": "G-MW6KYHFLYH"
}
firebase = pyrebase.initialize_app(config)
authe = firebase.auth() 
database = firebase.database()

def index(request):
    return render(request, 'index.html')



#start of login api
def login(request, email, password):
    try:
        user = authe.sign_in_with_email_and_password(email,password)
        if Users.objects.filter(email=email).exists() and user:
            session_id = user['idToken']
            request.session['uid'] = str(session_id)
            return JsonResponse({"message": "Successfully logged in"})
        elif not Users.objects.filter(email=email).exists():
            return JsonResponse({"message": "No user found with this email,please register"})
        elif not user:
            return JsonResponse({"message": "Invalid email"})
        else:
            return JsonResponse({"message": "please register"})
    except:
        message = "Invalid Credentials!! Please Check your data"
        return JsonResponse({"message": message})
    
    
#end of login api

#start of logout api
def logout(request):
    try:
        del request.session['uid']
    except:
        pass 
    return JsonResponse({"message": "Successfully logged out"})
#end of logout api

#start of register api
@csrf_exempt
@api_view(['POST'])
def register(request):
    try:
        data = json.loads(request.body)  # Convert request body to JSON
        
        # Extract data
        email = data.get("email")  # Define email first
        role = data.get("role")
        password = data.get("password")

        # Check if email already exists
        if Users.objects.filter(email=email).exists():
            return JsonResponse({"message": "Email already exists"}, status=400)

        # Create user
        user = authe.create_user_with_email_and_password(email, password)
        uid = user['localId']

        # Save member
        user = Users(email=email, role=role, password=uid)
        user.save()

        return JsonResponse({"message": "Successfully registered"}, status=201)

    except Exception as e:
        print("Error:", str(e))  # Log error for debugging
        return JsonResponse({"message": "Registration failed", "error": str(e)}, status=500)
#end of register api

#end of reset api
def resetpassword(request, email):
    try:
        authe.send_password_reset_email(email)
        message = "A email to reset password is successfully sent"
        return JsonResponse({"message": message})
    except:
        message = "Something went wrong, Please check the email, provided is registered or not"
        return JsonResponse({"message": message})
#start of reset api

#get feedbacks api
@api_view(['GET'])
def getfeedbacks(request, email):
    try:
        user_id = Users.objects.get(email=email)
        if not user_id:
            return JsonResponse({"message":"Invalid email address"})
        feedbacks = Feedbacks.objects.get(user_id=user_id)
        serializer = FeedbacksSerializer(feedbacks)
        return JsonResponse(serializer.data)
    except Feedbacks.DoesNotExist:
        return JsonResponse({"message":"You do not have any feedbacks"})
#end of get feedbacks api


#start of feedbacks api 
@api_view(['POST'])
def feedbacks(request):
    try:
        data = json.loads(request.body)
        email = data.get('email') 
        title = data.get('title')
        category = data.get('category')
        message = data.get('message')
        anonymous = data.get('anonymous')
       
        user = Users.objects.get(email=email)
        print(user.user_id)
        # return JsonResponse({"message":user.user_id})
        if anonymous == "true":
            user1 = None
        elif anonymous == "false":
            user1 = Users.objects.get(email=email)
        if user:
            feedback = Feedbacks(user_id=user1, title=title, category=category,message=message, status="pending")
            feedback.save()
            return JsonResponse({"message":"Feedback was successfully submitted","status":200})
        else:
            return JsonResponse({"message":"Please signin"})

    except Users.DoesNotExist:
        return Response({"message":"Invalid email address"})
#end of feedbacks api