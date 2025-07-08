# photos/utils.py
from photos.forms import CommentForm


def is_liked_by_user(photo, user):
    if not user.is_authenticated:
        return False
    return photo.likes.filter(user=user).exists()
