from django.shortcuts import render, redirect
from chat.models import Room, Message
from django.http import HttpResponse, JsonResponse

# Create your views here.
def home(request):
    return render(request, 'home.html')  

def room(request, room): 
    username = request.GET.get('username') 
    room_details = Room.objects.get(name=room) 
    return render(request, 'room.html', {
        'username': username,  
        'room': room,
        'room_details': room_details
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.user.username
    passw = request.POST.get('password')  # Use get() method to avoid MultiValueDictKeyError
    if Room.objects.filter(name=room, password=passw).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        return createRoom(request)

def createRoom(request):
    room_name = request.POST['room_name']
    passw = request.POST.get('password')  # Use get() method to avoid MultiValueDictKeyError

    if Room.objects.filter(name=room_name).exists():
        return HttpResponse('Room already exists')
    else:
        chat_room = Room.objects.create(name=room_name, password=passw)
        chat_room.save()
        return checkview(request)
    
def send(request):
    message = request.POST['message']
    username = request.user.username
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})