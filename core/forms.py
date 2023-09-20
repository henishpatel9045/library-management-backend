from django import forms
from django.contrib.auth import get_user_model

from .models import Issue

User = get_user_model()


class IssueAdminForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(IssueAdminForm, self).__init__(*args, **kwargs)
        self.fields["user"].queryset = User.objects.filter(is_superuser=False)
