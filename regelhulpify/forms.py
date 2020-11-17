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
            "name": "Naam",
            "desc": "Beschrijving",
            "img": "Afbeelding (link)",
            "shorturl": "Korte url",
        }
        help_texts = {
            'img': _('Make sure the link ends with .jpg of .png.'),
        }

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['text','expl','tool','position', 'result']
        widgets = {'tool': HiddenInput(), 'position': HiddenInput(), 'result': HiddenInput()}
        labels = {
        "text": "Tekst",
        "expl": "Toelichting",
        }

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['text','nextquestion', 'question']
        widgets = {'question': HiddenInput()}
        labels = {
        "text": "Tekst",
        "nextquestion": "Volgende vraag",
        }

    def __init__(self, tool, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['nextquestion'].queryset = Question.objects.filter(tool=tool)
 
    

       
        
