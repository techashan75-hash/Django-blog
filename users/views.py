from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm
#9from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse_lazy
from .utils import send_welcome_email


def register(request):
  if request.method == 'POST':
    form=UserRegisterForm(request.POST)
    if form.is_valid():
      form.save()
      #send_welcome_email(user)
      username = form.cleaned_data.get('username')
      #password = form.cleaned_data.get('password1')
      messages.success(request,f'Account created for {username}!')
      return redirect('login')
  else:
 # This part ensures a response is returned if it's NOT a POST request
    form = UserRegisterForm()
 # This must be outside the 'if' block
  return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
  if request.method =='POST':
    u_form=UserUpdateForm(request.POST,instance=request.user)
    p_form=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
    if u_form.is_valid() and p_form.is_valid():
      u_form.save()
      p_form.save()
      messages.success(request,f'{request.user.username} Profile updated successfully!')
      return redirect('profile')
  else:
    u_form=UserUpdateForm(instance=request.user)
    p_form=ProfileUpdateForm(instance=request.user.profile)
    context ={
      'u_form':u_form,
      'p_form':p_form
    }
  return render(request,'users/profile.html',context)
  
"""@require_POST
def logout_View(request):
    logout(request)
    return render('login')"""
    
    


class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset.html'
    success_url = reverse_lazy('password_reset_done')     # redirect after submit
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    # Optional: force plain text version from .txt automatically
    html_email_template_name = 'users/password_reset_email.html'

 

