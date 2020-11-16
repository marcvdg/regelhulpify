from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Validator
def safe_url(value):
    forbidden = ['builder','admin', 'login', 'register']
    if value.isdigit():
        raise ValidationError(
            _('%(value)s bevat geen letters; gebruik er minstens één'),
            params={'value': value},
        )
    if value.lower() in forbidden:
        raise ValidationError(
            _('Je kunt "%(value)s" niet gebruiken als url. Probeer een ander woord. '),
            params={'value': value},
        )

# Create your models here.
class Tool(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1)
    name = models.CharField(max_length=128, unique=True)
    desc = models.CharField(max_length=1024)
    img = models.URLField(max_length=1024, null=True, blank=True)
    shorturl = models.SlugField(max_length=64, unique=True, null=True, blank=True, validators=[safe_url])

    def __str__(self):
        """Regelhulp-beschrijving."""
        return f"{self.name} – {self.desc}"

    def save(self, *args, **kwargs):
        """Saves slug as lowercase."""
        if self.shorturl:
            self.shorturl = self.shorturl.lower()
        return super(Tool, self).save(*args, **kwargs)    

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