from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from .token import account_activation_token
from django.shortcuts import render, redirect, reverse
import re
from django.http import HttpResponse
from .models import myuser
from .forms import RegisterationForm, loginForm, EditForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string



# Create your views here.

def home(request):
    if request.method == 'GET':
        context = {}
        email = request.session['Email']
        # password = request.session['password']
        users = myuser.objects.all()
        for user in users:
            if user.Email == email:
                context['user'] = user
                return render(request, 'home.html', context)
        # return HttpResponse(userr)
        # if users:


def login(request):
    context = {}
    form = loginForm()
    if (request.method == 'GET'):
        context['form'] = form
        return render(request, 'login.html', context)
    else:
        Email = request.POST['Email']
        password = request.POST['password']
        # check cred in User
        # authuser = authenticate(email=Email, password=password)
        # check cred in myuser
        user = myuser.objects.get(Email=Email, password=password)

        if user and user.is_active:
            request.session['Email'] = Email

            return redirect(reverse('home'))
        else:
            context['errormsg'] = 'Invalid credentials or not validated Email Address'
            return render(request, 'login.html', context)


def mylogout(request):
    request.session['username'] = None
    return redirect('login')



def edit(request):
    context = {}
    email = request.session['Email']
    users = myuser.objects.all()
    for user in users:
        if user.Email == email:
            context['current_user'] = user
    if request.method == "GET":
        return render(request, 'edit.html', context)
    else:

        if request.POST:
            user_form = EditForm(request.POST)

        if user_form.is_valid():

            userr = myuser.objects.get(Email=email)
            user_form = EditForm(request.POST, instance=userr)
            user_form.save()
            return redirect('home')
        else:
            userr = myuser.objects.get(Email=email)
            user_form = EditForm(instance=userr)

            return render(request, 'edit.html', {'form': user_form})

def delete(request):
    email = request.session['Email']
    myuser.objects.filter(Email=email).delete()
    return redirect('/login')


def signup(request):
    context={}
    if request.method == 'POST':
        form = RegisterationForm(request.POST, request.FILES)
        Email = request.POST['Email']
        password = request.POST['password']
        conf = request.POST['confirm_password']
        phoneNum = request.POST['phone_number']
        pattern = re.compile("^01[0125][0-9]{8}$")
        emailPattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        checkNum = pattern.match(phoneNum)
        checkMail = re.fullmatch(emailPattern,Email)
        checkPass = password == conf
        if not checkMail:
            context['errormsg'] = "Invalid Email Address"
            return render(request, 'register.html', context)
        if not checkNum:
            context['errormsg'] = "Invalid phone number"
            return render(request, 'register.html', context)
        if not checkPass:
            context['errormsg'] = "Passwords don't match"
            return render(request, 'register.html', context)
        if form.is_valid():
            conff = form.cleaned_data.get('conf')
            print(conff)
            # save form in the memory not in database
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # to get the domain of the current site
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('Email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )

            email.send()
            context['errormsg'] = 'Please confirm your email address to complete the registration'
            context['form'] = loginForm()
            return render(request, 'login.html', context)
            #return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = RegisterationForm()
    return render(request, 'register.html', {'form': form})

def activate(request, uidb64, token):
    #User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = myuser.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, myuser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')