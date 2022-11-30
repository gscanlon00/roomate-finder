from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import *
from .forms import *


def index(request):
    return render(request, 'index.html')


def logout_view(request):
    logout(request)


class Login(LoginView):
    template_name = 'login.html'


class Register(CreateView):
    model = SiteUser
    form_class = UserSignupForm
    template_name = 'signup.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


def all_properties(request):
    all_p = Property.objects.all()

    return render(request, 'all_properties.html', {'properties': all_p})


def single_property(request, pid):
    if Property.objects.filter(pk=pid).exists():
        user = request.user
        prod = Property.objects.get(pk=pid)
        offers = Offer.objects.filter(from_user=user, property=prod)
        return render(request, 'single_property.html', {'property': prod, 'offers': offers})
    else:
        all_p = Property.objects.all()
        return render(request, 'all_properties.html', {'properties': all_p})


def profile(request, name):
    if SiteUser.objects.filter(username=name).exists():
        profile_name = SiteUser.objects.get(username=name)
        new_offers = Offer.objects.filter(receiver=profile_name)
        old_offers = Offer.objects.filter(receiver=profile_name, is_read=True)
        return render(request, 'profile_page.html', {'profile': profile_name,
                                                     'new_offers': new_offers,
                                                     'old_offers': old_offers})
    else:
        return redirect('/error')


@login_required()
def offers(request):
    user = request.user
    new_offers = Offer.objects.filter(receiver=user, is_read=False, accepted=False)
    accepted_offers = Offer.objects.filter(receiver=user, accepted=True)
    sent_offers = Offer.objects.filter(from_user=user)
    return render(request, 'offers.html', {'new_offers': new_offers,
                                           'accepted_offers': accepted_offers,
                                           'sent_offers': sent_offers})


@login_required()
def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            new_property = form.save(commit=False)
            new_property.user = request.user
            new_property.save()
            return render(request, 'single_property.html', {'property': new_property})
    else:
        form = PropertyForm()
        return render(request, 'add_property.html', {'form': form})


@login_required()
def edit_property(request, property_id):

    property_to_edit = get_object_or_404(Property, pk=property_id, user=request.user)
    form = UpdatePropertyForm(instance=property_to_edit)
    if request.method == 'POST':
        form = UpdatePropertyForm(request.POST, request.FILES, instance=property_to_edit)
        if form.is_valid():
            form.save()
            return render(request, 'single_property.html', {'property': property_to_edit})
    else:
        form = UpdatePropertyForm(instance=property_to_edit)
    return render(request, "edit_property.html", {'form': form, 'property': property_to_edit})


def edit_property_picture(request, property_id):
    property_to_edit = get_object_or_404(Property, pk=property_id, user=request.user)
    form = UpdatePropertyPic(instance=property_to_edit)
    if request.method == 'POST':
        form = UpdatePropertyPic(request.POST, request.FILES, instance=property_to_edit)
        if form.is_valid():
            form.save()
            return render(request, 'single_property.html', {'property': property_to_edit})
    else:
        form = UpdatePropertyPic(instance=property_to_edit)
    return render(request, "edit_property.html", {'form': form, 'property': property_to_edit})


@login_required()
def edit_user(request):
    user_to_edit = request.user
    user_name = user_to_edit.username
    form = UpdateUserForm(instance=user_to_edit)
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, request.FILES, instance=user_to_edit)
        if form.is_valid():
            form.save()
            return render(request, 'profile_page.html', {'profile': user_to_edit})
    else:
        form = UpdateUserForm(instance=user_to_edit)
        return render(request, "edit_user.html", {'form': form, 'user': user_to_edit})


@login_required()
def edit_user_pic(request):
    user_to_edit = request.user
    form = UpdateUserPic(instance=user_to_edit)
    if request.method == 'POST':
        form = UpdateUserPic(request.POST, request.FILES, instance=user_to_edit)
        if form.is_valid():
            form.save()
            return render(request, 'profile_page.html', {'profile': user_to_edit})
    else:
        form = UpdateUserPic(instance=user_to_edit)
        return render(request, "edit_user.html", {'form': form, 'user': user_to_edit})


@login_required()
def display_own_properties(request):
    properties = Property.objects.filter(user=request.user)

    return render(request, 'all_properties.html', {'properties': properties})


# For each property, a list will be made with the property object first followed by attributes that we compare
# We loop through the list and compare each attribute to the user's one and total up the total difference between
# them all. We store the total for each property in a dictionary and the property that has the lowest total
# is returned (i.e the difference between attributes was smallest)
@login_required()
def recommended_property(request):
    user = request.user
    d = {}
    userl = [user.cleanliness, user.noise_level, user.age, (user.budget/5)]
    all_p = Property.objects.all()
    print(user.re_gender)

    # Filter properties depending on hard requirements the user has set
    if user.smoking is True:
        all_p = all_p.filter(allows_smoking=True)
    if user.has_pet is True:
        all_p = all_p.filter(allows_pets=True)
    if user.wc_access is True:
        all_p = all_p.filter(wc_access=True)
    if user.re_gender != "4": # If the user has a gender preference
        all_p = all_p.filter(gender=user.re_gender)

    for p in all_p:
        # Check if the user has disliked the property, if they have ignore it
        if Dislikes.objects.filter(user=user, property=p).exists():
            continue
        else:
            l = [p, p.cleanliness, p.noise_level, p.age, (p.price/5)]
            sum_l = [sum(l[1::]), sum(userl)]
            max_v = max(sum_l)
            total = 0
            for a in range(0, len(userl)):
                total += abs(l[a+1] - userl[a])

            d[l[0]] = total

    most_similar = min(d, key=d.get)

    offers = Offer.objects.filter(from_user=user, property=most_similar)
    percentage = 100 - int((d[most_similar] / max_v) * 100) # Getting percentage to show how close a match
    return render(request, 'recommended.html', {'property': most_similar, 'percentage': percentage, 'offers': offers})


@login_required()
def dislike(request, pid):
    user = request.user
    p = Property.objects.get(pk=pid)
    d = Dislikes(user=user, property=p)
    d.save()
    return recommended_property(request)


@login_required()
def like(request, pid):
    user = request.user
    p = Property.objects.get(pk=pid)
    receiver = p.user
    o = Offer(from_user=user, receiver=receiver, property=p)
    o.save()
    offers = Offer.objects.filter(from_user=user, property=p)
    return render(request, 'single_property.html', {'property': p, 'offers': offers})


@login_required()
def accept_offer(request, oid):
    offer = Offer.objects.get(pk=oid)
    offer.is_read = True
    offer.accepted = True
    offer.save()

    user = request.user
    new_offers = Offer.objects.filter(receiver=user, is_read=False, accepted=False)
    accepted_offers = Offer.objects.filter(receiver=user, accepted=True)
    sent_offers = Offer.objects.filter(from_user=user)
    return render(request, 'offers.html', {'new_offers': new_offers,
                                           'accepted_offers': accepted_offers,
                                           'sent_offers': sent_offers})

