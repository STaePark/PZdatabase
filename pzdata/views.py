import re
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Food
import re
import bcrypt

def index(request):
    if not 'user_id' in request.session:
        context = {
            "whitelist": Food.objects.all()
        }
    else:
        this_user = User.objects.get(id = request.session['user_id'])
        favorite_foods = []
        for favorite_food in this_user.favorite_foods.all():
            favorite_foods.append(favorite_food.id)
        whitelist = Food.objects.exclude(id__in = favorite_foods)
        context = {
            "this_user": this_user,
            "foods": Food.objects.all(),
            "favorites": this_user.favorite_foods.all(),
            "whitelist": whitelist
        }
    return render(request, "index.html",context)

def favoriteFood(request,item_id):
    if 'user_id' not in request.session:
        return redirect('/')
    User.objects.get(id=request.session['user_id']).favorite_foods.add(Food.objects.get(id=item_id))
    return redirect('/')
def unfavoriteFood(request,item_id):
    if 'user_id' not in request.session:
        return redirect('/')
    User.objects.get(id=request.session['user_id']).favorite_foods.remove(Food.objects.get(id=item_id))
    return redirect('/')

def register(request):
    return render(request, "register.html")

def createUser(request):
    if request.method != "POST":
        return redirect('/register')
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/register')
    else:
        username=request.POST['username']
        isEditor=False
        password=request.POST['password']
        confirmPassword=''
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(username=username, isEditor=isEditor, password=pw_hash, confirmPassword=confirmPassword)

        request.session['user_id'] = new_user.id
        return redirect('/')

def new_item(request):
    return render(request, "new_item.html")

def new_item_create(request):
    if request.method != "POST":
        return redirect('/new-item')
    errors = Food.objects.food_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/new_item')
    else:
        name=request.POST['name']
        image=''
        perishable=request.POST['perishable']
        weight=request.POST['weight']
        hunger=request.POST['hunger']
        thirst=request.POST['thirst']
        boredom=request.POST['boredom']
        unhappiness=request.POST['unhappiness']
        description=request.POST['description']

        new_food = Food.objects.create(name=name, image=image,perishable=perishable,weight=weight,hunger=hunger,thirst=thirst,boredom=boredom,unhappiness=unhappiness,description=description)
        return redirect('/')

def edit_item(request, item_id):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        "item": Food.objects.get(id=item_id)
    }
    return render(request, "edit_item.html", context)

def update_item(request, item_id):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method != "POST":
        return redirect('/new-item')
    errors = Food.objects.food_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/edit_item')
    else:
        updated_item = Food.objects.get(id=item_id)

        updated_item.name=request.POST['name']
        updated_item.image=''
        updated_item.perishable=request.POST['perishable']
        updated_item.weight=request.POST['weight']
        updated_item.hunger=request.POST['hunger']
        updated_item.thirst=request.POST['thirst']
        updated_item.boredom=request.POST['boredom']
        updated_item.unhappiness=request.POST['unhappiness']
        updated_item.description=request.POST['description']
        updated_item.save()
        return redirect('/')




def login(request):
    
    if request.method != "POST":
        return redirect('/')
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        this_user = User.objects.filter(username = request.POST['loginUsername'])[0]
        request.session['user_id'] = this_user.id
        return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')
