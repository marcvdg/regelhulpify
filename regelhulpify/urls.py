from django.urls import path
from regelhulpify import views

urlpatterns = [
    path("", views.home, name="home"),
    path("builder/", views.builder, name="builder"),
    path("builder/<int:tool>", views.builder_tool, name="builder_tool"),
    path("builder/newtool", views.newtool, name="newtool"),
    path("builder/<int:tool>/newquestion", views.newquestion, name="newquestion"),
    path("builder/<int:tool>/<int:question>", views.builder_question, name="builder_question"),
    path("builder/<int:tool>/<int:question>/newanswer", views.newanswer, name="newanswer"),
    path("builder/<int:tool>/<int:question>/<int:answer>", views.builder_answer, name="builder_answer"),
    path("<int:tool>", views.tool, name="tool"),
    path("<int:tool>/<int:question>", views.question, name="question"),
]