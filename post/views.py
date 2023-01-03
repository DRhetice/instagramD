from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponseRedirect


from post.models import *
from post.forms import NewPostForm
from userauths.models import Profile
from comment.models import Comment
from comment.forms import NewCommentForm

from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    user = request.user
    all_users = User.objects.all()
    posts = Stream.objects.filter(user=user)
    group_ids = []
    for post in posts:
        group_ids.append(post.post_id)
    post_items = Post.objects.filter(
        id__in=group_ids).all().order_by('-posted')
    context = {
        'post_items': post_items,
        'all_users' : all_users
    }
    return render(request, 'index.html', context)


def newPost(request):
    user = request.user.id
    tags_obj = []

    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            caption = form.cleaned_data.get('caption')
            tag_form = form.cleaned_data.get('tags')
            tag_list = list(tag_form.split(','))
            

            for tag in tag_list:
                t, created = Tag.objects.get_or_create(title=tag)
                tags_obj.append(t)
            p, created = Post.objects.get_or_create(picture=picture, caption =caption, user_id=user)
            p.tags.set(tags_obj)
            p.save()
            return redirect('index')
    else:
        form = NewPostForm()
    context = {
        'form': form
        }
    return render(request, 'newpost.html', context)


def postDetail(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    #comment
    comments = Comment.objects.filter(post=post).order_by('-date')
    
    #commentForm

    if request.method == "POST":
        form = NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.post = post
            comment.user = user
            comment.save()
            return HttpResponseRedirect(reverse('post-details', args=[post.id]))
    else:
        form = NewCommentForm()
    
    
    context = {
        'post' : post,
        'form':form,
        'comments': comments,
    }
    return render(request, 'postdetail.html', context)

def tags(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags=tag).order_by('-posted')
    context = {
        'posts': posts,
        'tag' : tag
    }
    return render(request, 'tags.html', context)

def likes(request, post_id):
    user = request.user
    post= Post.objects.get(id=post_id)
    current_likes = post.likes
    liked = Likes.objects.filter(user=user, post=post).count()
    if not liked:
        liked = Likes.objects.create(user=user, post=post)
        current_likes = current_likes + 1
    else:
        liked = Likes.objects.filter(user=user, post=post).delete()
        current_likes = current_likes - 1
    post.likes = current_likes
    post.save()
    return HttpResponseRedirect(reverse('index'))

def favorite(request, post_id):
    user = request.user
    post= Post.objects.get(id=post_id)
    profile = Profile.objects.get(user=user)
  
    if  profile.favorite.filter(id=post_id).exists():
        profile.favorite.remove(post)
    else:
        profile.favorite.add(post)
    return HttpResponseRedirect(reverse('post-details', args=[post_id]))