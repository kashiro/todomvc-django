from django.forms import ModelForm
from todo.models import Todo


class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ('title', 'completed')

    #def clean_title(self):
    #    '''how to validate data'''
    #    self.cleaned_data.get('title')
    #    title == 'test':
    #        raise form.validationError('do not input test')
    #    return title
