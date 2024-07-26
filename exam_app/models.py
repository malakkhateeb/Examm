
from django.db import models
import bcrypt
import re
from django.core.exceptions import ObjectDoesNotExist

class UserManager(models.Manager):
    def basic_validator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['firstname']) < 2:
            errors["firstname"] = "First name should be at least 2 characters"
        if len(postData['lastname']) < 2:
            errors["lastname"] = "Last name should be at least 2 characters"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if  User.objects.filter(email=postData['email']).exists():
            errors['email'] = "Email already exists"
        if postData['password'] != postData['copassword']:
            errors['password_match'] = "Passwords do not match"
        if not EMAIL_REGEX.match(postData['email']):         
            errors['email'] = "Invalid email address!"
        return errors
    # add validations to the log in
    def basic_validatorlogin(self,postData):
            errors = {}
            try:
                user = User.objects.get(email=postData['email'])
            except ObjectDoesNotExist:
                errors['email'] = "Email not found."
                return errors
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors['password'] = "Invalid password."
            return errors
    def basic_validatorpie(self,postData):
        errors = {}
        if not  postData['name']:
            errors['name']="Please enter the name"
        if not  postData['filling']:
            errors['filling']="Please enter the filling"
        if not  postData['crust']:
            errors['crust']="Please enter the crust"
        return errors
    
class User(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    copassword = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return f"{self.firstname}"
    
class Pie(models.Model):
    name = models.CharField(max_length=255)
    filling = models.CharField(max_length=255)
    crust=models.CharField(max_length=255)
    made_by = models.ForeignKey(User, related_name="pie_made", on_delete=models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name="liked_pies")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
def add_regestraion(POST):
    password = bcrypt.hashpw(POST['password'].encode(), bcrypt.gensalt()).decode()
    copassword=bcrypt.hashpw(POST['copassword'].encode(), bcrypt.gensalt()).decode()
    registration = User.objects.create(
        firstname=POST['firstname'],
        lastname=POST['lastname'],
        email=POST['email'],
        password=password,
        copassword=copassword
    )
    return registration

def all_pies():
    return Pie.objects.all()

def all_users():
    return User.objects.all()

def get_pie_id(pie_id):
    return Pie.objects.get(id=pie_id)

def get_user_id(user_id):
    return User.objects.get(id=user_id)

def add_pies(request, POST):
        user = User.objects.get(id=request.session['user_id'])
        pie = Pie.objects.create(
            name=POST['name'],
            filling=POST['filling'],
            made_by=user
        )
        return pie

def update_pies(POST,pie_id):
    pie = Pie.objects.get(id=pie_id)
    pie.name =POST['name']
    pie.filling = POST['filling']
    pie.crust=POST['crust']
    pie.save()

def delete_pies(pie_id):
        book = Pie.objects.get(id=pie_id)
        book.delete()
