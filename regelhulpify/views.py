from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Max
from django.urls import reverse
from regelhulpify.models import Tool, Question, Answer
from regelhulpify.forms import ToolForm, QuestionForm, AnswerForm

# Create your views here.

def home(request):
    return HttpResponse("Hello, Django!")

def builder(request):
    context = {'tools': Tool.objects.all()}
    return render(request, 'regelhulpify/builder.html', context)

def builder_question(request, tool, question):
    t = get_object_or_404(Tool, id=tool)
    q = Question.objects.get(tool=t, position=question) 
    a = Answer.objects.filter(question=q)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=q)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('builder_tool', args=[tool]))
        else:
            context = {'form': form, 'tool': t, 'question': q, 'answers': a}
            return render(request, 'regelhulpify/builder_question.html', context)
    form = QuestionForm(initial={'text': q.text, 'expl': q.expl, 'tool': q.tool, 'position': q.position})  
    context = {'form': form, 'tool': t, 'question': q, 'answers': a}
    return render(request, 'regelhulpify/builder_question.html', context)

def builder_answer(request, tool, question, answer):
    t = get_object_or_404(Tool, id=tool)
    q = Question.objects.get(tool=t, position=question) 
    a = Answer.objects.get(pk=answer)
    if request.method == 'POST':
        form = AnswerForm(t, request.POST, instance=a)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('builder_question', args=[tool, question]))
        else:
            context = {'form': form, 'tool': t, 'question': q, 'answers': a}
            return render(request, 'regelhulpify/builder_question.html', context)
    form = AnswerForm(t, instance=a)  
    context = {'form': form, 'tool': t, 'question': q, 'answers': a}
    return render(request, 'regelhulpify/builder_answer.html', context)

def newanswer(request, tool, question):
    t = get_object_or_404(Tool, id=tool)
    q = Question.objects.get(tool=t, position=question) 
    if request.method == 'POST':
        form = AnswerForm(t, request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('builder_question', args=[tool, question]))
        else:
            context = {'form': form, 'tool': t}
            return render(request, 'regelhulpify/newquestion.html', context)
    else:               
        form = AnswerForm(t, initial={'question': q})  
        context = {'form': form, 'tool': t, 'question': q}
        return render(request, 'regelhulpify/newanswer.html', context)

def builder_tool(request, tool):
    t = get_object_or_404(Tool, id=tool)
    q = Question.objects.filter(tool=t) # overbodig tot API
    a = Answer.objects.filter(question=q)
    context = {'tool': t, 'questions': q, 'answers': a}
    return render(request, 'regelhulpify/builder_tool.html', context)

def newtool(request):
    if request.method == 'POST':
        form = ToolForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('builder'))
    else:        
        form = ToolForm
        context = {'form': form}
        return render(request, 'regelhulpify/newtool.html', context)

def newquestion(request, tool):
    t = get_object_or_404(Tool, id=tool)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('builder_tool', args=[tool]))
        else:
            context = {'form': form, 'tool': t}
            return render(request, 'regelhulpify/newquestion.html', context)
    else:               
        highest = t.question_set.aggregate(Max('position')).get('position__max') or 0
        p = highest + 1
        form = QuestionForm(initial={'tool' : t, 'position': p})  
        context = {'form': form, 'tool': t}
        return render(request, 'regelhulpify/newquestion.html', context)

def tool(request, tool):
    t = get_object_or_404(Tool, id=tool)
    context = {'tool': t}
    return render(request, 'regelhulpify/tool.html', context)

def question(request, tool, question):
    t = get_object_or_404(Tool, id=tool)
    q = t.question_set.get(position=question)
    a = q.answer_set.all()
    n = q.position + 1
    context = {'tool': t, 'question': q, 'answers': a, 'next': n}
    return render(request, 'regelhulpify/question.html', context)

    

    

