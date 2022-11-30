from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator


gender_choices = (
        ("1", "Male"),
        ("2", "Female"),
        ("3", "Other"),
    )
re_gender_choices = (
    ("1", "Male"),
    ("2", "Female"),
    ("3", "Other"),
    ("4", "No preference"),
)


class SiteUser(AbstractUser):
    gender = models.CharField(choices=gender_choices, default=3, max_length=100)
    cleanliness = models.IntegerField(default=1, validators=[
        MaxValueValidator(10),
        MinValueValidator(1)])
    noise_level = models.IntegerField(default=1, validators=[
        MaxValueValidator(10),
        MinValueValidator(1)])
    is_student = models.BooleanField(default=False)
    re_gender = models.CharField(choices=re_gender_choices, default=4, max_length=100)
    wc_access = models.BooleanField(default=False)
    phone_number = models.DecimalField(default=0, decimal_places=0, max_digits=10)
    age = models.DecimalField(default=0, decimal_places=0, max_digits=2)
    budget = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    smoking = models.BooleanField(default=False)
    has_pet = models.BooleanField(default=False)
    picture = models.FileField(upload_to='user_img', default='user_img/default_pic.png')


class Property(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    property_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    picture = models.FileField(upload_to='property_img', default='property_img/default_pic.jpg', blank=True)
    description = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cleanliness = models.IntegerField(default=1, validators=[
            MaxValueValidator(10),
            MinValueValidator(1)])
    noise_level = models.IntegerField(default=1, validators=[
            MaxValueValidator(10),
            MinValueValidator(1)])
    wc_access = models.BooleanField(default=False)
    allows_smoking = models.BooleanField(default=False)
    allows_pets = models.BooleanField(default=False)
    gender = models.CharField(max_length=100)
    age = models.DecimalField(default=0, decimal_places=0, max_digits=2)

    def save(self, *args, **kwargs):
        self.gender = self.user.gender
        self.age = self.user.age
        super(Property, self).save(*args, **kwargs)  # Call the real save() method.


class Dislikes(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    user = models.ForeignKey(SiteUser, on_delete=models.CASCADE)


class Offer(models.Model):
    from_user = models.ForeignKey(SiteUser, related_name="sender", on_delete=models.CASCADE)
    sender_name = models.CharField(max_length=100)
    sender_num = models.DecimalField(default=0, decimal_places=0, max_digits=10)
    receiver = models.ForeignKey(SiteUser, related_name="receiver", on_delete=models.CASCADE)
    receiver_name = models.CharField(max_length=100)
    receiver_num = models.DecimalField(default=0, decimal_places=0, max_digits=10)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    p_id = models.IntegerField()
    property_name = models.CharField(max_length=100)
    is_read = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.receiver_name = self.receiver.username
        self.sender_name = self.from_user.username
        self.receiver_num = self.receiver.phone_number
        self.sender_num = self.from_user.phone_number
        self.p_id = self.property.id
        self.property_name = self.property.property_name
        super(Offer, self).save(*args, **kwargs)
