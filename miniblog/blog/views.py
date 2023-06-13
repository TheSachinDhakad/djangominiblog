from django.shortcuts import render , HttpResponseRedirect
from .forms import SignUpForm , LoginForm , PostForm
from django.contrib import messages
from django.contrib.auth import login , authenticate , logout
from .models import Post
from django.contrib.auth.models import Group
# Home page
def home(request):
    posts = Post.objects.all()
  
    return render(request, 'blog/home.html' , {'posts':posts})

def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    return render(request, 'blog/contact.html')


def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        # print(user.groups.all())
        return render(request, 'blog/dashboard.html' , {'posts':posts, 'full_name':full_name, 'gps':gps})

    else :
        return HttpResponseRedirect('/login/')
       

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request=request , data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                pword = form.cleaned_data['password']
                user = authenticate(username=uname , password=pword)
                if user is not None:
                    login(request , user)
                    messages.success(request , 'You logged in successfully')
                    return HttpResponseRedirect('/dashboard/')
        else :
            form = LoginForm()
        return render(request , 'blog/login.html' , {'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')
        
            
                
    
   

def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request , 'User signed up successfully')
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
          
    else:
        form = SignUpForm()
    
    return render(request, 'blog/signup.html', {'form': form})


def add_post(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form = PostForm(request.POST)
            if form.is_valid():
                titile = form.cleaned_data['titile']
                desc = form.cleaned_data['desc']
                pst = Post(titile = titile , desc = desc)
                pst.save()
                form = PostForm()
        else:
            form = PostForm()
        return render(request, 'blog/addpost.html' , {'form': form})
    else:
        return HttpResponseRedirect('/login/')
    
def update_post(request , pk):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=pk)
            form = PostForm(request.POST , instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi = Post.objects.get(pk=pk)
            form = PostForm(instance=pi)

        return render(request, 'blog/updatepost.html' , {'form': form})
    else:
        return HttpResponseRedirect('/login/')
def delete_post(request , pk):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=pk)
            pi.delete()
    
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')
       

        

    
    