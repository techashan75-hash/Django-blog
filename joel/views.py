from django.shortcuts import render,get_object_or_404
from .models import Post
from django.contrib.auth.models import User
from django.views.generic import ListView,DetailView,CreateView ,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .filters import PostFilter


# Create your views here.
def home(request):
  context={'posts':Post.objects.all()}
  return render(request,'joel/home.html',context)
  
class PostListView(ListView):
  model=Post
  template_name='joel/home.html'
  context_object_name='posts'
  paginate_by = 4
  
  def get_queryset(self):
    queryset = Post.objects.all()
    self.filterset = PostFilter(self.request.GET, queryset=queryset)
    return self.filterset.queryset
        
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['filter'] = self.filterset
    return context
  
class UserPostListView(ListView):
  model=Post
  template_name='joel/user_posts.html'
  context_object_name='posts'
  paginate_by = 4
  
  def get_queryset(self):
    user=get_object_or_404(User,username=self.kwargs.get('username'))
    return Post.objects.filter(author=user).order_by('-date_created')
    
    
class PostDetailView(DetailView):
  model=Post
  #<app_name>/<model_name>_detail.html _Automatic template look up.
  #joel/post_detail.html --converts all to lowercase
  
  #context_object_name ==django generic is object,auto_generated ==lowercase model model name 
  #{{ post }},{{ object }}
  
class PostCreateView(LoginRequiredMixin,CreateView):
  model=Post
  fields = ['title','content']
  
  def form_valid(self,form):
    form.instance.author =self.request.user
    return super().form_valid(form)
   #template rendering =app_name/modelname_form.html
   
class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
  model=Post
  fields = ['title','content']
  
  def form_valid(self,form):
    form.instance.last_updated_by =self.request.user
    return super().form_valid(form)
    
  def test_func(self):
    post=self.get_object()
    if self.request.user == post.author:
      return True
    return False
    
class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
  model=Post
  success_url='/' #homepage
  
  def test_func(self):
    post=self.get_object()
    if self.request.user == post.author:
      return True
    return False
    
def about(request):
  return render(request,'joel/about.html',{})
  
 