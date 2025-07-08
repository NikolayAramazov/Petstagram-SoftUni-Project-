from django import forms
from accounts.models import Profile
from photos.models import Photo, Comment


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['photo', 'description', 'location', 'tagged_pet']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class SharePhotoForm(forms.Form):
    recipient = forms.ModelChoiceField(
        queryset=Profile.objects.none(),
        label="Share with",
        empty_label='Select user',
                                       )
    photo_id = forms.IntegerField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['recipient'].queryset = user.profile.following.all()