from regelhulpify.models import Tool, Question, Answer
from django.shortcuts import get_object_or_404, HttpResponse
from django.http import Http404

def reset_tool(tool):
    '''Reset the positioning of a tool's questions'''
    t = get_object_or_404(Tool, id=tool)
    q = Question.objects.order_by('position', 'pk').filter(tool=t)
    for question in q:
        print(str(question.text) + str(question.position))
    p = 1
    for question in q:
        print("old" + str(question.position))
        question.position = p
        question.save()
        print("new" + str(question.position))
        p = p + 1
    return HttpResponse('Succes')  

def question_load_helper(question):
    ''' Util function that gets question and its answers based on id '''
    answer_list = []
    for answer in question.answer_set.all():
        if answer.nextquestion != None: 
            next_q_id = answer.nextquestion.id 
            next_q_text = answer.nextquestion.text 
        else: 
            try: 
                next_q = Question.objects.get(position=(question.position+1), tool=question.tool)
                next_q_id = next_q.id
                next_q_text = next_q.text
            except:
                next_q_id = ""
                next_q_text = "[Laatste vraag]"
        answer_dict = {'id': answer.pk, 'text': answer.text, 'nextquestion': next_q_id, 'nexttext': next_q_text}
        answer_list.append(answer_dict)
    question_dict = {
        'id': question.id, 
        'text': question.text, 
        'expl': question.expl, 
        'position': question.position,
        'tool': question.tool.id, 
        'result': question.result,
        'answers': answer_list
        }
    return question_dict

def check_user_or_403(user):
    if user != request.user:
        raise Http404('Not the right user')
    else:
        return 1


