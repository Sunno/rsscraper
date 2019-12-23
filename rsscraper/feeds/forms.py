from django import forms
from rsscraper.feeds.models import Feed


class FeedForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        if not self.user:
            raise AttributeError('user param is required')
        super().__init__(*args, **kwargs)

    def clean(self):
        if Feed.objects.filter(user=self.user, url=self.cleaned_data['url']).exists():
            raise forms.ValidationError('Url already in database')

        return self.cleaned_data

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.user = self.user
        if commit:
            obj.save()
        return obj

    class Meta:
        model = Feed
        fields = ('url',)
