from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import LoginForm, SignUpForm, EditForm, ProfileEditForm
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(login_required, name='dispatch')
class EditView(View):

    def get(self, request):
        if bool(Profile.objects.filter(user=request.user)) is False:
            obj = Profile(user=request.user)
            obj.save()
        user_form = EditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request,
                      'accounts/edit.html', {
                          'user_form': user_form, 'profile_form': profile_form
                      })

    def post(self, request):
        user_form = EditForm(instance=request.user,
                             data=request.POST)
        profile_form = ProfileEditForm(
            files=request.FILES, instance=request.user.profile,
            data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            print('---------------------------------------')
            print(profile_form.cleaned_data['photo'])
            print('---------------------------------------')
            profile_form.save()
            messages.success(request, ' Your profile has been updated successfully')
            return redirect('accounts:edit')
        else:
            messages.error(request, '   Error occured while updating your profile, Please update again')
        return render(request,
                      'accounts/edit.html', {
                          'user_form': user_form, 'profile_form': profile_form
                      })


class UserSignUpView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:edit')
        user_form = SignUpForm()
        return render(request, 'accounts/signup.html', {'user_form': user_form})

    def post(self, request):
        user_form = SignUpForm(request.POST)
        print(user_form)
        try:
            already_user = User.objects.all().filter(
                email=user_form['email'].value())[0]

        except:
            already_user = None
        print(already_user, user_form['email'].value())
        if already_user is None:
            if user_form.is_valid():
                new_user = user_form.save(commit=False)
                new_user.set_password(user_form.cleaned_data['password'])
                new_user.is_active = False
                new_user.save()
                profile = Profile(user=new_user)
                profile.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your blog account.'
                message = render_to_string('activate_email.html', {
                    'user': new_user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                    'token': account_activation_token.make_token(new_user),
                })
                print(urlsafe_base64_encode(force_bytes(new_user.pk)),
                      account_activation_token.make_token(new_user))
                to_email = user_form.cleaned_data.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                messages.success(
                    request,
                    "  Successfully SignUp! Please activate your account mail has been send to your mail box! ")
                return redirect('accounts:login')
        else:
            messages.error(request, "   Email has been registered already!!!")
            return redirect('accounts:signup')
        return render(request, 'accounts/signup.html', {'user_form': user_form})


class ActivateView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "  Thank you for your email confirmation. Now you can login to your account.")
            return redirect('accounts:login')

        else:
            messages.error(request, "   Activation link is invalid!.", fail_silently=True)
            return redirect('accounts:login')


class UserLoginView(View):
    def get(self, request):
        form = LoginForm()
        if request.user.is_authenticated:
            return redirect('blogposts:list')
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = User.objects.all().filter(email=cd['email'])
            if username:
                user = authenticate(request, username=username[0],
                                    password=cd['password'])
                print(user)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        messages.success(request, " Authenticated Successfully")
                        return redirect('blogposts:user_post_list', request.user.username, request.user.id)
                    else:

                        messages.error(request, "   Your account is not activated, Please check your mail")
                        return redirect('accounts:login')

                else:
                    messages.error(request, "   Your have used wrong password")
                    return redirect('accounts:login')
            else:
                messages.error(request, "   Wrong Email has been please try again!!!")
                return redirect('accounts:login')
        return render(request, 'accounts/login.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class UserLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, ' You have Successfully logout from account')
        return redirect('accounts:login')
