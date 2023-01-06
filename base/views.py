from django.shortcuts import render,redirect
from django.db.models import Q
from .models import Room,Topic,User,Message
from .forms import createRoom
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def home(request):
    q = request.GET.get('q') if request.GET.get('q') else ''
    topic = Topic.objects.all()
    rooms = Room.objects.filter(
        Q(topic__name__contains=q) | 
        Q(name__contains=q) | 
        Q(description__contains=q) | 
        Q(host__username__contains=q)
        )
    room_count = rooms.count()
    message_rooms = Message.objects.filter(
        Q(room__topic__name__icontains=q)
    )
    context = {'rooms':rooms,'topics':topic,'room_count':room_count,'message_rooms':message_rooms}
    return render(request, 'base/home.html',context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=  request.user,
            room=room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
    context = {'room':room,'room_messages':room_messages,'participants':participants}
    return render(request, 'base/room.html',context)

@login_required(login_url='login')
def profile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    message_rooms = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user,'rooms':rooms,'message_rooms':message_rooms,'topics':topics}
    return render(request, 'base/profile.html',context)

@login_required(login_url='login')
def create_rooms(request):
    form = createRoom()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            topic = topic,
            host=request.user,
            name = request.POST.get('name'),
            description=request.POST.get('description')
        )
        # form = createRoom(request.POST)
        # if form.is_valid():
        #     room = form.save()
        #     room.host = request.user
        #     room.save()

        return redirect('home')
    context = {'form':form,'idiot':topics}
    return render(request, 'base/create_rooms.html',context)

@login_required(login_url='login')
def update_room(request,pk):
    room = Room.objects.get(id=pk)
    form = createRoom(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('You are not allowed!')
    
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        room.topic = topic
        room.name = request.POST.get('name')
        room.description=request.POST.get('description')
        room.save()
        # form = createRoom(request.POST,instance=room)
        # if form.is_valid():
        #     form.save()
        return redirect('home')
    
    context = {'form':form,'topics':topics,'room':room}
    return render(request, 'base/create_rooms.html',context)

@login_required(login_url='login')
def delete_room(request,pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete_room.html',{'room':room})

def loginPage(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')
    context = {'page':page}
    return render(request, 'base/login_register.html',context)

def logoutPage(request):
    logout(request)
    return redirect('home')

def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        user = form.save(commit=False)
        user.username = user.username.lower()
        user.save()
        login(request, user)
        return redirect('home')
    else:
        messages.error(request, 'Invalid Registration')

    return render(request, 'base/login_register.html',{'form':form})

@login_required(login_url='login')
def delete_message(request,pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete_room.html',{'obj':message})
