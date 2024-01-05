from django.contrib.auth import login, get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views import View
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from django.contrib.auth.tokens import default_token_generator
import requests
import json
import logging


logger = logging.getLogger(__name__)
# peppered a lot of logger lines because i needed lots of debugging
# also a lot of different types of error handling responses,
# the register page gave me quite some issues so yes. 

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password):
            return user

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        
@method_decorator(csrf_exempt, name='dispatch')
class UserLoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            logger.info(f'Authenticating user with email: {email} and password: {password}')
            
            backend = EmailBackend()
            user = backend.authenticate(request, username=email, password=password)

            logger.info(f'Authenticated user: {user}')

            if user is not None:
                login(request, user, backend='login.views.EmailBackend')
                token = default_token_generator.make_token(user)
                return JsonResponse({'status': 'success', 'token': token})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid email or password'}, status=401)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class UserRegisterView(View):
    
    def check_username_exists(self, username):
        return User.objects.filter(username=username).exists()
    
    def post(self, request, *args, **kwargs):
        
        data = json.loads(request.body)
        logger.info('Received data: %s', data)
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        recaptcha_token = data.get('recaptchaToken')

       # Check if the reCAPTCHA is valid
        if not self.verify_recaptcha(recaptcha_token):
            return JsonResponse({'error': 'Invalid reCAPTCHA.'}, status=400)
        
        # Check if the username already exists
        if self.check_username_exists(username):
            return JsonResponse({'error': 'This username is already taken.'}, status=400)

        try:
            user = User.objects.create_user(username, email, password)
            # If the user was created successfully, return a success response
            return JsonResponse({'message': 'Registration successful'}, status=201)
        except IntegrityError as e:
            logger.error('IntegrityError: %s', e)
            return JsonResponse({'error': 'This username is already taken.'}, status=400)
        except ValidationError as e:
            logger.error('ValidationError: %s', e)
            return JsonResponse({'error': 'Invalid data.'}, status=400)
        except Exception as e:
            logger.error('Unexpected error: %s', e)
            return JsonResponse({'error': 'Registration failed.'}, status=400)

    
    def verify_recaptcha(self, token):
        recaptcha_verify_url = f'https://recaptchaenterprise.googleapis.com/v1/projects/lang-aide/assessments?key=my-recaptcha-key'
        response = requests.post(
            recaptcha_verify_url,
            json={
                'event': {
                    'token': token,
                    'siteKey': 'my-recaptcha-sitekey',
                }
            },
            headers={
                'Content-Type': 'application/json'
            }
        )
        response_data = response.json()
        logger.info('reCAPTCHA response: %s', response_data)
        
        return response_data.get('tokenProperties', {}).get('valid', False)
    
    def get(self, request, *args, **kwargs):
        # This method will handle the username availability check
        username = request.GET.get('username')
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'isTaken': True})
        else:
            return JsonResponse({'isTaken': False})


