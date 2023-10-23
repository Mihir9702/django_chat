from django.shortcuts import render, redirect
from .models import Room, Message
from django.http import HttpResponse, JsonResponse

# Create your views here.
def index(request):
		return render(request, 'index.html')

def room(request, room):
		username = request.GET.get('username')
		room_details = Room.objects.get(name=room)
		return render(request, 'room.html', { 'room': room, 'username': username, 'room_details': room_details })

def checkview(request):
		room = request.POST['room_name']
		username = request.POST['username']

		if Room.objects.filter(name=room).exists():
				return redirect('/' + room + '/?username=' + username)
		else:
				new_room = Room.objects.create(name=room)
				new_room.save()
				return redirect('/' + room + '/?username=' + username)

def send(request):
		username = request.POST['username']
		room_id = request.POST['room_id']
		message = request.POST['message']

		new_message = Message.objects.create(value=message, user=username, room=room_id)
		new_message.save()
		return HttpResponse('Message sent successfully')

def updateMessageValue(request):
    message = request.POST['message']
    message_id = request.POST['message_id']

    message_to_update = Message.objects.get(pk=message_id)
    message_to_update.value = message
    message_to_update.save()

    return HttpResponse('Message updated successfully')

def messages(request, room):
		room_details = Room.objects.get(name=room)
		messages = Message.objects.filter(room=room_details.id)
		return JsonResponse({ 'messages': list(messages.values()) })