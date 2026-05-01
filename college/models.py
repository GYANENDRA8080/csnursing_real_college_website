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
    file = models.FileField(upload_to="notices/", blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Gallery(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="gallery/")

    def __str__(self):
        return self.title


class Admission(models.Model):
    # Personal Information
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=True, blank=True)
    sex = models.CharField(
        max_length=10,
        choices=[("male", "Male"), ("female", "Female")],
        default="female",
    )

    # Family Information
    father_name = models.CharField(max_length=200, default="")
    mother_name = models.CharField(max_length=200, blank=True, default="")
    father_occupation = models.CharField(max_length=200, blank=True, default="")
    mother_occupation = models.CharField(max_length=200, blank=True, default="")

    # Address Information
    address_line1 = models.CharField(max_length=500, default="")
    address_line2 = models.CharField(max_length=500, blank=True, default="")
    city = models.CharField(max_length=100, default="")
    pincode = models.CharField(max_length=6, default="")

    # Academic & Other Information
    course = models.CharField(max_length=200)
    category = models.CharField(
        max_length=20,
        choices=[("GENERAL", "General"), ("SC", "SC"), ("ST", "ST"), ("OBC", "OBC")],
        default="GENERAL",
    )
    nationality = models.CharField(max_length=100, default="Indian")
    religion = models.CharField(max_length=100, blank=True, default="")
    caste = models.CharField(max_length=100, blank=True, default="")
    language = models.CharField(max_length=100, blank=True, default="")
    height = models.CharField(max_length=10, blank=True, default="")
    weight = models.IntegerField(blank=True, null=True)
    marital_status = models.CharField(
        max_length=20,
        choices=[("unmarried", "Unmarried"), ("married", "Married")],
        blank=True,
        default="unmarried",
    )

    # Documents
    documents = models.FileField(upload_to="admissions/")

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.course}"


class Enquiry(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
