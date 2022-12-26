from .models import *
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.urls import reverse
from datetime import datetime
from itertools import chain
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .utils import token_generator_email, token_generator_password

# Create your views here.

def index (request):
    time_now = datetime.utcnow()
    user_profile = Profile.objects.get(user__username = request.user)
    user_posts = Post.objects.filter(profile = user_profile).order_by("posted_at")
    user_follow = Follow.objects.get(following = user_profile)
    feed = user_posts
    
    for profile in user_follow.followed.all():
        follower_posts = Post.objects.filter(profile = profile)
        feed = feed | follower_posts

    feed.order_by("posted_at")



    context = {
        'user_profile' : user_profile,
        'feed' : feed,
        'time_now' : time_now,
        # 'follow_sugestions' : follow_sugestions
    }

    if request.method == 'POST':
        post_image = None
        if request.FILES.get('image') != None:
            post_image = request.FILES.get('image')
        text_content = request.POST['text_content']
        post = Post.objects.create(profile= user_profile,text_content=text_content, posted_at = datetime.utcnow(), image = post_image)
        post.save()
        
        return redirect('index')

    return render(request, 'index.html', context)

def profile (request, username):
    
    profile = Profile.objects.get(user__username = username)
    user_profile = Profile.objects.get(user = request.user)
    user_follow = Follow.objects.get(following = user_profile)
    profile_follow = Follow.objects.get(following = profile)
    profile_posts = Post.objects.filter(profile = profile)
  
    if profile in user_follow.followed.all():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    context = {
        'profile' : profile,
        'button_text' : button_text,
        'profile_follow' : profile_follow,
        'profile_posts' : profile_posts
        
    }
         
    return render(request, 'profile.html', context)

def post(request,pk):
    
    post = Post.objects.get(pk = pk)
    comments = Comment.objects.filter(post = post)

    context = {
        'post' : post,
        'comments' : comments
    }

    return render(request, 'post.html', context)

def comment(request,pk):
    if request.method == 'POST':
        post_path = request.POST['post_path']
        post = Post.objects.get(pk = pk)
        user_profile = Profile.objects.get(user = request.user)
        text_content = request.POST['text_content']

        comment = Comment.objects.create(post = post, text_content = text_content, 
                                            posted_at = datetime.now(), profile = user_profile)
        comment.save()

        return redirect(post_path)

def follow (request):
    
    if request.method == 'POST':
        who_is_being_followed = request.POST['who_is_being_followed']
        wbf_profile = Profile.objects.get(user__username = who_is_being_followed)
        user_profile = Profile.objects.get(user = request.user)
        user_follow = Follow.objects.get(following = user_profile)

        # if len(Follow.objects.filter(who_is_following = request.user.username, who_is_being_followed = who_is_being_followed)) == 0:
        #     follow = Follow.objects.create(who_is_following = request.user.username, who_is_being_followed = who_is_being_followed)
        #     follow.save()
        #     return redirect (f'profile/{who_is_being_followed}')
        # else: 
        #     follow = Follow.objects.get(who_is_following = request.user.username, who_is_being_followed =who_is_being_followed)
        #     follow.delete()
        #     return redirect (f'profile/{who_is_being_followed}')
        
        if wbf_profile in user_follow.followed.all():
            user_follow.followed.remove(wbf_profile)
            return redirect (f'profile/{who_is_being_followed}')

        else:
            user_follow.followed.add(wbf_profile)
            return redirect (f'profile/{who_is_being_followed}')



           
    else:
        return redirect (f'profile/{who_is_being_followed}')

def delete_post(request,pk):
    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        if post.image:
            post.image.delete()
        post.delete()
        
        return redirect ('/')

def like (request):
     
    if request.method == 'POST':
        post_being_liked = request.POST['post_being_liked']
        post_liked = Post.objects.get(pk = post_being_liked)
        next = request.POST['next']
        liked = None
        
        if len(Like.objects.filter(who_is_liking = request.user.username, post_being_liked = post_liked.id)) == 0:
            like = Like.objects.create(who_is_liking = request.user.username, post_being_liked = post_liked.id)
            like.save()
            post_liked.likes += 1
            post_liked.save()
            
            return redirect(next)
        
        else:
            alrealdy_liked = Like.objects.get(who_is_liking = request.user.username, post_being_liked = post_liked.id)
            alrealdy_liked.delete()
            post_liked.likes -= 1
            post_liked.save()
            
            return redirect(next)
    else:
        
        return redirect('/')

def search(request):
    if request.method == 'POST':
        search = request.POST['search']
        profiles_search = Profile.objects.filter(Q(user__username__icontains = search) | Q(nickname = search))


        return render(request,'search.html', {'profiles_search' : profiles_search })

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

                profile = Profile.objects.create(user = user)
                profile.save()

                follow_obj = Follow.objects.create(following = profile)
                follow_obj.save()


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
            user_profile.profile_img.delete()
            profile_image = request.FILES.get('image')
            bio = request.POST['bio']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            nickname = request.POST['nickname']

            user_profile.nickname = nickname
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
            nickname = request.POST['nickname']

            user_profile.nickname = nickname
            user_profile.bio = bio
            user_profile.profile_img = profile_image
            user_profile.first_name = first_name
            user_profile.last_name = last_name
            

            user_profile.save()

        return redirect ('index')

    return render (request, 'settings.html', {'user_profile' : user_profile,})

def editing_change_password(request):
    messages.error(request,"TESTE")    
    return render (request,'change-password.html')

