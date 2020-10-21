from django.forms import ModelForm, HiddenInput
from regelhulpify.models import Tool, Question, Answer

class ToolForm(ModelForm):
    class Meta:
        model = Tool
        fields = ['name', 'desc']

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['text','expl','tool','position']
        widgets = {'tool': HiddenInput(), 'position': HiddenInput()}

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['text','nextquestion', 'question']
        widgets = {'question': HiddenInput()}

    def __init__(self, tool, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['nextquestion'].queryset = Question.objects.filter(tool=tool)
    

       
        
