from django import forms
from ckeditor.widgets import CKEditorWidget


class CommentForm(forms.Form):
	reply_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'id':'reply_id'}))

	content_type = forms.CharField(widget=forms.HiddenInput)
	object_id = forms.IntegerField(widget=forms.HiddenInput)

	text = forms.CharField(widget=CKEditorWidget(config_name='comment'))
