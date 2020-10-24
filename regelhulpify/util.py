from regelhulpify.models import Tool, Question, Answer

def reset_tool(tool):
    '''Reset the positioning of a tool's questions'''
    t = get_object_or_404(Tool, id=tool)
    q = Question.objects.order_by('position', 'pk').filter(tool=t)
    p = 1
    for question in q:
        question.position = p
        question.save()
        print(question.position)
        p = p + 1
    return HttpResponse('Succes')  

def question_load_helper(question):
    ''' Util function that gets question and its answers based on id '''
    answer_list = []
    for answer in question.answer_set.all():
        next_q = ( answer.nextquestion.id if answer.nextquestion != None 
            else Question.objects.get(position=(question.position+1), tool=question.tool).id )
        answer_dict = {'id': answer.pk, 'text': answer.text, 'nextquestion': next_q}
        answer_list.append(answer_dict)
    question_dict = {
        'id': question.id, 
        'text': question.text, 
        'expl': question.expl, 
        'position': question.position,
        'tool': question.tool.id, 
        'answers': answer_list
        }
    return question_dict
