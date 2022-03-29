from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.template.response import TemplateResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
from django.db.models import Q

from django.contrib.auth import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from django.urls import *
from .models import Bb, Car
from .models import Rubric, CarBrands, CarModels
from .forms import BbForm, CarForm, CarFormEdit, UserForm, ProfileForm, StartForm, CarBrandsForm


def index(request):
    bbs = Bb.objects.all()
    rubrics = Rubric.objects.all()
    paginator = Paginator(bbs, 6)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'rubrics': rubrics, 'page': page, 'bbs': page.object_list}
    return render(request, 'bboard/index.html', context)


def by_rubric(request, rubric_id):
    bbs = Bb.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.all()
    current_rubric = Rubric.objects.get(pk=rubric_id)
    context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}
    return render(request, 'bboard/by_rubric.html', context)


def by_logged_user(request):
    bbs = Bb.objects.all()
    context = {'bbs': bbs}
    return render(request, 'bboard/by_logged_user.html', context)


class BbCreateView(CreateView):
    template_name = 'bboard/create.html'
    form_class = CarForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbEditView(UpdateView):
    model = Bb
    form_class = BbForm
    template_name_suffix = '_edit'
    success_url = reverse_lazy('index')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class CarEditView(UpdateView):
    model = Car
    form_class = CarFormEdit
    template_name_suffix = ''
    template_name = 'bboard/bb_edit.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['Car'] = Rubric.objects.all()
        return context


class BbDeleteView(DeleteView):
    model = Bb
    success_url = reverse_lazy('index')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


def add_and_save(request, rubric_id):
    current_rubric = Rubric.objects.get(pk=rubric_id)
    if current_rubric.name == 'Авто':
        if request.method == 'GET':
            bbf = CarBrandsForm(request.GET)
            if bbf.is_valid():
                bbf.save(commit=False)
                carbrand_id = bbf.cleaned_data['name'].pk
                return HttpResponseRedirect(
                    reverse('add_car_by_brand', kwargs={'rubric_id': rubric_id, 'carbrand_id': carbrand_id}))
            else:
                context = {'form': bbf, 'current_rubric': current_rubric}
                return render(request, 'bboard/create_rub.html', context)
        else:
            bbf = CarBrandsForm()
            context = {'form': bbf, 'current_rubric': current_rubric}
            return render(request, 'bboard/create_rub.html', context)
    else:
        if request.method == 'POST':
            bbf = BbForm(request.POST, request.FILES)
            if bbf.is_valid():
                bb = bbf.save(commit=False)
                bb.buser = request.user.username
                bb.rubric = Rubric.objects.get(pk=rubric_id)
                bbf.save()
                return HttpResponseRedirect(reverse('by_rubric', kwargs={'rubric_id': rubric_id}))
            else:
                context = {'form': bbf, 'current_rubric': current_rubric}
                return render(request, 'bboard/create.html', context)
        else:
            bbf = BbForm()
            context = {'form': bbf, 'current_rubric': current_rubric}
            return render(request, 'bboard/create.html', context)


def add_car_by_brand(request, rubric_id, carbrand_id):
    current_rubric = Rubric.objects.get(pk=rubric_id)
    print(carbrand_id)
    if request.method == 'POST':
        bbf = CarForm(carbrand_id, request.POST, request.FILES)
        if bbf.is_valid():
            bb = bbf.save(commit=False)
            bb.buser = request.user.username
            bb.rubric = Rubric.objects.get(pk=rubric_id)
            context_eq = Car.objects.filter(model=bb.model)
            if len(context_eq):
                avg_price = 0
                coin = 0
                for obj in context_eq:
                    if obj != bb:
                        if (obj.year == bb.year) or (obj.year == (bb.year + 1)) or (obj.year == (bb.year - 1)):
                            if ((obj.mileage - bb.mileage) < 30001) and ((bb.mileage - obj.mileage) < 30001):
                                avg_price += obj.price
                                coin += 1
                if coin:
                    avg_price = avg_price / coin
                    if (bb.price < avg_price) and (bb.price > avg_price * 0.8) and (bb.price <= avg_price * 0.9):
                        bb.is_competitive = 1
                    elif (bb.price < avg_price) and (bb.price > avg_price * 0.7) and (bb.price <= avg_price * 0.8):
                        bb.is_competitive = 2
                    elif (bb.price > avg_price) and (bb.price > avg_price * 1.1) and (bb.price <= avg_price * 1.2):
                        bb.is_competitive = -1
                    elif (bb.price > avg_price) and (bb.price > avg_price * 1.2) and (bb.price <= avg_price * 1.3):
                        bb.is_competitive = -2

            bbf.save()
            return HttpResponseRedirect(reverse('by_rubric', kwargs={'rubric_id': rubric_id}))
        else:
            context = {'form': bbf, 'current_rubric': current_rubric, 'carbrand_id': carbrand_id}
            return render(request, 'bboard/create.html', context)
    else:
        bbf = CarForm(carbrand_id)
        context = {'form': bbf, 'current_rubric': current_rubric, 'carbrand_id': carbrand_id}
        return render(request, 'bboard/create.html', context)


def add_rub(request):
    if request.method == 'GET':
        bbf = StartForm(request.GET)
        if bbf.is_valid():
            bbf.save(commit=False)
            return HttpResponseRedirect(reverse('add_by_rub', kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
        else:
            context = {'form': bbf}
            return render(request, 'bboard/create_rub.html', context)
    else:
        bbf = StartForm()
        context = {'form': bbf}
        return render(request, 'bboard/create_rub.html', context)


class BbDetailView(DetailView):
    model = Bb

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class CarDetailView(DetailView):
    model = Car

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Car'] = Rubric.objects.all()
        return context


@login_required
def profile_view(request):
    profile = User.objects.all()
    context = {'profile': profile}
    return render(request, 'registration/user_profile.html', context)


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('profile')
        else:
            messages.error(request, 'Пожалуйсте корретно заполните данные.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'registration/update_profile.html', {'user_form': user_form, 'profile_form': profile_form})


def user_reg(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/user_registrate.html', {'form': form})


def profile_ads_view(request, pk):
    bbs = Bb.objects.get(pk=pk)
    viewed = User.objects.get(username=bbs.buser)
    context = {'viewed': viewed}
    return render(request, 'bboard/profile_ads_view.html', context)


def search_ads(request):
    query = request.GET.get('what')

    bbs = Bb.objects.filter(
        Q(title__icontains=query) | Q(title__icontains=query.title()) | Q(title__icontains=query.lower())
        | Q(title__icontains=query.upper()))

    bbs2 = Bb.objects.filter(
        Q(content__icontains=query) | Q(content__icontains=query.title()) | Q(content__icontains=query.lower())
        | Q(content__icontains=query.upper()))
    context = {'bbs': bbs, 'bbs2': bbs2, 'query': query}
    return render(request, 'bboard/search_result.html', context)


class BbRedirectView(RedirectView):
    url = '/detail/%(pk)d/'
