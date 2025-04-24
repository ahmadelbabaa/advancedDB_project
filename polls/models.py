from django.db import models

# Organization
class Organization(models.Model):
    organization_name = models.CharField(max_length=200)
    type_of_organization = models.CharField(max_length=200, null=True, blank=True)
    country_of_operation = models.CharField(max_length=200, null=True, blank=True)
    organization_size = models.IntegerField()
    revenue_size = models.IntegerField()
    website_url = models.URLField(max_length=200, null=True, blank=True)
    social_media = models.CharField(max_length=200)

    def __str__(self):
        return self.organization_name


# Gender
class GenderChoices(models.TextChoices):
    MALE = "male", "Male"
    FEMALE = "female", "Female"
    OTHER = "other", "Other"


# Client
class Client(models.Model):
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    gender = models.CharField(
        choices=GenderChoices.choices,
        max_length=30
    )
    email = models.EmailField(max_length=200)
    phone_number = models.CharField(max_length=200)  # For symbols like +57
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Sector
class Sector(models.Model):
    class SectorChoices(models.TextChoices):
        TOURISM = "tourism", "Tourism"
        CULTURE = "culture", "Culture"
        SUSTAINABILITY = "sustainability", "Sustainability"
        EDUCATION = "education", "Education"

    sector_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    sector = models.CharField(max_length=50, choices=SectorChoices.choices)

    def __str__(self):
        return self.sector


# Status
class Status(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    status_choices = [
        ('AT', 'Attracted'),
        ('CO', 'Contacted'),
        ('IT', 'Interested'),
        ('QU', 'Qualified'),
        ('RS', 'Registered'),
        ('AS', 'Call Application Submitted'),
    ]

    status = models.CharField(max_length=2, choices=status_choices)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return dict(self.status_choices).get(self.status, self.status)

    class Meta:
        verbose_name_plural = "Statuses"

