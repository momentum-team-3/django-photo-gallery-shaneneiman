#Django Imports 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

#Project File Imports
from .models import User
from .forms import UpdateUserForm


# Views
@login_required
def view_profile(request):
    user = request.user
    if request.method == "GET":
        form = UpdateUserForm(instance=user)
    else:
        form = UpdateUserForm(request.POST, instance=user, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect("profile")
    return render(request, "users/profile.html", {
        "user": user,
        "form": form
    })