from django.shortcuts import render, redirect
from django.http import HttpRequest
from .models import Tracker
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def custom_logout(request):
    logout(request)
    return redirect('login')

# @login_required(login_url='login')
def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            return redirect('login')
    return render(request, "login.html")

def user_register(request):
    if request.method == "POST":
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            return render(request, 'register.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username is already taken'})

        user = User.objects.create_user(username=username, password=password1)

        login(request, user)

        # Redirect to the home page or any other desired page
        return redirect('home')
    return render(request, "register.html")

def history(request):
    if not request.user.is_authenticated:
        return redirect('login')
    quotes = Tracker.objects.filter(uname=request.user.username)
    income = 0
    expenses = 0
    for i in quotes:
        if i.cost>0:
            income+=i.cost
        else:
            expenses+=i.cost
    print(income, expenses)
    return render(request, "history.html", {"quotes": quotes, "income":income, "expenses":expenses, "net":income+expenses})

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    print(request.user)
    if request.method == "POST" and "income" in request.POST:
        print(request.POST)
        quote = request.POST['incomeSource']
        cost = request.POST['incomeAmount']
        new_income = Tracker(uname=request.user.username,quote=quote,cost=cost)
        new_income.save()
    elif request.method == "POST" and "expense" in request.POST:
        print(request.POST)
        quote = request.POST['expenseCategory']
        cost = request.POST['expenseAmount']
        cost = "-"+cost
        new_expense = Tracker(uname=request.user.username,quote=quote,cost=cost)
        new_expense.save()
    quotes = Tracker.objects.filter(uname=request.user.username)
    # for i in quotes:
    #     print(i.uname, i.cost)

    income = 0
    expenses = 0
    for i in quotes:
        if i.cost>0:
            income+=i.cost
        else:
            expenses+=i.cost
    expenses = -expenses
    # print(income, expenses)
    if income==0 and expenses==0:
        return render(request, "home.html")
    msg = "You are on Budget"
    if income<=expenses:
        msg = f"You are out of Budget by {expenses-income}"
    print()
    quotes = quotes[::-1][:5]

    return render(request, "home.html", {"quotes": quotes , "msg": msg})