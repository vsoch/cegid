from functools import wraps

from django.http.response import (HttpResponseRedirect, JsonResponse)
from django.shortcuts import (render, get_object_or_404, render_to_response,
                              redirect)
from .models import UserProfile
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib import auth
from .forms import UserEditForm, UserCreateForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
import pickle

def create_user(request, template_name='registration/signup.html'):
    if request.method == "POST":
        form = UserCreateForm(request.POST, request.FILES, instance=User())
        if form.is_valid():
            form.save()
            new_user = auth.authenticate(username=request.POST['username'],
                                         password=request.POST['password1'])

            # We now save the user into the UserProfile object, with a role
            profile_picture = request.POST.get('picture',None)
            new_staff,_ = UserProfile.objects.update_or_create(user=new_user,
                                                               avatar=profile_picture)
            new_staff.save()
            auth.login(request, new_user)

            # Do something. Should generally end with a redirect. For example:
            if request.POST['next']:
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse("edit_profile"))
    else:
        form = UserCreateForm(instance=User())

    context = {"form": form,
               "request": request,
               "submit_text":"Sign Up",
               "form_title":"Sign Up"}
    return render(request, template_name, context)


def view_profile(request, username=None):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (reverse('login'), request.path))
    user_base = User.objects.get(username=request.user)
    user_profile,_ = UserProfile.objects.get_or_create(user=user_base)
    return render(request, 'registration/profile.html', {'user': user_profile})


@login_required
def edit_user(request):
    '''edit_user is for password and email.
    '''
    edit_form = UserEditForm(request.POST or None, instance=request.user)
    if request.method == "POST":
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse("my_profile"))
    return render_to_response("registration/edit_user.html",
                              {'form': edit_form},
                              context_instance=RequestContext(request))

@login_required
def edit_profile(request):
    '''edit_profile will allow the user to edit profile information like picture, description,etc.
    '''
    if request.user.is_authenticated():
        user = get_object_or_404(User,username=request.user)
        user_profile = UserProfile.objects.get(user=user)
        edit_form = UserUpdateForm(instance=user_profile)
        context = {'form_title':"Edit Profile",
                   'submit_text':"Submit"}
        if request.method == "POST":
            edit_form = UserUpdateForm(request.POST, request.FILES,instance=user_profile) 
            if edit_form.is_valid():
                edit_form.save()
                return HttpResponseRedirect(reverse("my_profile"))
        context['form'] = edit_form
        return render_to_response("registration/edit_profile.html",
                                  context,
                                  context_instance=RequestContext(request))
    return HttpResponseRedirect(reverse("my_profile"))


def view_faculty(request):
    context = {"title":"Faculty"}
    context["people"] = UserProfile.objects.filter(role="FACULTY")
    return render(request, 'people/people.html',context)


def view_staff(request):
    context = {"title":"Staff"}
    context["people"] = UserProfile.objects.filter(role="STAFF")
    return render(request, 'people/people.html',context)

def view_students(request):
    context = {"title":"Students"}
    context["people"] = UserProfile.objects.filter(role="STUDENTS")
    return render(request, 'people/people.html',context)

# def login(request):
#     return render_to_response('home.html', {
#         'plus_id': getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None)
#     }, RequestContext(request))
