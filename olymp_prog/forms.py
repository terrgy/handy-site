from django import forms

from olymp_prog.models import Task, Tag


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'link', 'tags', 'notes', ]


class TaskFilterForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        required=False,
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
    )
    link = forms.BooleanField(
        required=False,
        label='Testing system required'
    )


class TrainingSettings(TaskFilterForm):
    shuffle_method = forms.ChoiceField(
        choices=Task.get_shuffle_methods_choices(),
    )

    field_order = ['shuffle_method']
