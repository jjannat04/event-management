from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count, Prefetch
from django.utils import timezone
from .models import Event, Participant, Category
from .forms import EventForm, ParticipantForm, CategoryForm

def home(request):
    return render(request, 'events/home.html')

def dashboard(request):
    today = timezone.localdate()

    total_events = Event.objects.count()
    upcoming_events = Event.objects.filter(date__gte=today).count()
    past_events = Event.objects.filter(date__lt=today).count()
    total_participants = Participant.objects.count()

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
    total_participants = Participant.objects.distinct().count()

    return render(request, 'events/event_list.html', {
        'events': events,
        'categories': categories,
        'total_participants': total_participants
    })

def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form})


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


def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'events/event_confirm_delete.html', {'object': event})


def participant_list(request):
    q = request.GET.get('q', '')

    participants = Participant.objects.prefetch_related(
        Prefetch('events', queryset=Event.objects.select_related('category'))
    )

    if q:
        participants = participants.filter(name__icontains=q) | participants.filter(email__icontains=q)

    return render(request, 'events/participant_list.html', {'participants': participants})

def participant_create(request):
    if request.method == "POST":
        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save()  
            return redirect('participant_list')
    else:
        form = ParticipantForm()
    return render(request, 'events/participant_form.html', {'form': form})
def participant_update(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == "POST":
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            participant = form.save()
            form.save_m2m()  
            return redirect('participant_list')
    else:
        form = ParticipantForm(instance=participant)
    return render(request, 'events/participant_form.html', {'form': form})

def participant_delete(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        participant.delete()
        return redirect('participant_list')
    return render(request, 'events/participant_confirm_delete.html', {'object': participant})


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'events/category_list.html', {'categories': categories})


def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'events/category_form.html', {'form': form})


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


def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'events/category_confirm_delete.html', {'object': category})