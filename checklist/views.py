from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (ListView, 
	DetailView, 
	CreateView,
	UpdateView,
	DeleteView
)
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from .models import Checklist, Upvote

# home page - this function will be called when I navigate to "localhost:8000/"
def home(request):
	# return HttpResponse('<h1>This is your home page! Welcome</h1>')

	# count upvotes for each post
	upvotes_cnt_list = []
	checklists_var = Checklist.objects.all().order_by('-date_posted')
	for checklist in checklists_var:
		upvotes_cnt_list.append(Upvote.objects.filter(checklist=checklist).count())

	checklist_upvotes = zip(checklists_var, upvotes_cnt_list)
	context = {
		'checklist_upvotes': checklist_upvotes,
		'title': 'home'
	}
	return render(request, 'checklist/home.html', context) # because render looks in templates subdirectory, by default


# can be used instead of "home" method - however useless
class ChecklistListView(ListView):
	model = Checklist
	template_name = 'checklist/home.html' # <app_name>/<model>_<viewtype>.html
	context_object_name = 'checklists_var'
	ordering = ['-date_posted']
	paginate_by = 5


class UserChecklistListView(ListView):
	model = Checklist
	template_name = 'checklist/user_checklists.html' # <app_name>/<model>_<viewtype>.html
	context_object_name = 'checklists_var'
	paginate_by = 5

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Checklist.objects.filter(author=user).order_by('-date_posted')


class ChecklistDetailView(DetailView):
	model = Checklist


class ChecklistCreateView(LoginRequiredMixin, CreateView):
	model = Checklist
	fields = ['title', 'content']

	# to link logged in user as author to the checklist being created
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

# mixins for checking if user is logged in and the checklist author is the same as logged in user
class ChecklistUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Checklist
	fields = ['title', 'content']

	# to link logged in user as author to the checklist being updated
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	# checks if currently logged in user is the checklist author
	def test_func(self):
		checklist = self.get_object()
		return (self.request.user == checklist.author)


class ChecklistDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Checklist
	success_url = '/'

	# checks if currently logged in user is the checklist author
	def test_func(self):
		checklist = self.get_object()
		return (self.request.user == checklist.author)

def about(request):
	return render(request, 'checklist/about.html', {'title_new': 'about'})

# my checklist page - shows checklists written by the logged in user only
def mychecklist(request):
	context = {
		'checklists_var': request.user.checklist_set.all().order_by('-date_posted'),
		'title': 'My Checklists'
	}

	return render(request, 'checklist/mychecklist.html', context) # because render looks in templates subdirectory, by default

def upvote_post(request, checklist_id, username):
	# for "messages", refer https://stackoverflow.com/a/61603003/6543250
	
	if Upvote.objects.filter(user=User.objects.filter(username=username).first(), checklist=Checklist.objects.get(id=checklist_id)):
		msg = 'You have already upvoted the checklist once!'
		messages.info(request, msg)
	else:
		# if fetching by id, use "get()", else "filter()"
		upvote_obj = Upvote(user=User.objects.filter(username=username).first(), checklist=Checklist.objects.get(id=checklist_id))
		upvote_obj.save()

		msg = 'Checklist upvoted!'
		messages.info(request, msg)

	# redirect to home url; simply reload the page
	return redirect('checklist-home') 