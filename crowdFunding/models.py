from django.db import models


# Create your models here.
class myuser(models.Model):
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    Email = models.EmailField(max_length=30, unique=True)
    password=models.CharField(max_length=20)
    confirm_password=models.CharField(max_length=20, null=True)
    phone_number = models.CharField(max_length=11)
    profile_picture = models.ImageField(upload_to='images/', default='images/images.jpeg')
    is_active = models.BooleanField(default=False)
    country = models.CharField(max_length=20, null=True)
    birthdate = models.DateField(null=True)
    fb_account = models.URLField(null=True)

    def __str__(self):
        return self.Email
