from django.shortcuts import render, get_object_or_404
from .models import blogPost
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ( ListView, CreateView,
	DetailView, UpdateView, DeleteView,
	)


class UserPostsListView(ListView):
	model = blogPost
	template_name = 'blogPosts/users_all_post.html'
	context_object_name = 'posts'
	paginate_by = 4	

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return blogPost.objects.filter(author=user)

class PostDetailView(DetailView):
	model = blogPost
	context_object_name = 'post'
	template_name = 'blogPosts/post_detail.html'


class PostCreateView(LoginRequiredMixin, CreateView):
	model = blogPost
	fields = ['image','title','content']
	template_name = 'blogPosts/create_post.html'

	def form_valid(self,form):
		form.instance.author=self.request.user
		messages.info(self.request,"Your post Created")
		return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,
						SuccessMessageMixin, UpdateView):
	model = blogPost
	fields = ['image','title','content']
	template_name = 'blogPosts/create_post.html'
	success_message = "Your post was updated successfully"
 
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = blogPost
	template_name = 'blogPosts/post_delete.html'
	success_url='/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False


def homePage(request):
	posts = blogPost.objects.all().order_by('-date')
	recent_posts = blogPost.objects.all().order_by('date')[:3]
	total = User.objects.all().count()
	try:
		recent_user = User.objects.all()[total-3:]
	except:
		recent_user = User.objects.all()
		
	paginator = Paginator(posts,5)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	return render(request,'blogPosts/home.html',
		{'recent_posts':recent_posts,
		'recent_user':recent_user, 'page_obj':page_obj})