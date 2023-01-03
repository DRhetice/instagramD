from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.urls import resolve,reverse
from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login

from post.models import *
from userauths.models import *
from userauths.form import *

def userProfile(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    url_name = resolve(request.path).url_name
    if url_name == 'profile':
        posts = Post.objects.filter(user=user).order_by('-posted')
    else:
        posts= profile.favorite.all()
    
    #Tracking Profile stats
    post_count = Post.objects.filter(user=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    follower_count = Follow.objects.filter(following=user).count()


    
    #pagination
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    posts_paginator = paginator.get_page(page_number)

    #follow status

    follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

    context = {
        'posts' : posts,
        'profile' : profile,
        'posts_paginator' : posts_paginator,
        'follower_count' : follower_count,
        'following_count' : following_count,
        'post_count':post_count,
        'follow_status':follow_status,
    }
    return render(request, 'profile.html', context)

def follow(request, username, option):
    use = request.user
    following = get_object_or_404(User, username=username)
    try:
        f, created = Follow.objects.get_or_create(follower=use, following=following)
        
        if int(option) == 0:
            f.delete()
            Stream.objects.filter(following=following, user=request.user).all().delete()
        else:
            posts = Post.objects.all().filter(user=following)[:10]

            with transaction.atomic():
                for post in posts:
                    stream = Stream(post=post, user=use, date=post.posted, following=following)
                    stream.save()      
        return HttpResponseRedirect(reverse('profile',args=[username] ))
    
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('profile',args=[username]))
            


def editProfile(request,username):
    user = request.user
    profile = Profile.objects.get(user__id=user.id)
    if request.method=='POST':
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile.image = form.cleaned_data.get('image') or profile.image 
            profile.first_name = form.cleaned_data.get('first_name')
            profile.last_name = form.cleaned_data.get('last_name')
            profile.location = form.cleaned_data.get('location')
            profile.url = form.cleaned_data.get('url')
            profile.bio = form.cleaned_data.get('bio')
            profile.save()
            return redirect('profile', profile.user.username)
    else:
        form = EditProfileForm(instance=request.user.profile)

    context = {
        'form':form,
    }
    return render(request, 'editprofile.html', context)

 

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            # Profile.get_or_create(user=request.user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hurray your account was created!!')

            # Automatically Log In The User
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],)
            login(request, new_user)
            # return redirect('editprofile')
            return redirect('index')
            


    elif request.user.is_authenticated:
        return redirect('index')
    else:
        form = UserRegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'sign-up.html', context)

