from functools import wraps

from django.http.response import (HttpResponseRedirect, JsonResponse)
from django.shortcuts import (render, get_object_or_404, render_to_response,
                              redirect)
from .models import User
from django.contrib.auth.models import User as djUser
from django.core.urlresolvers import reverse
from django.contrib import auth
from .forms import UserEditForm, UserCreateForm
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext

def create_user(request, template_name='registration/signup.html'):
    if request.method == "POST":
        form = UserCreateForm(request.POST, request.FILES, instance=djUser())
        if form.is_valid():
            form.save()
            new_user = auth.authenticate(username=request.POST['username'],
                                         password=request.POST['password1'])

            # We now save the user into the Expfactory User object, with a role
            expfactory_user,_ = User.objects.update_or_create(user=new_user,
                                                              role="LOCAL")
            expfactory_user.save()
            auth.login(request, new_user)

            # Do something. Should generally end with a redirect. For example:
            if request.POST['next']:
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse("my_profile"))
    else:
        form = UserCreateForm(instance=User())

    context = {"form": form,
               "request": request}
    return render(request, template_name, context)


def view_profile(request, username=None):
    if not username:
        if not request.user.is_authenticated():
            return redirect('%s?next=%s' % (reverse('login'), request.path))
        else:
            user = request.user
    else:
        user = get_object_or_404(User, username=username)
    return render(request, 'registration/profile.html', {'user': user})


@login_required
def edit_user(request):
    edit_form = UserEditForm(request.POST or None, instance=request.user)
    if request.method == "POST":
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse("my_profile"))
    return render_to_response("registration/edit_user.html",
                              {'form': edit_form},
                              context_instance=RequestContext(request))


# def login(request):
#     return render_to_response('home.html', {
#         'plus_id': getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None)
#     }, RequestContext(request))
