from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm, AddUserForm
from .models import Record
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache


# Create your views here.

def home(request):
    records = Record.objects.all()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Login Success')
            return redirect('home')
        else:
            messages.success(request, 'Login Failed, Please try again...')
            return redirect('home')
    else:
        return render(request, 'home.html', {'records':records})

def login_user(request):
    pass

def logout_user(request):
    logout(request)
    messages.success(request, 'Logout Success...')
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login

            # username = form.cleaned_data['username']
            # password = form.cleaned_data['password1']
            # user = authenticate(username=username, password=password)
            # login(request, user)
            messages.success(request, 'Registration Success')
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
    
    return render(request, 'register.html', {'form':form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        # look records
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    else:
        messages.success(request, 'You have to login')
        return redirect('home')
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, 'Record Deleted successfully')
        return redirect('home')
    else:
        messages.success(request, 'You have to login')
        return redirect('home')
    
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added...")
                return redirect('home')
        
        return render(request, 'add_record.html', {'form':form})
    else:
        messages.success(request, "Login Required")
        return redirect('home')
    
def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Successully Updated")
            return redirect('home')
        return render(request, 'update_record.html', {'form':form})
    else:
        messages.success(request, "Login Required")
        return redirect('home')
    
def logout_admin(request):
    if 'username' in request.session:
        request.session.flush()
        messages.info(request,'logout success')
    return redirect('dashboard')

def dashboard(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        admin = authenticate(username=username, password=password)
        if admin.is_superuser:
            request.session['username'] = username
            if request.session.get('username') == username:
                messages.success(request, 'Login Success')
                return redirect('adminpanel')
        else:
            messages.success(request, 'You are not an admin')
            return render(request, 'adminlogin.html')
        
    elif request.session.get('username'):
        return redirect('adminpanel')
    else:
        messages.success(request, "Logout Success")
        return render(request, 'adminlogin.html')
    
@never_cache
def adminpanel(request):
    if 'username' in request.session:
        users = User.objects.all()
        return render(request, 'adminpanel.html', {'users':users})
    return redirect('dashboard')
    
    


def update_user(request, pk):
    current_record = User.objects.get(pk=pk)
    form = AddUserForm(request.POST or None, instance=current_record)
    if form.is_valid():
        form.save()
        messages.success(request, "Record Successully Updated")
        return redirect('adminpanel')
    return render(request, 'update_record.html', {'form':form, 'users':current_record})

def delete_user(request, pk):
    delete_it = User.objects.get(pk=pk)
    delete_it.delete()
    messages.success(request, 'User Deleted successfully')
    return redirect('adminpanel')
