from django.forms import ModelForm, HiddenInput
from regelhulpify.models import Tool, Question, Answer
from django import forms
from django.utils.translation import gettext_lazy as _

class ToolForm(ModelForm):
    class Meta:
        model = Tool
        fields = ['name', 'desc', 'img', 'shorturl', 'owner']
        widgets = {'owner': HiddenInput()}
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

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['text','expl','tool','position', 'result']
        widgets = {'tool': HiddenInput(), 'position': HiddenInput(), 'result': HiddenInput()}
        labels = {
        "text": "Text",
        "expl": "Explanation",
        }
        help_texts = {
            'expl': _('Optional.'),
        }

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['text','nextquestion', 'question']
        widgets = {'question': HiddenInput()}
        labels = {
        "text": "Text",
        "nextquestion": "Next question",
        }
        help_texts = {
            'nextquestion': _('Optional. Use for logic once you have created all questions & results.'),
        }

    def __init__(self, tool, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['nextquestion'].queryset = Question.objects.filter(tool=tool)
 
    

       
        
