from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from googleapiclient.discovery import build
import google.oauth2.credentials
import google_auth_oauthlib.flow as gFlow
import os

CLIENT_ID_PATH = os.path.join(settings.BASE_DIR, ('client_secret.json'))
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

flow = gFlow.Flow.from_client_secrets_file(CLIENT_ID_PATH, scopes=['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/plus.me', 'https://www.googleapis.com/auth/userinfo.email'])

# Create your views here.
class LoginView(generic.TemplateView):
    template_name = 'auth_google/login.html'

    #for redirection IF user is already logged in
    def dispatch(self, request, *args, **kwargs):
        if (request.user.is_authenticated):
            return redirect("pages:home")
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)
################Login and Registration with Google###############################
def AuthView(request):

    if (settings.DEBUG):
        flow.redirect_uri = settings.DEBUG_CALLBACK
    else:
        flow.redirect_uri = settings.PROD_CALLBACK

    authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true', prompt='consent')
    return redirect(authorization_url)

def oAuthCallBack(request):
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    credentials = flow.credentials
    service = build('oauth2', 'v2', credentials=credentials)
    resource = service.userinfo().get()
    response = resource.execute()

    email = response['email']
    name = response['name']
    user = authenticate(email=email)

    if user:
        login(request, user)
    else:
        #create the user
        user = User.objects.create_user(response['id'], response['email'])
        user.save()

        #authenticate using the newly created user
        user = authenticate(email=email)
        login(request, user)

    return redirect('pages:home')

def logoutView(request):
    logout(request)
    return redirect('login')
