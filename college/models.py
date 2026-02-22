
from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=200)
    duration = models.CharField(max_length=100)
    eligibility = models.TextField()
    description = models.TextField()
    seats = models.IntegerField(default=0)
    fees = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Notice(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='notices/', blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

class Gallery(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/')

    def __str__(self):
        return self.title

class Admission(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    course = models.CharField(max_length=200)
    documents = models.FileField(upload_to='admissions/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Enquiry(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
