from django.urls import path
from regelhulpify import views

urlpatterns = [
    path("", views.home, name="home"),
    path("alltools", views.alltools, name="alltools"),
    path("builder/", views.builder, name="builder"),
    path("builder/<int:tool>/", views.builder_tool, name="builder_tool"),
    path("builder/newtool/", views.newtool, name="newtool"),
    path("builder/<int:tool>/edit/", views.edittool, name="edittool"),
    path("builder/<int:tool>/newquestion/<int:result>/", views.newquestion, name="newquestion"),
    path("builder/<int:tool>/<int:question>/", views.builder_question, name="builder_question"),
    path("builder/<int:tool>/<int:question>/newanswer/", views.newanswer, name="newanswer"),
    path("builder/<int:tool>/<int:question>/newanswers/", views.newanswers, name="newanswers"),
    path("builder/<int:tool>/<int:question>/<int:answer>/", views.builder_answer, name="builder_answer"), 
    path("<int:tool>/", views.tool, name="tool"),
    path("<int:tool>/<int:question>/", views.question, name="question"),
    path("api/get_tools/", views.get_tools, name="get_tools"),
    path("api/get_complete_tool/<int:tool>/", views.get_complete_tool, name="get_complete_tool"),
    path("api/get_toolstart/<int:tool>/", views.get_toolstart, name="get_toolstart"),
    path("api/get_question/<int:question>/", views.get_question, name="get_question"),
    path("api/tool_delete/<int:tool>/", views.tool_delete, name="tool_delete"),
    path("api/question_move/<int:question>/<str:direction>/", views.question_move, name="question_move"),
    path("api/question_delete/<int:question>/", views.question_delete, name="question_delete"),
    path("api/answer_delete/<int:answer>/", views.answer_delete, name="answer_delete"), 
    path("api/answer_getnext/<int:question>/", views.answer_getnext, name="answer_getnext"), 
    path("api/answers_add/<int:question>/", views.answers_add, name="answers_add"), 
]