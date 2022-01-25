from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData['username']) < 3:
            errors['username'] = "Username should be longer than 2 characters!"
        for user in User.objects.all():
            if user.username == postData['username']:
                errors['username'] = "Username already exists!"
                break
        if len(postData['password']) < 4:
            errors['password'] = "Password should be longer than 3 characters!"
        if postData['confirmPassword'] != postData['password']:
            errors['confirmPassword'] = "Passwords do not match!"
        return errors

    def login_validator(self, postData):
        errors = {}
        if len(User.objects.filter(username = postData['loginUsername'])) < 1:
            errors['noUser'] = "Account does not exist!"
        else:
            input_user = User.objects.filter(username = postData['loginUsername'])[0]

            
            if len(postData['loginUsername']) < 1:
                errors['loginUsername'] = "Please enter a username"
            if len(postData['loginPassword']) < 1:
                errors["loginPassword"] = "Please enter a password"
            if not bcrypt.checkpw(postData['loginPassword'].encode(), input_user.password.encode()):
                errors["mismatch"] = "Incorrect password"
        return errors

class User(models.Model):
    username = models.CharField(max_length=40)
    isEditor = models.BooleanField()
    password = models.CharField(max_length=40)
    confirmPassword = models.CharField(max_length=40)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class FoodManager(models.Manager):
    def food_validator(self, postData):
        errors = {}
        if len(postData['name']) < 3:
            errors['name'] = "Names should be longer than 2 characters!"
        for food in Food.objects.all():
            if food.name == postData['name']:
                errors['name'] = "This item already exists!"
                break
        return errors
    def food_update_validator(self, postData, item_id):
        errors = {}
        if len(postData['name']) < 3:
            errors['name'] = "Names should be longer than 2 characters!"
        foods = Food.objects.exclude(id=item_id)
        for food in foods:
            if food.name == postData['name']:
                errors['name'] = "This item already exists!"
                break
        return errors

class Food(models.Model):
    name = models.CharField(max_length=40)
    image = models.CharField(max_length=40)
    perishable = models.BooleanField()
    weight = models.FloatField()
    hunger = models.IntegerField()
    thirst = models.IntegerField()
    boredom = models.IntegerField()
    unhappiness = models.IntegerField()
    description = models.TextField()

    favoriters = models.ManyToManyField(User, related_name="favorite_foods")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = FoodManager()