from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views import View
import xgboost as xgb
import pandas as pd
from .models import URLHistory
import json
import pickle
import re
# Login and Signup View
def login_signup_view(request):
       if request.method == 'POST':
        if 'email' in request.POST:  # Signup form includes email
            # Signup process
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            # Check if user already exists
            if User.objects.filter(username=username).exists():
              alert_message = 'Username already taken'
              return render(request, 'loginandsignup.html', {'alert_message': alert_message})
            # Create a regular user with the given credentials
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            # After successful signup, redirect to the login page
            return redirect('login_signup')  # Redirect to the login page after signup
        elif 'password' in request.POST and 'email' not in request.POST:  # Login form doesn't include email
            # Login process
            username = request.POST.get('username')
            password = request.POST.get('password')
            # Authenticate user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to the dashboard after successful login
            else:
                alert_message = 'Invalid credentials'
                return render(request, 'loginandsignup.html', {'alert_message': alert_message})
    # Render the login and signup page for GET requests
       return render(request, 'loginandsignup.html')  # Always return an HttpResponse object here
# Dashboard View (protected by login)
@login_required(login_url='login_signup')
def dashboard(request):
    user_history = URLHistory.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'dashboard.html', {'history': user_history})
# URL Analysis View
class AnalyzeURLView(View):
    def load_model(self):
        self.model = xgb.XGBClassifier()
        self.model.load_model('xgboost_model.json')
    def extract_features_from_url(self, url):
        url_length = len(url)
        num_special_chars = len(re.findall(r'[\W_]', url))
        # Load the label encoder
        with open(r'app01\model\label_encoder_url.pkl', 'rb') as f:
            label_encoder_url = pickle.load(f)
        # Encode the URL
        url_encoded = label_encoder_url.transform([url])[0] if url in label_encoder_url.classes_ else 0
        # Return features as a DataFrame
        features = {
            'url': [float(url_encoded)],
            'url_length': [float(url_length)],
            'num_special_chars': [float(num_special_chars)]
        }
        return pd.DataFrame(features)
    def post(self, request):
        url = request.POST.get('url')
        if not url:
            return JsonResponse({'message': 'No URL provided'}, status=400)

        if not hasattr(self, 'model'):
            self.load_model()
        try:
            features = self.extract_features_from_url(url)#extracts features from the url
            prediction = self.model.predict(features)[0] #passes the features for prediction 
            result = 'malicious' if prediction == 1 else 'safe'#returns weather the url is safe or not 
            URLHistory.objects.create(user=request.user, url=url, result=result)
            return JsonResponse({'result': result})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
# View to render the history table and add history entries
@login_required
def add_history(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        url = data.get('url')
        result = data.get('result')
        # Save the history entry in the database
        new_entry = URLHistory.objects.create(user=request.user, url=url, result=result)
        # Send a response with the entry details including a timestamp
        return JsonResponse({
            'timestamp': new_entry.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'url': new_entry.url,
            'result': new_entry.result
        })
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)
#for clearing the history    
@login_required
def clear_history(request):
    if request.method == 'POST':
        # Clear all history for the logged-in user
        URLHistory.objects.filter(user=request.user).delete()
        return JsonResponse({'message': 'History cleared successfully.'})
#for reseting the password
def reset_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        new_password = data.get('new_password')
        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            return JsonResponse({'message': 'Password reset successfully'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'message': 'Username not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)