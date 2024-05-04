from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from subplatform import settings
from .forms import CreateUserForm
from .models import CustomUser
from .token import user_tokenizer_generator


# Create your views here.
def home(request):
    return render(request, 'account/index.html')


def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('account/email-verification.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_tokenizer_generator.make_token(user)
            })
            user_email = user.email
            send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER,
                      recipient_list=[user_email])

            return redirect('email-verification-sent')

    context = {'RegisterForm': form}

    return render(request, 'account/register.html', context)


def logins(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_writer is True:
                login(request, user)
                # return HttpResponse('Welcome Client')
                return redirect('writer-dashboard')
            if user is not None and user.is_writer is False:
                login(request, user)
                # return HttpResponse('Welcome Client')
                return redirect('client-dashboard')
    context = {'LoginForm': form}
    return render(request, 'account/login.html', context)


@login_required(login_url="login")
def logouts(request):
    logout(request)
    return redirect('login')


def email_verification(request, uidb64, token):
    unique_token = force_str(urlsafe_base64_decode(uidb64))
    custom_user = CustomUser.objects.get(pk=unique_token)
    if custom_user and user_tokenizer_generator.check_token(custom_user, token):
        custom_user.is_active = True
        custom_user.save()
        return redirect('email-verification-success')
    else:
        return redirect('email-verification-failed')


def email_verification_sent(request):
    return render(request, 'account/email-verification-sent.html')


def email_verification_success(request):
    return render(request, 'account/email-verification-success.html')


def email_verification_failed(request):
    return render(request, 'account/email-verification-failed.html')
