from django.contrib.auth import authenticate, login as login_user, logout as logout_user
from django.utils.datastructures import MultiValueDictKeyError
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
import random
# Create your views here.

def suffledimages():
    images = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p']
    random.shuffle(images)
    imageset = []
    imageset.append(list(images[0:4]))
    imageset.append(list(images[4:8]))
    imageset.append(list(images[8:12]))
    imageset.append(list(images[12:16]))
    return imageset

def aboutus(request):
    return render(request, 'aboutus.html')

def sendotp(recipient,subject,otp):
    message = subject + " OTP:\n\n" + str(otp) + "\n\nFrom PicPassword Team"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient])

def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html', {'username': request.user.username})
    else:
        return render(request, 'home.html')

def authenticate_user(id,password):
    user = authenticate(username=id, password=password)
    if user is not None:
        return user
    else:
        if User.objects.filter(email=id).exists():
            username = User.objects.filter(email=id).first().username
            user = authenticate(username=username, password=password)
            if user is not None:
                return user
            else:
                return None
        else:
            return None

def login(request):
    if request.user.is_authenticated:
        return redirect(f'/profile/{request.user.username}')
    elif request.method == 'POST':
        id = request.POST['id']
        try:
            password = request.POST['password']
        except MultiValueDictKeyError:
            return redirect('/login')
        user = authenticate_user(id,password)
        if user is not None:
            login_user(request, user)
            messages.info(request, f"{user.username} successfully logged in.")
            return redirect(f'/profile/{user.username}')
        else:
            messages.error(request, 'Oops! Invalid login.')
            return redirect('/login')
    else:
        return render(request, 'form.html', {'loginform':True,'imageset':suffledimages()})

def profile(request, username):
    if User.objects.filter(username=username).exists():
        if request.user.is_authenticated:
            if username == request.user.username:
                return render(request, 'profile.html', {'username':request.user.username,'email':request.user.email,'loggedin':True})
            else:
                return render(request, 'profile.html', {'username':username,'loggedin':False})
        else:
            return render(request, 'profile.html', {'username':username,'loggedin':False})
    else:
        messages.error(request, "Profile doesn't exist.")
        return redirect('/')

def logout(request):
    if request.user.is_authenticated:
        logout_user(request)
        messages.info(request, 'Successfully logged out.')
    return redirect('/')

def signup(request):
    if request.user.is_authenticated:
        messages.error(request,"Log out first to create a account.")
        return redirect('/login')
    elif request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        try:
            password = request.POST['password']
        except MultiValueDictKeyError:
            return redirect('/signup')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('/signup')
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
            return redirect('/signup')
        else:
            otp = random.randint(100000,999999)
            request.session['operation'] = {'type':'signup','username':username,'email':email,'password':password,'otp':otp}
            sendotp(email,'Email Confirmation',otp)
            messages.info(request,'Email confirmation OTP has been sent.')
            return redirect('/emailconfirmation')
    else:
        return render(request,'form.html',{'signupform':True,'imageset':suffledimages()})

def emailconfirmation(request):
    if 'operation' not in request.session:
        messages.error(request, "Access Denied.")
        return redirect('/')
    elif request.session['operation']['type'] != 'signup':
        messages.error(request, "Access Denied.")
        return redirect('/')
    elif request.method == 'POST':
        userotp = request.POST['otp']
        otp = request.session['operation']['otp']
        if int(userotp) == otp :
            username = request.session['operation']['username']
            email = request.session['operation']['email']
            password = request.session['operation']['password']
            user = User.objects.create_user(username=username,email=email,password=password)
            user.is_active = True
            user.save()
            del request.session['operation']
            messages.info(request, "Account created successfully.")
            return redirect('/login')
        else:
            del request.session['operation']
            messages.error(request, "Oops! Wrong OTP.")
            return redirect('/signup')
    else:
        return render(request,'form.html',{'otpform':True})

def accountdeletionrequest(request):
    if request.user.is_authenticated:
        otp = random.randint(100000,999999)
        request.session['operation'] = {'type':'accountdeletionrequest','username':request.user.username,'otp':otp}
        sendotp(request.user.email,'Account Deletion Request',otp)
        messages.info(request,'Account Deletion Request OTP has been sent.')
        return redirect('/deleteaccount')
    else:
        messages.error(request, "First login to delete the account.")
        return redirect('/login')

def deleteaccount(request):
    if 'operation' not in request.session:
        messages.error(request, "Access Denied.")
        return redirect('/')
    elif request.session['operation']['type'] != "accountdeletionrequest":
        messages.error(request, "Access Denied.")
        return redirect('/')
    elif request.user.is_authenticated:
        if request.method == 'POST':
            userotp = request.POST['otp']
            otp = request.session['operation']['otp']
            username = request.session['operation']['username']
            if int(userotp) == otp :
                user = User.objects.filter(username=username).first()
                user.delete()
                del request.session['operation']
                messages.info(request, "Account deleted successfully.")
                return redirect('/')
            else:
                del request.session['operation']
                messages.error(request, "Oops! Wrong OTP.")
                return redirect('/login')
        else:
            return render(request, 'form.html',{'otpform':True})
    else:
        messages.error(request, "First login to delete the account.")
        return redirect('/login')

def resetpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            otp = random.randint(100000,999999)
            request.session['operation'] = {'type':'resetpassword','otp':otp,'email':email}
            sendotp(email,'Reset Password',otp)
            messages.info(request,'Reset Password OTP has been sent.')
            return redirect('/resetpasswordotp')
        else:
            messages.error(request,"Email doesn't exist.")
            return redirect('/resetpassword')
    else:
        return render(request, 'form.html',{'emailform':True})

def resetpasswordotp(request):
    if 'operation' not in request.session:
        messages.error(request, "Access Denied.")
        return redirect('/login')
    elif request.session['operation']['type'] != 'resetpassword':
        messages.error(request, "Access Denied.")
        return redirect('/login')
    elif request.method == 'POST':
        userotp = request.POST['otp']
        otp = request.session['operation']['otp']
        if int(userotp) == otp :
            del request.session['operation']['otp']
            return redirect('/changepassword')
        else:
            del request.session['operation']
            messages.error(request, "Oops! Wrong OTP.")
            return redirect('/login')
    else:
        return render(request, 'form.html',{'otpform':True})

def changepassword(request):
    if 'operation' not in request.session:
        messages.error(request, "Access Denied.")
        return redirect('/login')
    elif request.session['operation']['type'] != 'resetpassword':
        messages.error(request, "Access Denied.")
        return redirect('/login')
    elif request.method == 'POST':
        try:
            password = request.POST['password']
        except MultiValueDictKeyError:
            return redirect('/changepassword')
        email = request.session['operation']['email']
        user = User.objects.filter(email=email).first()
        user.set_password(password)
        user.save()
        del request.session['operation']
        messages.info(request,"Password changed successfully.")
        return redirect('/login')
    else:
        return render(request, 'form.html', {'passwordform':True,'imageset':suffledimages()})

def changeusername(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            newusername = request.POST['username']
            if User.objects.filter(username=newusername).exists():
                messages.error(request,"Username already taken.")
                return redirect('/changeusername')
            else:
                user = User.objects.filter(username=request.user.username).first()
                user.username = newusername
                user.save()
                messages.info(request,"Username changed successfully.")
                return redirect('/login')
        else:
            return render(request,'form.html',{'usernameform':True})
    else:
        messages.error(request,"First login to change username.")
        return redirect('/login')
