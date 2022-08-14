from django import forms
from .models import Comment, Song


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class SongUploadForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'banner', 'audio_file', 'mood', 'genre']

    def __init__(self, *args, **kwargs):
        super(SongUploadForm, self).__init__(*args, **kwargs)

        # add class to default html tags created by django
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

        # add attribute to define acceptable file-type
        self.fields['banner'].widget.attrs['accept'] = "image/png, image/gif, image/jpeg"
        self.fields['audio_file'].widget.attrs['accept'] = 'audio/*'
