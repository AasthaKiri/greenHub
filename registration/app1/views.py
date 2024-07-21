from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.mail import EmailMessage
import certifi
import smtplib
import ssl


# Create your views here.
@login_required(login_url='login')
def HomePage(request):
    return render(request, 'home.html')


def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Your password and confirm password are not Same!!")

        if User.objects.filter(username=uname).exists():
            messages.error(request, "Username already exists. Please choose a different one.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered. Please use a different email.")
            return redirect('signup')

        else:

            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect('login')

    return render(request, 'signup.html')


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Username or Password is incorrect!!!")

    return render(request, 'login.html')

@login_required(login_url='login')
def LogoutPage(request):
    logout(request)
    return redirect('login')


def password_reset_request(request):
    if request.method == "POST":
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)

            # Create a password reset token and send it to the user's email
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

            # Send email with password reset link
            subject = 'Password Reset Request'
            message = render_to_string('password_reset_email.html', {
                'user': user,
                'domain': request.META['HTTP_HOST'],
                'uidb64': uidb64,
                'token': token,
            })
            from_email = settings.EMAIL_HOST_USER
            to_email = [user.email]

            # Create the email message
            email_message = EmailMessage(subject, message, from_email, to_email)

            # Encode the message as bytes
            message_as_bytes = message.encode('utf-8')

            # Configure SSL context with certifi
            context = ssl.create_default_context(cafile=certifi.where())
            try:
                with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
                    server.starttls(context=context)  # Secure the connection
                    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                    server.sendmail(from_email, to_email, message_as_bytes)
            except Exception as e:
                messages.error(request, 'Error sending email: {}'.format(e))
                return render(request, 'password_reset_request.html')

            messages.success(request, 'Password reset email has been sent.')
            return redirect('password_reset_done')
        else:
            messages.error(request, 'Email address not found. Please enter a valid email.')
            return render(request, 'password_reset_request.html')

    return render(request, 'password_reset_request.html')


def password_reset_done(request):
    return render(request, 'password_reset_done.html')

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        # Check if the token is valid for the user
        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                password1 = request.POST['password1']
                password2 = request.POST['password2']
                if password1 == password2:
                    user.set_password(password1)
                    user.save()
                    messages.success(request, 'Password reset successful. You can now login with your new password.')
                    return redirect('login')
                else:
                    messages.error(request, 'Passwords do not match. Please try again.')
                    return render(request, 'password_reset_confirm.html', {'uidb64': uidb64, 'token': token})
            return render(request, 'password_reset_confirm.html', {'uidb64': uidb64, 'token': token})
        else:
            messages.error(request, 'Password reset link is invalid or has expired. Please request a new one.')
            return redirect('password_reset_request')
    except Exception as e:
        print(e)
        messages.error(request, 'An error occurred. Please try again.')
        return redirect('password_reset_request')

def password_reset_complete(request):
    return render(request, 'password_reset_complete.html')