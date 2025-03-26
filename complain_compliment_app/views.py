from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Users, Feedbacks, AdminResponse, Report
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pyrebase
from django.views.decorators.csrf import csrf_exempt
from requests.auth import HTTPBasicAuth


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
        if Members.objects.filter(email=email).exists() and user:
            session_id = user['idToken']
            request.session['uid'] = str(session_id)
            return JsonResponse({"message": "Successfully logged in"})
        elif not Members.objects.filter(email=email).exists():
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
        chama_name = data.get("chama")
        name = data.get("name")
        phone_number = data.get("phone_number")
        password = data.get("password")

        # Check if email already exists
        if Members.objects.filter(email=email).exists():
            return JsonResponse({"message": "Email already exists"}, status=400)

        # Create user
        user = authe.create_user_with_email_and_password(email, password)
        uid = user['localId']
        
        # Check if chama exists
        try:
            chama = Chamas.objects.get(name=chama_name)
        except Chamas.DoesNotExist:
            return JsonResponse({"message": "Chama not found"}, status=400)

        # Save member
        member = Members(chama=chama, name=name, email=email, phone_number=phone_number, password=uid)
        member.save()

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


