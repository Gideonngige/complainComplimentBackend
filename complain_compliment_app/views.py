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
from .serializers import FeedbacksSerializer, AdminResponseSerializer, ReportSerializer, UsersSerializer
import hashlib
from django.db.models import Q
from django.db.models import Sum
from django.utils.timezone import now


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

# email hash function 
def hash_email(email):
    hash_object = hashlib.sha256(email.encode())
    hex_dig = hash_object.hexdigest()
    return hex_dig
# end of email hash function

#get feedbacks api
@api_view(['GET'])
def getfeedbacks(request, email):
    try:
        user_id = Users.objects.get(email=email)
        email_hash = hash_email(email)
        if not user_id:
            return JsonResponse({"message":"Invalid email address"})
        feedbacks = Feedbacks.objects.filter(Q(user_id=user_id) | Q(email_hash=email_hash))
        serializer = FeedbacksSerializer(feedbacks, many=True)
        return JsonResponse(serializer.data, safe=False)
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
        email_hash = hash_email(email)
        
        if user and not anonymous:
            feedback = Feedbacks(user_id=user, email_hash=email_hash, title=title, category=category,message=message, status="pending")
            feedback.save()
            return JsonResponse({"message":"Feedback was successfully submitted","status":200})
        else:
            feedback = Feedbacks(email_hash=email_hash, title=title, category=category,message=message, status="pending")
            feedback.save()
            return JsonResponse({"message":"Feedback was successfully submitted","status":200})

    except Users.DoesNotExist:
        return Response({"message":"Invalid email address"})
#end of feedbacks api

# start of get feedacks for admin api
def getadminfeedbacks(request, department):
    print(department)
    feedbacks = Feedbacks.objects.filter(status__in=["pending", "on-progress"], category=department).order_by('-created_at')
    serializer = FeedbacksSerializer(feedbacks, many=True)
    return JsonResponse(serializer.data, safe=False)
# end of get feedbacks for admin api

# start of admin response api

@api_view(['POST'])
def adminresponse(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        feedback_id = data.get('feedback_id')
        message = data.get('message')
        a_response = data.get('response')
        status = data.get('status')

        if not Users.objects.filter(email=email).exists():
            return JsonResponse({"message":"Invalid email address"})

        admin_id = Users.objects.get(email=email)
        feedback = Feedbacks.objects.get(feedback_id=feedback_id)
        admin_response = AdminResponse(admin_id=admin_id, feedback_id=feedback, message=message, response=a_response)
        admin_response.save()
        feedback.status = status
        feedback.updated_at = admin_response.response_date
        feedback.save()
        return JsonResponse({"message":"Response was successfully submitted","status":200})

    except Feedbacks.DoesNotExist:
        return JsonResponse({"message":"Feedback with this id does not exist"})
    except AdminResponse.DoesNotExist:
        return JsonResponse({"message":"Admin response with this id does not exist"})
# end of admin response api

# start of notification api
@api_view(['GET'])
def notification(request, email):
    try:
        # Get the logged-in user
        user = Users.objects.get(email=email) 

        # Get all feedbacks for this user
        feedback_ids = list(Feedbacks.objects.filter(user_id=user).values_list('feedback_id', flat=True))
        print(feedback_ids)

        if not feedback_ids:
            return Response({"message": "No feedbacks found"}, status=404)

        # Get all admin responses related to the user's feedbacks
        responses = AdminResponse.objects.filter(feedback_id__in=feedback_ids).order_by('-response_date')

        if not responses.exists():
            return Response({"message": "No responses found"}, status=404)

        # Serialize and return the responses
        serializer = AdminResponseSerializer(responses, many=True)
        return Response(serializer.data)

    except Exception as e:
        return Response({"message": f"An error occurred: {str(e)}"}, status=500)
#end of notification api

# start of get_receive_resolved api
@api_view(['GET'])
def countreceivedresolved(request):
    academic_received = Feedbacks.objects.filter(status__in=["pending", "on-progress", "resolved"],category="academic").count()
    academic_resolved = Feedbacks.objects.filter(status__in=["resolved"], category="academic").count()
    administration_received = Feedbacks.objects.filter(status__in=["pending", "on-progress", "resolved"],category="administration and support").count()
    administration_resolved = Feedbacks.objects.filter(status__in=["resolved"], category="administration and support").count()
    health_received = Feedbacks.objects.filter(status__in=["pending", "on-progress", "resolved"],category="health and wellness").count()
    health_resolved = Feedbacks.objects.filter(status__in=["resolved"], category="health and wellness").count()
    ict_received = Feedbacks.objects.filter(status__in=["pending", "on-progress", "resolved"],category="ict and communication").count()
    ict_resolved = Feedbacks.objects.filter(status__in=["resolved"], category="ict and communication").count()
    student_received = Feedbacks.objects.filter(status__in=["pending", "on-progress", "resolved"],category="student services").count()
    student_resolved = Feedbacks.objects.filter(status__in=["resolved"], category="student services").count()
    maintenance_received = Feedbacks.objects.filter(status__in=["pending", "on-progress", "resolved"],category="maintenance and environment").count()
    maintenance_resolved = Feedbacks.objects.filter(status__in=["resolved"], category="maintenance and environment").count()
    return Response(
        {
            'academic_received': academic_received, "academic_resolved": academic_resolved,
            'administration_received': administration_received, "administration_resolved": administration_resolved,
            'health_received': health_received, "health_resolved": health_resolved,
            'ict_received': ict_received, "ict_resolved": ict_resolved,
            'student_received': student_received, "student_resolved": student_resolved,
            'maintenance_received': maintenance_received, "maintenance_resolved": maintenance_resolved,
            })

# end of get_receive_resolved api

# start of report api
def report():
    current_month = now().strftime("%B")
    print(current_month)
    complains = Feedbacks.objects.filter(title__in=["complain"]).count()
    compliments = Feedbacks.objects.filter(title__in=["compliment"]).count()
    received = Feedbacks.objects.filter(status__in=["pending", "on-progress", "resolved"]).count()
    resolved = Feedbacks.objects.filter(status__in=["resolved"]).count()
    report = Report(month=current_month, total_complaints=complains, total_compliments=compliments, total_resolved=resolved, total_feedbacks=received)
    report.save()
# end of report api

#start of get report
@api_view(['GET'])
def getreport(request):
    current_month = now().strftime("%B")
    reports = Report.objects.filter(month=current_month)
    if not reports:
        report()
        serializer = ReportSerializer(reports, many=True)
    else:
        serializer = ReportSerializer(reports, many=True)
    
    return Response(serializer.data)
# end of get report

# start get user api 
@api_view(['GET'])
def getuser(request, email):
    try:
        user = Users.objects.get(email=email)
        serializer = UsersSerializer(user, many=False)
        return JsonResponse(serializer.data, safe=False)
    except Users.DoesNotExist:
        return JsonResponse({"message":"User not found"}, status=404)
    except Exception as e:
        return JsonResponse({"message":"Something went wrong"}, status=500)
# end of get user api