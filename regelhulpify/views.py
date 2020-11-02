import json
import urllib
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Max
from django.urls import reverse
from django.core.serializers import serialize
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from regelhulpify.models import Tool, Question, Answer
from regelhulpify.forms import ToolForm, QuestionForm, AnswerForm
from regelhulpify.util import reset_tool, question_load_helper
from regelhulpify.context_processors import login_form

def home(request):
    return render(request, 'regelhulpify/index.html')

#LOGIN

def login_view(request, origin):
    print(request)
    origin = urllib.parse.unquote(origin)
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect(origin)
        else:
            return redirect('login_page')
    else:
        return HttpResponse(status="403")

def logout_view(request):
    logout(request)
    return redirect('home')

def login_page(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect(origin)
        else:
            context = {'form': AuthenticationForm(request.post)}
            return render(request, 'regelhulpify/login.html', context)
    else:
        context = {'form': AuthenticationForm}
        return render(request, 'regelhulpify/login.html', context)

# BUILDER

@login_required
def builder(request):
    context = {'tools': Tool.objects.all()}
    return render(request, 'regelhulpify/builder.html', context)

@login_required
def builder_question(request, tool, question):
    t = get_object_or_404(Tool, id=tool)
    q = Question.objects.get(tool=t, pk=question) 
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


@login_required
def builder_answer(request, answer):
    a = get_object_or_404(Answer, pk=answer)
    q = get_object_or_404(Question, pk=a.question.id) 
    t = get_object_or_404(Tool, pk=q.tool.id) 
    if request.method == 'POST':
        form = AnswerForm(t, request.POST, instance=a)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('builder_question', args=[t.id, q.id]))
        else:
            context = {'form': form, 'tool': t, 'question': q, 'answers': a}
            return render(request, 'regelhulpify/builder_question.html', context)
    form = AnswerForm(t, instance=a)  
    context = {'form': form, 'tool': t, 'question': q, 'answers': a}
    return render(request, 'regelhulpify/builder_answer.html', context)

@login_required
def newanswer(request, tool, question):
    t = get_object_or_404(Tool, id=tool)
    q = Question.objects.get(tool=t, pk=question) 
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

@login_required
def builder_tool(request, tool):
    t = get_object_or_404(Tool, id=tool)
    q = Question.objects.order_by("position").filter(tool=t) # overbodig tot API
    a = Answer.objects.filter(question=q)
    print(q)
    context = {'tool': t, 'questions': q, 'answers': a}
    return render(request, 'regelhulpify/builder_tool.html', context)

@login_required
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

@login_required
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
    return render(request, 'regelhulpify/question.html')

# API paths

def get_tools(request):
    '''Get a list of tools (eventually depending on filters)'''
    t = Tool.objects.all() #to do: limit once user has been implemented
    data = serialize('json', t)
    return JsonResponse(data, safe=False)    

def get_complete_tool(request, tool):
    '''Get a single tool and all questions and answers'''
    t = Tool.objects.filter(pk=tool)
    questions = Question.objects.order_by("position").filter(tool=t[0])
    question_list = []
    for question in questions:
        question_dict = question_load_helper(question)
        question_list.append(question_dict)
    data = {'tool': serialize('json', t), 'questions': question_list}
    return JsonResponse(data, safe=False)   

def get_toolstart(request, tool):
    '''Get a single tool and the start question'''
    t = Tool.objects.get(pk=tool)
    q = t.question_set.get(position=1)
    data = {'name': t.name, 'desc': t.desc, 'img': t.img,'start': q.pk}
    return JsonResponse(data, safe=False)    

def get_question(request, question):
    '''Get a single question and all answers'''
    q = Question.objects.get(pk=question)
    question_dict = question_load_helper(q)
    question_dict['tool'] = q.tool.name
    data = {'question': question_dict}
    return JsonResponse(data, safe=False)    

@csrf_exempt
def question_move(request, question, direction):
    '''Change the position of a question by 1'''
    if (request.method != "PUT") or (direction not in ["up", "down"]):
        return HttpResponse(status=403)
    q = Question.objects.get(pk=question)
    t = q.tool

    # Reset question numbering in case an earlier request went wrong
    reset_tool(t.id)

    # Get next question, if it exists
    next_p = q.position + 1 if (direction == 'up') else q.position - 1
    try:
        next_q = t.question_set.get(position=next_p)
    except:
        return HttpResponse(status=204)
    
    # Trade places
    next_q.position = q.position
    q.position = 9999
    q.save()
    next_q.save()
    q.position = next_p
    q.save()

    return HttpResponse(status=200)  

@csrf_exempt
def question_delete(request, question):
    if request.method == "DELETE":
        q = get_object_or_404(Question, pk=question)
        q.delete()
        reset_tool(q.tool.id)
        return HttpResponse(status=200)  
    else:
        return HttpResponse(status=403)  

def tool_delete(request, tool):
    if request.method == "DELETE":
        t = get_object_or_404(Tool, id=tool)
        t.delete()
        return HttpResponse(status=200)  
    else:
        return HttpResponse(status=403)  





    

    

