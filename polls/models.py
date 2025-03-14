from django.db import models

# Create your models here.


class Company(models.Model):
    company_name = models.CharField(max_length=200)
    region = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    company_size = models.IntegerField(max_length=200)
    revenue_size = models.IntegerField(max_length=200)
    history = models.BooleanField()
    website_url = models.URLField(max_length=200, null=True, blank=True)
    social_media = models.CharField(max_length=200)

class GenderChoices(models.TextChoices):
    MALE="male"
    FEMALE="female"
    OTHER="other"

class Client(models.Model):
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    gender = models.CharField(
        choices=GenderChoices.choices,
        max_length=30
    )
    email = models.EmailField(max_length=200)
    phone_number = models.CharField(max_length=200)  # (CharField: Symbols --> +57)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


class Interest(models.Model):
    interest_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    interest_name = models.CharField(max_length=200)


class Status(models.Model):
    status_choices = [
        ('AT', 'Attracted'),
        ('CO', 'Contacted'),
        ('QU', 'Qualified'),
        ('PS', 'Proposal Sent'),
        ('AS', 'Application Submitted'),
        ('WC', 'Won/Closed'),
    ]

    status = models.CharField(max_length=2, choices=status_choices)
    time = models.DateTimeField(auto_now=True)






