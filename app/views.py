from .models import *
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.urls import reverse
from datetime import datetime
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .utils import token_generator_email, token_generator_password

# Create your views here.

def index (request):
    time_now = datetime.utcnow()
    user_profile = Profile.objects.filter(user = request.user).first()
    feed = Post.objects.all()
    if request.method == 'POST':
        text_content = request.POST['text_content']
        post = Post.objects.create(profile= user_profile,text_content=text_content, posted_at = datetime.utcnow())
        post.save()
        
        return redirect('index')

    return render(request, 'index.html', {'user_profile' : user_profile, 'feed': feed, 'time_now' : time_now})

def profile (request, pk):
    
    profile = Profile.objects.get(user__username = pk)
    number_of_followers = len(Follow.objects.filter(who_is_being_followed = profile.user.username))
    following = len(Follow.objects.filter(who_is_following = profile.user.username))

    if Follow.objects.filter(who_is_following = request.user.username, who_is_being_followed = profile.user.username):
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    context = {
        'number_of_followers' : number_of_followers,
        'following' : following,
        'profile' : profile,
        'button_text' : button_text
    }
         
    return render(request, 'profile.html', context)

def follow (request):
    
    if request.method == 'POST':
        who_is_being_followed = request.POST['who_is_being_followed']
        
        if len(Follow.objects.filter(who_is_following = request.user.username, who_is_being_followed = who_is_being_followed)) == 0:
            follow = Follow.objects.create(who_is_following = request.user.username, who_is_being_followed = who_is_being_followed)
            follow.save()
            return redirect (f'profile/{who_is_being_followed}')
        else: 
            follow = Follow.objects.get(who_is_following = request.user.username, who_is_being_followed =who_is_being_followed)
            follow.delete()
            return redirect (f'profile/{who_is_being_followed}')
    else:
        return redirect (f'profile/{who_is_being_followed}')
            

def sign_up(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST ['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email = email):
                messages.error(request,"This email alrealdy exist")
                return redirect('signup')
            elif User.objects.filter(username = username):
                messages.error(request,"This username alrealdy exist")
                return redirect('signup')
            
            else:
                user = User.objects.create_user(username = username, email = email, password = password)
                user.is_active = False
                user.save()

                profile = Profile.objects.create(user = user, id_user = user.pk)
                profile.save()

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse('email-verification',kwargs={'uidb64' : uidb64, 'token': token_generator_email.make_token(user)})
                activate_url ='http://'+domain+link

                email_subject = 'Activate your account'
                email_body = f'Hi {user.username}! Use this link to verify your account:\n {activate_url}'
                
                email_confirm = EmailMessage (
                    email_subject,
                    email_body,
                    'davidjango0604@gmail.com',
                    [email],
                )

                email_confirm.send(fail_silently=False)

                messages.success(request, "Account created sucessfully, check your e-mail for account verification")
                return redirect('signin')


        else:
            messages.error(request,"The passwords do not match.")
            return redirect('signup')

    return render(request, 'signup.html')

def email_verification(request, uidb64,token):


    try:
        id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk = id)
        
        if not token_generator_email.check_token(user, token):
                return HttpResponse('You alrealdy changed your email')
        
        if user.is_active:
            return redirect('signin')
        
        user.is_active = True
        user.save()

        messages.success(request,"Your acccount was activated sucessfully!")
        return redirect('signin')

    except Exception as ex:
        pass


    return redirect('signin')

def forgot_password(request):

    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.get(email = email)

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        domain = get_current_site(request).domain
        link = reverse('change-password',kwargs={'uidb64' : uidb64, 'token': token_generator_password.make_token(user)})
        activate_url ='http://'+domain+link

        email_subject = 'Reset your password'
        email_body = f'Hi {user.username}! Use this link to change your password:\n {activate_url}'
        
        email_confirm = EmailMessage (
            email_subject,
            email_body,
            'davidjango0604@gmail.com',
            [email],
                )

        email_confirm.send(fail_silently=False)
        messages.success(request, "Email succesfully sent.Please, check your mailbox.")
        
        return redirect('signin')



    return render(request, 'forgot-password.html')

def change_password(request, uidb64,token):
    
    try:
        id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk = id)

        if not token_generator_password.check_token(user, token):
            
            return HttpResponse("This email is invalid, if you want to change your password again, send another email")

        if request.method == 'POST':
            password = request.POST['password']
            password2 = request.POST['password2']

            if password == password2:
                if password != None:
                    user.set_password(password)
                    user.save()
                    print("PASSWORD alterado com sucesso")
                    messages.success(request,"Password succesfully changed.Please, sign in.")
                    return redirect('signin')
                else:
                    # MENSAGEM DE ERRO, SENHA INVALIDA
                    messages.error("Invalid password.")
                    return redirect('change-password')
            else:
                # MENSAGEM DE ERRO, SENHAS NAO COINCIDEM
                messages.error("Invalid password.")
                return redirect('change-password')
          
    except Exception as ex:
        pass

    return render(request, 'change-password.html', {'user' : user})
    
def sign_in(request):
    if request.method == 'POST':
        login_user = request.POST['login']
        password = request.POST['password']
        

        if User.objects.filter(username = login_user).first():
            user_login = authenticate(username = login_user, password = password)
            login(request,user_login)  
            
            return redirect ('index')      
        
        elif User.objects.filter(email = login_user).first():
            user = User.objects.get(email = login_user)
            user_login = authenticate(username = user.username, password = password)
            login(request, user_login)

            return redirect ('index')

    return render(request, 'signin.html')
       
def logout_user(request):
    
    logout(request)
    return redirect ('signin')

def profile_settings(request):
    user_profile = Profile.objects.get(user = request.user)
    user = User.objects.get(username = user_profile.user)


    if request.method == 'POST':
        if request.FILES.get('image') != None:
            profile_image = request.FILES.get('image')
            bio = request.POST['bio']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']

            user_profile.bio = bio
            user_profile.profile_img = profile_image
            user_profile.first_name = first_name
            user_profile.last_name = last_name

            user_profile.save()

        if request.FILES.get('image') == None:
            profile_image = user_profile.profile_img
            bio = request.POST['bio']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            
            user_profile.bio = bio
            user_profile.profile_img = profile_image
            user_profile.first_name = first_name
            user_profile.last_name = last_name
            

            user_profile.save()

        return redirect ('profile-settings')

    return render (request, 'settings.html', {'user_profile' : user_profile,})

def editing_change_password(request):
    messages.error(request,"TESTE")    
    return render (request,'change-password.html')

