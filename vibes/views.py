from django.contrib.sites.models import Site
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from .forms import SignUpForm, UserForm, ProjectForm
from .models import UserProfile, Project
from .tokens import account_activation_token

# Create your views here.


def home(request):
    projects = Project.objects.all()
    return render(request, 'home.html', {'projects': projects})


def project(request, project_id):
    try:
        project = Project().fetch_project(project_id)
    except ObjectDoesNotExist:
        raise Http404()
    return render(request, 'project.html', {'project': project})


@login_required(login_url='login/')
def new_project(request):
    current_user = request.user
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            project = form.save(commit=False)
            project.project_owner = current_user
            project.save()
            return redirect('home')
    else:
        form = ProjectForm()
    return render(request, 'new_project.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            subject = "Activate Your Photopedia Account"
            current_site = Site.objects.get_current()
            print(current_site.domain)
            # current_site = get_current_site(request)
            sender = "atst.acc19@gmail.com"

            # passing in the context vairables
            text_content = render_to_string(
                "email/account_activation_email.txt",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            html_content = render_to_string(
                "email/account_activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )

            msg = EmailMultiAlternatives(
                subject, text_content, sender, [user.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'email/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('edit_profile')
    else:
        return render(request, 'email/account_activation_invalid.html')


@login_required(login_url='login/')
def profile(request):
    # TODO: 1. get current logged in user
    # TODO: 2. fetch user profile data
    # TODO: 3. pass the user profile data to the template form

    current_user = request.user
    user_data = User.objects.get(id=current_user.id)
    user_profile = UserProfile.objects.get(id=current_user.id)

    return render(request, 'registration/profile.html', {'user_data': user_data, 'user_profile': user_profile})


@login_required(login_url='login/')  # only logged in users should access this
def edit_profile(request):

    current_user = request.user
    user = User.objects.get(id=current_user.id)

    # prepopulate UserProfileForm with retrieved user values from above.
    user_form = UserForm(instance=user)

    # The sorcery begins from here, see explanation below
    ProfileInlineFormset = inlineformset_factory(User, UserProfile, fields=(
        'photo', 'phone', 'bio'))
    formset = ProfileInlineFormset(instance=user)

    if request.user.is_authenticated and request.user.id == user.id:
        if request.method == "POST":
            user_form = UserForm(request.POST, request.FILES, instance=user)
            formset = ProfileInlineFormset(
                request.POST, request.FILES, instance=user)

            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(
                    request.POST, request.FILES, instance=created_user)

                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return redirect('profile')

        return render(request, "registration/account_update.html", {
            "noodle": user.id,
            "noodle_form": user_form,
            "formset": formset,
        })
    else:
        raise PermissionDenied
