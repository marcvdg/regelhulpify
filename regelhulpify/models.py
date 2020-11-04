from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tool(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1)
    name = models.CharField(max_length=128, unique=True)
    desc = models.CharField(max_length=1024)
    img = models.URLField(max_length=1024, null=True, blank=True)

    def __str__(self):
        """Regelhulp-beschrijving."""
        return f"{self.name} – {self.desc}"

class Question(models.Model):
    text = models.CharField(max_length=128)
    expl = models.CharField(max_length=256, blank=True)
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)
    position = models.IntegerField()
    result = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['tool', 'position'], name='unique position within tool')
        ]

    def __str__(self):
        """Vraagtext."""
        return f"{self.text}"

class Answer(models.Model):
    text = models.CharField(max_length=128)
    resulttext = models.CharField(max_length=256, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    nextquestion = models.ForeignKey(Question, on_delete=models.SET_DEFAULT, null=True, default="", blank=True, related_name='comesfrom')

    def __str__(self):
        """Vraagtext."""
        return f"{self.text}"