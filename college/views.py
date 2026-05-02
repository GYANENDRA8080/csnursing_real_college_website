import re
import time
from urllib.parse import urljoin
from urllib.request import Request, urlopen

from django.db.utils import OperationalError
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import Course, Notice, Gallery, Admission, Enquiry
from .forms import AdmissionForm

_NOTICE_CACHE = {
    "timestamp": 0,
    "data": [],
}


def fetch_upsmfac_notices(limit=5, cache_seconds=900):
    if time.time() - _NOTICE_CACHE["timestamp"] < cache_seconds:
        return _NOTICE_CACHE["data"]

    url = "https://upsmfac.org/en/news"
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="ignore")

        table_match = re.search(
            r'<table[^>]+id=["\']ContentPlaceHolder_Body_gdvNewsContent["\'][^>]*>(.*?)</table>',
            html,
            re.IGNORECASE | re.DOTALL,
        )
        notices = []
        if table_match:
            table_html = table_match.group(1)
            for row in re.findall(
                r"<tr>(.*?)</tr>", table_html, re.IGNORECASE | re.DOTALL
            ):
                link_match = re.search(
                    r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>.*?<span[^>]*>(.*?)</span>',
                    row,
                    re.IGNORECASE | re.DOTALL,
                )
                if not link_match:
                    continue
                href = link_match.group(1).strip()
                title = re.sub(r"<[^>]+>", "", link_match.group(2)).strip()
                if not title:
                    continue
                href = urljoin(url, href)
                notices.append({"title": title, "url": href})
                if len(notices) >= limit:
                    break

        _NOTICE_CACHE["timestamp"] = time.time()
        _NOTICE_CACHE["data"] = notices
        return notices
    except Exception as e:
        print("UPSMFAC news fetch failed:", e)
        return []


def _safe_list(queryset):
    try:
        return list(queryset)
    except OperationalError as e:
        print("Database query failed:", e)
        return []


def home(request):
    return render(
        request,
        "college/home.html",
        {
            "courses": _safe_list(Course.objects.all()),
            "notices": _safe_list(Notice.objects.all().order_by("-date")[:5]),
            "external_notices": fetch_upsmfac_notices(),
            "gallery": _safe_list(Gallery.objects.all()[:8]),
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
