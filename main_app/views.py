import profile
from django.shortcuts import render, redirect


from .models import Image, Board
from .forms import UpdateProfileForm, UpdateUserForm

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from main_app.models import Board, User, Profile

# Create your views here.
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth import login
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin
# Define the home view:
def home(request):

  return render(request, 'home.html')

# Define about view:
def about(request):
  return render(request, 'about.html')

     # image views
class ImageCreate(CreateView):
    model = Image
    fields = ['img', 'subject', 'description', ] # All fields mentioned in models.py file
    success_url = '/images/'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ImageUpdate(UpdateView):
    model = Image
    fields = ['img', 'subject', 'description', ]
class ImageDelete(DeleteView):
    model = Image
    success_url = 'images/index.html/'


# def image_Index(request):
   
#     return render(request, 'images/index.html')
def image_Index(request):
    images = Image.objects.filter()
    return render(request, 'images/index.html', { 'images': images})

def images_detail(request, image_id):
    # SELECT * FROM main_app_image WHERE id = image_id
    image = Image.objects.get(id = image_id)

def add_to_board(request, image_id):
    return redirect('detail', image_id = image_id)

# User Profile views:

# READ with UPDATE form
def profile_detail(request, user_id):
    user = User.objects.get(id = user_id)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile_detail', user_id = user_id)

    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user)
        profile_form.fields['user_bio'].initial = user.profile.user_bio
        profile_form.fields['user_profile_pic'].initial = user.profile.user_profile_pic

    return render(request, 'profiles/detail.html', {'user': user, 'user_form': user_form, 'profile_form': profile_form})


# DELETE - not working
# relation "main_app_board" does not exist
# def profile_delete(request, user_id):
#     user = User.objects.get(id = user_id)
#     user.delete()
#     return render('about')


    # authenitcation views
def signup(request):
    error_message = ""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('about') # change this once index or profile is added
        else:
            error_message = "Invalid signup - Please try again later"
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message }
    return render(request, 'registration/signup.html', context)


class BoardCreate(CreateView):
    model = Board
    fields = [ 'title', 'subject' ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BoardUpdate(UpdateView):
    model = Board
    fields = [ 'title', 'subject']


class BoardDelete(DeleteView):
    model = Board
    success_url = '/boards/'

def boards_index(request):
  boards = Board.objects.all()
  return render(request, 'boards/index.html', {'boards': boards})
     # board views 

def boards_detail(request, board_id,):
    board = Board.objects.get(id = board_id)
    image= Image.objects.exclude(id__in= board.images.all().values_list('id'))
   
    return render(request, 'boards/detail.html', {'board': board, 'image': image})

def assoc_image(request , board_id, image_id):

     Board.objects.get(id = board_id).images.add(image_id)
     return redirect('board_detail', board_id =board_id)

def unassoc_image(request , board_id, image_id):

    
    Board.objects.get(id = board_id).images.remove(image_id)
    return redirect('board_detail', board_id = board_id)


