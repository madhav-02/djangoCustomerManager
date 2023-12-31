from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Customer(models.Model):
    name = models.CharField(max_length=100)
    id = models.IntegerField(primary_key=True)
    
    def __str__(self):
        return self.name
    

class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.name 



# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()
    customers = models.ManyToManyField(Customer, related_name='users')

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)
