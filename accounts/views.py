from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache

from accounts.forms import RegisterForm, UserProfileForm, SearchForm, MessageForm
from accounts.models import Profile, Message
from photos.forms import CommentForm
from photos.models import Photo
from photos.utils import is_liked_by_user


@login_required
def home(request):
    profiles = Profile.objects.none()
    query = request.GET.get('query', '')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if query:
            profiles = Profile.objects.filter(user__username__icontains=query)
        else:
            profiles = Profile.objects.none()
        return render(request, 'common/partial_profiles.html', {'profiles': profiles, 'query': query})


    user_profile = request.user.profile
    followed_users = user_profile.following.all()
    followed_user_ids = followed_users.values_list('user__id', flat=True)

    photos = Photo.objects.filter(owner__id__in=followed_user_ids).order_by('-id')

    for photo in photos:
        photo.liked_by_user = is_liked_by_user(photo, request.user)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            # You need to know which photo is being commented on
            photo_id = request.POST.get('photo_id')
            photo = Photo.objects.get(pk=photo_id)

            comment = comment_form.save(commit=False)
            comment.photo = photo
            comment.author = request.user
            comment.save()

            return redirect('accounts:home')  # Redirect to avoid repost on refresh
    else:
        comment_form = CommentForm()

    form = SearchForm(request.GET)


    return render(request, 'common/home-page.html', {
        'search_form': form,
        'profiles': profiles,
        'query': query,
        'photos': photos,
        'comment_form': comment_form,
    })


def follow_user(request, username):
    target_user = get_object_or_404(User, username=username)
    request.user.profile.following.add(target_user.profile)
    return redirect('accounts:home')

def unfollow_user(request, username):
    target_user = get_object_or_404(User, username=username)
    request.user.profile.following.remove(target_user.profile)
    return redirect('accounts:home')

def root_redirect(request):
    if request.user.is_authenticated:
        return redirect('accounts:home')  # or wherever your home view is
    return redirect('accounts:sign_in')

def sign_in(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('accounts:home')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login-page.html', {'form': form})

def register(request):
    if request.method == "POST":
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:home')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register-page.html', {'form': form})

def sign_out(request):
    logout(request)
    return redirect('accounts:sign_in')

def profile_details(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    return render(request, 'accounts/profile-details-page.html', {'profile': profile})

def edit_profile(request, pk):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()

            profile.gender = form.cleaned_data.get('gender')
            profile_img = form.cleaned_data.get('profile_img')
            if profile_img:
                profile.profile_img = profile_img
            profile.save()

            return redirect('accounts:profile_details', pk=pk)
    else:
        form = UserProfileForm(
            instance=user,
            initial={
                'gender': profile.gender,
                'profile_img': profile.profile_img,
            }
        )

    return render(request, 'accounts/profile-edit-page.html', {'form': form})

def profile_delete(request, pk):
    profile = get_object_or_404(Profile, pk=pk)

    if request.method == 'POST':
        user = profile.user
        logout(request)
        profile.delete()
        user.delete()
        return redirect('accounts:sign_in')

    return render(request, 'accounts/profile-delete-page.html', {'profile': profile})

@never_cache
def chat(request, username):
    other_user = get_object_or_404(User, username=username)

    if request.method == "POST" and request.headers.get('X-requested-with') == 'XMLHttpRequest':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = other_user
            message.save()
            return render(request, 'accounts/messages_partial.html', {'message': message})
        else:
            return JsonResponse({'error': 'Invalid form'}, status=400)

    form = MessageForm()
    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        recipient__in=[request.user, other_user]
    ).order_by('timestamp')

    return render(request, 'accounts/chat.html', {
        'form': form,
        'messages': messages,
        'other_user': other_user
    })


