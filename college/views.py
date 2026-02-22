
from django.shortcuts import render, redirect
from .models import Course, Notice, Gallery, Admission, Enquiry

def home(request):
    return render(request, 'college/home.html', {
        'courses': Course.objects.all(),
        'notices': Notice.objects.all().order_by('-date')[:5],
        'gallery': Gallery.objects.all()[:8]
    })

def admission(request):
    if request.method == "POST":
        Admission.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            course=request.POST['course'],
            documents=request.FILES['documents']
        )
        return redirect('home')
    return render(request, 'college/admission.html')

def contact(request):
    if request.method == "POST":
        Enquiry.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            message=request.POST['message']
        )
        return redirect('home')
    return render(request, 'college/contact.html')
