from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from rsscraper.feeds.models import Feed


class FeedForm(forms.ModelForm):

    _cached_content = None

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        if not self.user:
            raise AttributeError('user param is required')
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('save', 'Save'))

    def clean_url(self):
        url = self.cleaned_data['url']

        parsed, valid = Feed.validate_url(url)

        if not valid:
            raise forms.ValidationError(
                f'Error fetching url: {parsed.bozo_exception}')

        self._cached_content = parsed

        return url

    def clean(self):
        if 'url' in self.cleaned_data and Feed.objects.filter(
                user=self.user, url=self.cleaned_data['url']).exists():
            raise forms.ValidationError('Url already in database')

        return self.cleaned_data

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.user = self.user
        if commit:
            obj.save()
            obj.set_content(self._cached_content)
            obj.fetch()
        return obj

    class Meta:
        model = Feed
        fields = ('url',)
