from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count, Prefetch
from django.utils import timezone
from .models import Event, Category
from .forms import EventForm, ParticipantForm, CategoryForm, CustomUserCreationForm, EditProfileForm
from .forms import SignupForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, User
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render, HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from .models import Event
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        # Notice we use 'profile_image' NOT 'profile_picture'
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'profile_image']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}),
            'profile_image': forms.FileInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}),
        }

User = get_user_model()

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()

def is_participant(user):
    return user.is_authenticated and user.is_participant

@login_required(login_url='login')
def home(request):
    return render(request, 'events/home.html')


@login_required(login_url='login')
@user_passes_test(lambda u: u.groups.filter(name='Organizer').exists() or u.groups.filter(name='Admin').exists())
def dashboard(request):
    today = timezone.localdate()

    total_events = Event.objects.count()
    upcoming_events = Event.objects.filter(date__gte=today).count()
    past_events = Event.objects.filter(date__lt=today).count()
    participant_group = Group.objects.get(name='Participant')
    total_participants = User.objects.filter(groups=participant_group).count()

    todays_events = Event.objects.filter(date=today)

    filter_type = request.GET.get('filter', 'today')  

    if filter_type == 'total':
        events_list = Event.objects.all()
    elif filter_type == 'upcoming':
        events_list = Event.objects.filter(date__gte=today)
    elif filter_type == 'past':
        events_list = Event.objects.filter(date__lt=today)
    else:  
        events_list = todays_events

    context = {
        'total_events': total_events,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'total_participants': total_participants,
        'todays_events': todays_events,
        'events_list': events_list,
        'filter_type': filter_type,
    }
    return render(request, 'events/dashboard.html', context)

@login_required(login_url='login')

@user_passes_test(lambda u: u.groups.filter(name='Organizer').exists() or u.groups.filter(name='Admin').exists() or u.groups.filter(name='Participant').exists())
def event_list(request):
    categories = Category.objects.all()

   
    events = Event.objects.select_related('category').prefetch_related('participants')

  
    query = request.GET.get('q')
    if query:
        events = events.filter(Q(name__icontains=query) | Q(location__icontains=query))

    category_id = request.GET.get('category')
    if category_id:
        events = events.filter(category_id=category_id)


    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date:
        events = events.filter(date__gte=start_date)
    if end_date:
        events = events.filter(date__lte=end_date)
    participant_group = Group.objects.get(name='Participant')
    total_participants = User.objects.filter(groups=participant_group).count()

    return render(request, 'events/event_list.html', {
        'events': events,
        'categories': categories,
        'total_participants': total_participants
    })

@login_required(login_url='login')
@user_passes_test(lambda u: u.groups.filter(name='Organizer').exists() or u.groups.filter(name='Admin').exists())
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form})


@login_required(login_url='login')
@user_passes_test(lambda u: u.groups.filter(name='Organizer').exists() or u.groups.filter(name='Admin').exists())
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form})

@login_required(login_url='login')
@user_passes_test(lambda u: u.groups.filter(name='Organizer').exists() or u.groups.filter(name='Admin').exists())
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'events/event_confirm_delete.html', {'object': event})




@login_required(login_url='login')
@user_passes_test(lambda u: u.groups.filter(name='Organizer').exists() or u.groups.filter(name='Admin').exists())
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'events/category_list.html', {'categories': categories})


@login_required(login_url='login')
@user_passes_test(lambda u: u.groups.filter(name='Organizer').exists() or u.groups.filter(name='Admin').exists())
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'events/category_form.html', {'form': form})



@login_required(login_url='login')
@user_passes_test(lambda u: u.groups.filter(name='Organizer').exists() or u.groups.filter(name='Admin').exists())
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'events/category_form.html', {'form': form})



@login_required(login_url='login')
@user_passes_test(lambda u: u.groups.filter(name='Organizer').exists() or u.groups.filter(name='Admin').exists())
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'events/category_confirm_delete.html', {'object': category})



@login_required
@user_passes_test(is_admin)
def participant_list(request):
    participant_group = Group.objects.get(name='Participant')
    participants = User.objects.filter(groups=participant_group)

    # Optional search
    q = request.GET.get('q')
    if q:
        participants = participants.filter(
            username__icontains=q
        ) | participants.filter(
            email__icontains=q
        )

    total_participants = participants.count()
    return render(request, 'events/participant_list.html', {
        'participants': participants,
        'total_participants': total_participants
    })
@login_required
@user_passes_test(is_admin)
def participant_delete(request, pk):
    participant = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        participant.delete()
        return redirect('participant_list')

    return render(request, 'events/participant_confirm_delete.html', {'participant': participant})
@login_required
@user_passes_test(is_admin)
def participant_create(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            # Create the user
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password=form.cleaned_data['password']
            )

            # Add to Participant group
            participant_group, created = Group.objects.get_or_create(name='Participant')
            user.groups.add(participant_group)

            # Assign selected events
            events = form.cleaned_data['events']
            user.events.set(events)

            return redirect('participant_list')
    else:
        form = ParticipantForm()
    
    return render(request, 'events/participant_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def assign_events_to_participant(request):
    if request.method == "POST":
        form = ParticipantForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            events = form.cleaned_data['events']
            # Clear old events and assign new ones
            for event in Event.objects.all():
                event.participants.remove(user)  # optional if you track ManyToMany
            for event in events:
                event.participants.add(user)
            return redirect('participant_list')
    else:
        form = ParticipantForm()
    return render(request, 'events/participant_form.html', {'form': form}) 

@login_required(login_url='login')
def participant_dashboard(request):
    user = request.user
    rsvped_events = user.rsvped_events.all()  # all events this user RSVPed to
    return render(request, 'events/participant_dashboard.html', {'rsvped_events': rsvped_events})

from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False # Deactivate account until email is confirmed
            user.save()


            participant_group, created = Group.objects.get_or_create(name='Participant')
            user.groups.add(participant_group)


            # --- Activation Email Logic ---
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('events/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            
            # This is what prints to your terminal
            send_mail(mail_subject, message, 'admin@event.com', [to_email])
            
            return render(request, 'events/activation_sent.html')
    else:
        form = CustomUserCreationForm()
    return render(request, 'events/signup.html', {'form': form})

def activate_account(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)


        valid = default_token_generator.check_token(user, token)
        

        if valid:
            user.is_active = True
            user.save()
            return redirect('login')
        else:
            return HttpResponse('Invalid activation link')

    except User.DoesNotExist:
        return HttpResponse('User not found')


from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return render(request, 'events/activation_failed.html')
    

def user_login(request):
    error = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if not user.is_active:
                error = "Please activate your account first."
            else:
                # REMOVED: UserProfile get_or_create line (It's no longer needed!)
                login(request, user)

                if user.groups.filter(name="Admin").exists():
                    return redirect("admin_dashboard")
                elif user.groups.filter(name="Organizer").exists():
                    return redirect("organizer_dashboard")
                else:
                    return redirect("participant_dashboard")
        else:
            error = "Invalid username or password."

    return render(request, "events/login.html", {"error": error})

def user_logout(request):
    logout(request)
    return redirect("login")

from django.contrib.auth.decorators import login_required
from .models import Event


@login_required
def admin_dashboard(request):

    events = Event.objects.all()
    participants = User.objects.all()
    categories = Category.objects.all()

    return render(request, "events/admin_dashboard.html", {
        "events": events,
        "participants": participants,
        "categories": categories
    })


@login_required
def organizer_dashboard(request):

    events = Event.objects.all()
    categories = Category.objects.all()

    return render(request, "events/organizer_dashboard.html", {
        "events": events,
        "categories": categories
    })


from django.contrib.auth.decorators import login_required

@login_required
def participant_dashboard(request):
    rsvped_events = request.user.rsvped_events.all()

    return render(
        request,
        "events/participant_dashboard.html",
        {"rsvped_events": rsvped_events},
    )

@login_required(login_url='login')
def rsvp_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    # Use the related_name you defined: 'rsvped_events'
    if event.participants.filter(id=request.user.id).exists():
        event.participants.remove(request.user)
    else:
        event.participants.add(request.user)
        
    return redirect('event_list')


class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'  
    context_object_name = 'events'   
    
class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

from .forms import EventForm

class EventCreateView(CreateView):
    model = Event
    form_class = EventForm # Use form_class instead of fields
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('event_list')

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        return super().form_valid(form)


from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView, DeleteView, CreateView

# --- EXAMPLE: EVENT EDIT (Admin Only) ---
class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    fields = '__all__'
    
    def test_func(self):
        # Admin > Everything
        return self.request.user.is_superuser or self.request.user.is_admin

# --- EXAMPLE: CATEGORY EDIT (Admin & Organizer) ---
class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    fields = '__all__'
    
    def test_func(self):
        # Admin or Organizer can edit categories
        user = self.request.user
        return user.is_superuser or user.is_admin or user.is_organizer
    
class ProfileDetailView(DetailView):
    model = settings.AUTH_USER_MODEL
    template_name = 'events/profile_detail.html'
    context_object_name = 'user_profile' 

    def get_object(self):
        return self.request.user
    


class ProfileUpdateView(UpdateView):
    model = User
    
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'profile_image']
    template_name = 'events/profile_form.html'
    success_url = reverse_lazy('profile_detail')

    def get_object(self):
        
        return self.request.user