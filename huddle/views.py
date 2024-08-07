from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Huddle
from .forms import ItemForm
from .utilities import notify_users

# Create your views here.
def index(request):
    return render(request, 'huddle/index.html')

def huddle(request):
    # Get info
    key = request.GET.get('key', '')
    user = request.GET.get('user', '')
    
    huddle, created = Huddle.objects.get_or_create(key=key)
    
    if created:
        messages.success(request, 'The huddle was created')
        
    # if form submitted
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.huddle = huddle
            item.save()
            
            notify_users(huddle, item.user)
            
            return redirect(f'/huddle?key={key}&user={user}')
    
    return render(request, 'huddle/huddle.html', {'user': user, 'huddle':huddle})