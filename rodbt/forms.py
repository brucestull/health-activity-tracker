from django.forms import ModelForm, ModelMultipleChoiceField

from rodbt.models import Journal, Question


class QuestionForm(ModelForm):
    """
    Form for a user to create a new `Question`.
    """
    # journals = ModelMultipleChoiceField()
    # Journal.objects.filter(author=self.request.user).order_by('-date')
    class Meta:
        model = Question
        fields = [
            'body',
            'journal',
        ]
    
    def __init__(self, *args, **kwargs):
        """
        Add the `user`s `Journal`s to the form's `journal` field.

        We do this so the user can only select their own `Journal`s.
        """
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['journal'].queryset = Journal.objects.filter(author=user).order_by('-date')
