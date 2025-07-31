from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import Message
from photos.forms import PhotoForm, CommentForm, SharePhotoForm
from photos.models import Photo, Like

@login_required
def like_toggle(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, photo=photo)

    if not created:
        like.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

def create_photo(request):
    if request.method == 'POST':
        create_photo_form = PhotoForm(request.POST, request.FILES)
        if create_photo_form.is_valid():
            photo = create_photo_form.save(commit=False)
            photo.owner = request.user
            photo.save()
            create_photo_form.save_m2m()
            return redirect('accounts:home')
    else:
        create_photo_form = PhotoForm()

    return render(request, 'photos/photo-add-page.html', {'form': create_photo_form})

def photo_details(request, pk):
    photo = get_object_or_404(Photo, pk=pk)

    # Handle AJAX POST request to add a comment
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.photo = photo
            comment.author = request.user
            comment.save()

            # Return the rendered HTML of the new comment
            return render(request, 'photos/comment_partial.html', {'comment': comment})
        else:
            return JsonResponse({'errors': comment_form.errors}, status=400)

    # Normal GET request
    comment_form = CommentForm()

    liked_by_user = False
    if request.user.is_authenticated:
        liked_by_user = photo.likes.filter(user=request.user).exists()

    return render(request, 'photos/photo-details-page.html', {
        'photo': photo,
        'liked_by_user': liked_by_user,
        'form': comment_form,
    })

def edit_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.method == 'POST':
        edit_photo_form = PhotoForm(request.POST, request.FILES, instance=photo)
        if edit_photo_form.is_valid():
            edit_photo_form.save()
            return redirect('photos:photo-details', pk=pk)
    else:
        edit_photo_form = PhotoForm(instance=photo)

    return render(request, 'photos/photo-edit-page.html', {'form': edit_photo_form})

def share_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)

    if request.method == 'POST':
        form = SharePhotoForm(request.POST, user=request.user)
        if form.is_valid():
            recipient_profile = form.cleaned_data['recipient']
            Message.objects.create(
                sender=request.user,
                recipient=recipient_profile.user,
                photo=photo,
            )
            return redirect('accounts:profile_details', pk=request.user.profile.pk)
    else:
        form=SharePhotoForm(user=request.user, initial={'photo_id': photo.id})

    return render(request, 'photos/share_photo.html', {'form': form, 'photo': photo})


def delete_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    photo.delete()
    return redirect('photos:photo-details', pk=pk)