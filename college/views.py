from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import Course, Notice, Gallery, Admission, Enquiry
from .forms import AdmissionForm


def home(request):
    return render(
        request,
        "college/home.html",
        {
            "courses": Course.objects.all(),
            "notices": Notice.objects.all().order_by("-date")[:5],
            "gallery": Gallery.objects.all()[:8],
        },
    )


def admission(request):
    if request.method == "POST":
        form = AdmissionForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the admission
            admission = form.save()

            # Prepare email content
            subject = f"New Admission Application - {admission.name}"
            message = f"""
New Admission Application Received!

Student Details:
Name: {admission.name}
Email: {admission.email}
Phone: {admission.phone}
Course: {admission.course}

Additional Information:
Father Name: {request.POST.get('father_name', '')}
Date of Birth: {request.POST.get('date_of_birth', '')}
Address: {request.POST.get('address_line1', '')}, {request.POST.get('city', '')}
Pincode: {request.POST.get('pincode', '')}

Please check the admin panel for complete details and documents.
"""

            # Send email notification
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    ["cmsnnursing@gmail.com"],  # Replace with your email
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Email sending failed: {e}")

            # WhatsApp message (opens WhatsApp with pre-filled message)
            whatsapp_message = f"New Admission Application from {admission.name} for {admission.course}. Email: {admission.email}, Phone: {admission.phone}"
            whatsapp_url = f"https://wa.me/918948274515?text={whatsapp_message.replace(' ', '%20')}"

            messages.success(
                request,
                "Your admission application has been submitted successfully! We will contact you soon.",
            )
            return render(
                request,
                "college/admission_success.html",
                {"admission": admission, "whatsapp_url": whatsapp_url},
            )
    else:
        form = AdmissionForm()

    return render(
        request,
        "college/admission.html",
        {"form": form, "courses": Course.objects.all()},
    )


def contact(request):
    if request.method == "POST":
        Enquiry.objects.create(
            name=request.POST["name"],
            email=request.POST["email"],
            phone=request.POST["phone"],
            message=request.POST["message"],
        )
        messages.success(request, "Your message has been sent successfully!")
        return redirect("home")
    return render(request, "college/contact.html")
