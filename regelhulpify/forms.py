from django.forms import ModelForm, HiddenInput, Textarea
from regelhulpify.models import Tool, Question, Answer
from django.utils.translation import gettext_lazy as _
from django_registration.forms import RegistrationForm


class RhRegistrationForm(RegistrationForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '') 
        super(RhRegistrationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ToolForm(ModelForm):
    class Meta:
        model = Tool
        fields = ['name', 'desc', 'img', 'shorturl', 'owner']
        widgets = {
            'owner': HiddenInput(),
            'desc': Textarea(attrs={'rows': 3})
        }
        labels = {
            "name": "Name",
            "desc": "Description",
            "img": "Image (link)",
            "shorturl": "Short url",
        }
        help_texts = {
            'img': _('Optional. Make sure the link ends with .jpg of .png.'),
            'shorturl': _('Optional. Lowercast only.')
        }

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '') 
        super(ToolForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = 'on'
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['text','expl','tool','position', 'result']
        widgets = {
            'tool': HiddenInput(), 
            'position': HiddenInput(), 
            'result': HiddenInput(),
            'expl': Textarea(attrs={'rows': 3}),
        }
        labels = {
            "text": "Text",
            "expl": "Explanation",
        }
        help_texts = {
            'expl': _('Optional.'),
        }

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '') 
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['autofocus'] = 'on'
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['text','nextquestion', 'question']
        widgets = {
            'question': HiddenInput(),
        }
        labels = {
            "text": "Text",
            "nextquestion": "Next question or result",
        }
        help_texts = {
            'nextquestion': _('Optional. Use for logic once you have created all questions & results.'),
        }

    def __init__(self, tool, position, *args, **kwargs):
        kwargs.setdefault('label_suffix', '') 
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['autofocus'] = 'on'
        self.fields['nextquestion'].queryset = Question.objects.filter(tool=tool).filter(position__gt=position)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    

       
        
