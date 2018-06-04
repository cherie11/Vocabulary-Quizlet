
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.


class CustomUserManager(BaseUserManager):   
    def create_user(self, username,email, password=None, **kwargs):
        # Ensure that an email address is set
        if not email:
            raise ValueError('Users must have a valid e-mail address')
        if not username:
            raise ValueError('Users must have a valid username')

        account = self.model(
            email=self.normalize_email(email),
            username=username,
            
        )
        account.set_password(password)  #Encrypt the plain text password
        account.save()
       
        return account

     #Only different is to set the is_admin=true
    def create_superuser(self,username, email, password=None, **kwargs):
    	account=self.create_user(username,email,password,**kwargs)
    	account.is_staff=True
    	account.is_superuser=True
    	account.save()
    	return account

    	
class CustomUser(AbstractUser):
    objects = CustomUserManager()

    username = models.CharField(unique=True,max_length=50)
    email = models.EmailField(unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']# removes email from REQUIRED_FIELDS
    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email