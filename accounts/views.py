from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.views.generic import CreateView
from .form import ClientSignUpForm, LawyerSignUpForm, MessageForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Lawyer, Client, Message, Conversation


def register(request):
    return render(request, '../templates/register.html')


def base(request):
    return render(request, 'base.html')


def main(request):
    lawyer = request.user.lawyer
    return render(request, 'lawyerhome.html', context={'lawyer': lawyer})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Conversation, Message

from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def clienthome(request):
    lawyers = Lawyer.objects.all()

    # Get the client user

    client_user = request.user

    # Filter conversations where the client is a participant
    conversations = Conversation.objects.filter(participants=client_user)

    # Create a dictionary to hold participants' names in conversations
    participants_names = {}

    for conversation in conversations:
        # Get all participants in the conversation
        participants = conversation.participants.all()

        # Exclude the current client user from participants and get the lawyer user
        lawyer_user = participants.exclude(id=client_user.id).first()

        # Store the lawyer user's name in the dictionary using conversation ID as the key
        participants_names[conversation.id] = lawyer_user.username if lawyer_user else None

    return render(request, 'clienthome.html',
                  {'conversations': conversations, 'participants_names': participants_names, 'client_user': client_user,
                   'lawyers': lawyers})


class client_register(CreateView):
    model = User
    form_class = ClientSignUpForm
    template_name = '../templates/client_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('clienthome')


class lawyer_register(CreateView):
    model = User
    form_class = LawyerSignUpForm
    template_name = '../templates/lawyer_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('lawhome')


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_lawyer:
                login(request, user)
                return redirect('lawhome')
            elif user is not None and user.is_client:
                login(request, user)
                return redirect('clienthome')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, '../templates/login.html',
                  context={'form': AuthenticationForm()})


def logout_view(request):
    logout(request)
    return redirect('/')


def LawyerDetail(request, pk):
    lawyer = Lawyer.objects.get(id=pk)

    return render(request, 'lawyerdetail.html', context={"lawyer": lawyer})


@login_required(login_url='login')
def lawyer_messages(request):
    lawyer_user = request.user


    # Get all conversations involving the lawyer user
    conversations = Conversation.objects.filter(participants=lawyer_user)

    # Create a list of tuples with conversation objects, client usernames, and messages
    conversation_data = []

    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)  # Add request.FILES for handling files
        if form.is_valid():
            content = form.cleaned_data['content']
            file = form.cleaned_data['file']

            # Check if the conversation already exists or create a new one
            conversation_id = request.POST.get('conversation_id')
            if conversation_id:
                conversation = get_object_or_404(Conversation, id=conversation_id)
            else:
                conversation = Conversation.objects.create()
                conversation.participants.add(lawyer_user)
                conversation_id = conversation.id

            # Create a new message for the conversation
            message = Message.objects.create(conversation=conversation, sender=lawyer_user, content=content)

            # Handle file upload (if any)
            if file:
                message.file = file
                message.save()

            # Redirect back to the same page after sending the message
            return redirect('lawyer_messages')

    else:
        form = MessageForm()

    for conversation in conversations:
        # Get the participants in the conversation
        participants = conversation.participants.all()

        # Exclude the lawyer from participants to get the client user(s)
        client_users = participants.exclude(id=lawyer_user.id)

        client_usernames = ', '.join([user.username for user in client_users])

        # Append the tuple (conversation, client_users, messages) to the conversation_data list
        messages = Message.objects.filter(conversation=conversation).order_by('timestamp')
        conversation_data.append((conversation, client_users, messages))

    return render(request, 'lawyer_message.html', {'conversation_data': conversation_data, 'form': form ,'client_usernames':client_usernames})




@login_required(login_url='login')
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    messages = conversation.message_set.all()

    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            sender = request.user
            content = form.cleaned_data['content']
            file_upload = form.cleaned_data['file_upload']

            # Create the message and save it
            message = Message(conversation=conversation, sender=sender, content=content, file_upload=file_upload)
            message.save()

            return redirect('conversation_detail', conversation_id=conversation_id)
    else:
        form = MessageForm()

    return render(request, 'coversation_detail.html',
                  {'conversation': conversation, 'messages': messages, 'form': form})


@login_required
@login_required
def reply_message(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)

    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            sender = request.user
            content = form.cleaned_data['content']
            file_upload = form.cleaned_data.get('file')  # Use get() instead of index access to avoid KeyError

            # Create the reply message and save it
            message = Message(conversation=conversation, sender=sender, content=content, file_upload=file_upload)
            message.save()

            return redirect('lawyer_messages')
    else:
        form = MessageForm()

    return render(request, 'reply_message.html', {'form': form, 'conversation': conversation})




@login_required(login_url='login')
def client_messages(request):
    client_user = request.user

    # Get all conversations involving the client user
    conversations = Conversation.objects.filter(participants=client_user)

    # Create a list of tuples with conversation objects and lawyer usernames
    conversation_data = []

    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)  # Add request.FILES for handling files
        if form.is_valid():
            conversation_id = form.cleaned_data['conversation_id']
            content = form.cleaned_data['content']

            # Get the conversation by ID
            conversation = get_object_or_404(Conversation, id=conversation_id)

            # Create a new message for the conversation
            message = Message.objects.create(conversation=conversation, sender=client_user, content=content)

            # Handle file upload (if any)
            file = form.cleaned_data['file']
            if file:
                message.file = file
                message.save()

            # Redirect back to the same page after sending the message
            return redirect('client_messages')

    else:
        form = MessageForm()

    for conversation in conversations:
        # Get the participants in the conversation
        participants = conversation.participants.all()

        # Exclude the client from participants to get the lawyer user
        lawyer_user = participants.exclude(id=client_user.id).first()

        # Ensure that the conversation involves the current client_user only
        if lawyer_user:
            conversation_data.append((conversation, lawyer_user.username))

    return render(request, 'client_messages.html', {'conversation_data': conversation_data, 'form': form})



# views.py



@login_required
def send_message(request, receiver_id, conversation_id=None):
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            sender = request.user
            receiver = get_object_or_404(User, id=receiver_id)

            # Check if a conversation between the sender and receiver already exists
            if conversation_id:
                conversation = get_object_or_404(Conversation, id=conversation_id)
            else:
                conversation = Conversation.objects.filter(participants=sender).filter(participants=receiver).first()

                if not conversation:
                    # If conversation does not exist, create a new one
                    conversation = Conversation.objects.create()
                    conversation.participants.add(sender)
                    conversation.participants.add(receiver)

            content = form.cleaned_data['content']
            file = form.cleaned_data['file']  # Use 'file' instead of 'file_upload'

            # Create the message and save it
            message = Message(conversation=conversation, sender=sender, content=content, file=file)  # Use 'file' here as well
            message.save()

            return redirect('lawyer_messages')
    else:
        form = MessageForm()

    return render(request, 'send_message.html', {'form': form})


