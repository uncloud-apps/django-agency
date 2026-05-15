from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.utils import timezone

from .models import Server, AdoptionApplication
from .forms import AdoptionApplicationForm, ServerFilterForm


def home(request):
    featured = Server.objects.featured()[:3]
    stats = {
        'available': Server.objects.available().count(),
        'adopted': Server.objects.filter(status=Server.Status.ADOPTED).count(),
        'pending_applications': AdoptionApplication.objects.pending().count(),
    }
    return render(request, 'shelter/home.html', {'featured': featured, 'stats': stats})


def server_list(request):
    filter_form = ServerFilterForm(request.GET or {'status': 'available'})
    servers = Server.objects.all()

    if filter_form.is_valid():
        if species := filter_form.cleaned_data.get('species'):
            servers = servers.filter(species=species)
        if size := filter_form.cleaned_data.get('size'):
            servers = servers.filter(size=size)
        if status := filter_form.cleaned_data.get('status'):
            servers = servers.filter(status=status)


    context = {'servers': servers, 'filter_form': filter_form}

    if request.htmx:
        return render(request, 'shelter/partials/server_grid.html', context)
    return render(request, 'shelter/server_list.html', context)


def server_detail(request, slug):
    server = get_object_or_404(Server, slug=slug)
    form = AdoptionApplicationForm()
    return render(request, 'shelter/server_detail.html', {'server': server, 'form': form})


@require_POST
def apply(request, slug):
    server = get_object_or_404(Server, slug=slug)
    form = AdoptionApplicationForm(request.POST)

    if form.is_valid():
        application = form.save(commit=False)
        application.server = server
        application.save()

        if request.htmx:
            return render(request, 'shelter/partials/application_thanks.html', {
                'application': application,
                'server': server,
            })
        return redirect('application_status', pk=application.pk)

    if request.htmx:
        return render(request, 'shelter/partials/application_form.html', {
            'form': form,
            'server': server,
        })
    return render(request, 'shelter/server_detail.html', {'server': server, 'form': form})


def application_status(request, pk):
    application = get_object_or_404(AdoptionApplication, pk=pk)
    return render(request, 'shelter/application_status.html', {'application': application})
