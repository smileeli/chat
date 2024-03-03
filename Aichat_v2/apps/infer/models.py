from django.db import models

class Infer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    file = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    prompt = models.CharField(max_length=200)
    thread=models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200)
    result = models.CharField(max_length=200)
    class Meta:
        ordering = ['-create_time']

class Llmodel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

class Textname(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
class Thread(models.Model):
    id = models.AutoField(primary_key=True)
    num = models.CharField(max_length=200)

