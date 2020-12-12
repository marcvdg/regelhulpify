import json
import urllib
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Max
from django.urls import reverse
from django.core.serializers import serialize
from django.forms.models import model_to_dict
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from regelhulpify.models import Tool, Question, Answer, User
from regelhulpify.forms import ToolForm, QuestionForm, AnswerForm
from regelhulpify.util import reset_tool, question_load_helper
from regelhulpify.context_processors import login_form

# FRONT

def home(request):
    return render(request, 'regelhulpify/index.html')

def alltools(request):
    return render(request, 'regelhulpify/alltools.html')

def tool(request, tool):
    t = get_object_or_404(Tool, id=tool)
    context = {'tool': t}
    return render(request, 'regelhulpify/tool.html', context)

def toolslug(request, slug):
    try: 
        t = Tool.objects.get(shorturl=slug)
    except:
        return redirect('home')
    return redirect('tool', t.pk)

def question(request, tool, question):
    return render(request, 'regelhulpify/question.html')
    
# BUILDER

@login_required
def builder(request):
    '''Homepage after login'''
    t = Tool.objects.filter(owner=request.user)
    context = {'tools': t}
    return render(request, 'regelhulpify/builder.html', context)

@login_required
def newtool(request):
    ''' Form page to create new tool '''
    if request.method == 'POST':
        form = ToolForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            new_t = form.save()
            # redirect to a new URL:
            messages.success(request, 'Tool created successfully!', extra_tags='alert alert-success')
            return redirect('builder_tool', new_t.pk)
        else:
            print(form.errors)
            context = {'form': form}
        return render(request, 'regelhulpify/newtool.html', context)
    else:        
        form = ToolForm(initial={'owner': request.user})
        context = {'form': form}
        return render(request, 'regelhulpify/newtool.html', context)

@login_required
def edittool(request, tool):
    ''' Lets you edit details of an existing tool '''
    t = get_object_or_404(Tool, id=tool)
    # Check for ownership
    if t.owner != request.user:
        return HttpResponseForbidden('Not your tool.')
    
    # If post, check form
    if request.method == 'POST':
        form = ToolForm(request.POST, instance=t)
        if form.is_valid():
            form.save()
            return redirect('builder_tool', tool)
        else:
            context = {'form': form, 'tool': tool}
            return render(request, 'regelhulpify/edittool.html', context)
    else:        
        form = ToolForm(instance=t)
        context = {'form': form, 'tool': tool}
        return render(request, 'regelhulpify/edittool.html', context)

@login_required
def builder_tool(request, tool):
    ''' Gives an overview of a tool, including all questions and answers '''
    t = get_object_or_404(Tool, id=tool)
    
    # Check for ownership
    if t.owner != request.user:
        return HttpResponseForbidden('Not your tool.')

    q = Question.objects.order_by("position").filter(tool=t) 
    a = Answer.objects.filter(question=q)
    context = {'tool': t, 'questions': q, 'answers': a}
    return render(request, 'regelhulpify/builder_tool.html', context)

@login_required
def newquestion(request, tool, result=0):
    ''' Form page to create new question, redirects to multiple answer form '''
    t = get_object_or_404(Tool, id=tool)
    if t.owner != request.user:
        return HttpResponseForbidden('Not your tool.')
    # If method POST, try and save result
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            new_q = form.save()
            if new_q.result:
                return redirect('builder_tool', tool)
            return redirect('newanswers', tool, new_q.pk)
            # return HttpResponseRedirect(reverse('builder_question', args=[tool, new_q.pk]))
        else:
            # If errors, display form with previous POST input
            context = {'form': form, 'tool': t}
            return render(request, 'regelhulpify/newquestion.html', context)
    else:               
        # Set position...
        highest = t.question_set.aggregate(Max('position')).get('position__max') or 0
        p = highest + 1
        form = QuestionForm(initial={'tool' : t, 'position': p, 'result': result})  

        # Set type...
        r = 'question' if result == 0 else 'result'
        context = {'form': form, 'tool': t, 'type': r}

        # ...and display form
        return render(request, 'regelhulpify/newquestion.html', context)

@login_required
def builder_question(request, tool, question):
    ''' Lets user view and edit an existing question and all answers  '''
    t = get_object_or_404(Tool, id=tool)
    if t.owner != request.user:
        return HttpResponseForbidden('Not your tool.')
    
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

    # GET request: set form and context        
    form = QuestionForm(instance=q)
    r = 'Vraag' if q.result == 0 else 'Uitkomst' 
    context = {'form': form, 'tool': t, 'question': q, 'answers': a, 'type': r}
    return render(request, 'regelhulpify/builder_question.html', context)


@login_required
def newanswer(request, tool, question):
    ''' Lets user create a new answer '''
    t = get_object_or_404(Tool, id=tool)
    if t.owner != request.user:
        return HttpResponseForbidden('Not your tool.')

    q = Question.objects.get(tool=t, pk=question) 
    if request.method == 'POST':
        form = AnswerForm(t, q.position, request.POST)
        if form.is_valid():
            form.save()
            return redirect('builder_question', question)
        else:
            context = {'form': form, 'tool': t}
            return render(request, 'regelhulpify/newquestion.html', context)
    else:               
        form = AnswerForm(t, q.position, initial={'question': q})  
        context = {'form': form, 'tool': t, 'question': q}
        return render(request, 'regelhulpify/newanswer.html', context)

@login_required
def newanswers(request, tool, question):
    ''' A form that allows users to create multiple answers at once '''
    t = get_object_or_404(Tool, id=tool)
    if t.owner != request.user:
        return HttpResponseForbidden('Not your tool.')

    q = Question.objects.get(tool=t, pk=question) 
    if request.method == 'POST':
        print(request.POST)
    context = {'tool': t, 'question': q}
    return render(request, 'regelhulpify/newanswers.html', context)

@login_required
def builder_answer(request, tool, question, answer):
    ''' A form that allows users to edit a single answer '''
    t = get_object_or_404(Tool, pk=tool) 
    if t.owner != request.user:
        return HttpResponseForbidden('Not your tool.')
    
    a = get_object_or_404(Answer, pk=answer)
    q = get_object_or_404(Question, pk=a.question.id) 

    if request.method == 'POST':
        form = AnswerForm(t, q.position, request.POST, instance=a)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('builder_question', args=[t.id, q.id]))
        else:
            context = {'form': form, 'tool': t, 'question': q, 'answer': a}
            return render(request, 'regelhulpify/builder_question.html', context)
    form = AnswerForm(t, q.position, instance=a)  
    context = {'form': form, 'tool': t, 'question': q, 'answer': a}
    return render(request, 'regelhulpify/builder_answer.html', context)


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
    
    try:
        q = t.question_set.get(position=1).pk 
    except: 
        q = ''
    data = {'name': t.name, 'desc': t.desc, 'img': t.img,'start': q}
    return JsonResponse(data, safe=False)    

def get_question(request, question):
    '''Get a single question and all answers'''
    q = Question.objects.get(pk=question)
    question_dict = question_load_helper(q)
    question_dict['tool'] = q.tool.name
    data = {'question': question_dict}
    return JsonResponse(data, safe=False)    

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

def tool_delete(request, tool):
    ''' Deletes a tool after fetch request'''
    if request.method == "DELETE":
        t = get_object_or_404(Tool, id=tool)
        t.delete()
        return HttpResponse(status=200)  
    else:
        return HttpResponse(status=403)  

def question_delete(request, question):
    ''' Deletes a question after fetch request'''
    if request.method == "DELETE":
        q = get_object_or_404(Question, pk=question)
        q.delete()
        reset_tool(q.tool.id)
        return HttpResponse(status=200)  
    else:
        return HttpResponse(status=403)  

def answer_delete(request, answer):
    ''' Deletes a question after fetch request'''
    if request.method == "DELETE":
        a = get_object_or_404(Answer, pk=answer)
        a.delete()
        return HttpResponse(status=200)  
    else:
        return HttpResponse(status=403)  

def answer_getnext(request, question):
    ''' Load all 'next question' options for answer form '''
    if request.method == "GET":
        q = get_object_or_404(Question, pk=question)
        t = q.tool
        # next_set = Question.objects.filter(tool=t).filter(position__gt=q.position).all()
        next_set = Question.objects.filter(tool=t).all()
        next_list = []
        for item in next_set:
            next_list.append({ 'pk': item.pk, 'text': item.text })
        return JsonResponse(next_list, safe=False)    
    else:
        return HttpResponse(status=403)  

def answers_add(request, question):
    ''' Add multiple answers '''
    if request.method == "POST":
        q = get_object_or_404(Question, pk=question)
        t = q.tool
        data = json.loads(request.body)
        for item in data['data']:
            if item['nextquestion'] != '':
                nq = get_object_or_404(Question, pk=item['nextquestion'])
                a = Answer(text=item['text'], question=q, nextquestion=nq)
            else:
                a = Answer(text=item['text'], question=q)
            a.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)  

    

    

