from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from django.shortcuts import redirect, render

from .forms import ContactMessageForm, ReportFilterForm
from .models import WorkLog


def home(request):
	form = ContactMessageForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		contact_message = form.save()
		messages.success(
			request,
			f'Gracias, {contact_message.name}. Nuestro equipo se pondrá en contacto contigo pronto.',
		)
		return redirect('/#contacto')

	return render(request, 'ecotech/home.html', {'form': form})


def solutions(request):
	return render(request, 'ecotech/section_page.html', {'page': 'solutions'})


def process(request):
	return render(request, 'ecotech/section_page.html', {'page': 'process'})


def about(request):
	return render(request, 'ecotech/section_page.html', {'page': 'about'})


def impact(request):
	return render(request, 'ecotech/section_page.html', {'page': 'impact'})


def resources(request):
	return render(request, 'ecotech/section_page.html', {'page': 'resources'})


def contact(request):
	form = ContactMessageForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		contact_message = form.save()
		messages.success(request, f'Gracias, {contact_message.name}. Recibimos tu mensaje.')
		return redirect('contact')

	return render(request, 'ecotech/section_page.html', {'page': 'contact', 'form': form})


@staff_member_required
def reports(request):
	form = ReportFilterForm(request.GET or None)
	logs = WorkLog.objects.select_related('employee', 'project')
	if form.is_valid():
		if form.cleaned_data['employee']:
			logs = logs.filter(employee=form.cleaned_data['employee'])
		if form.cleaned_data['project']:
			logs = logs.filter(project=form.cleaned_data['project'])
		if form.cleaned_data['start_date']:
			logs = logs.filter(date__gte=form.cleaned_data['start_date'])
		if form.cleaned_data['end_date']:
			logs = logs.filter(date__lte=form.cleaned_data['end_date'])

	return render(request, 'ecotech/reports.html', {
		'form': form,
		'logs': logs,
		'total_hours': logs.aggregate(total=Sum('hours'))['total'] or 0,
	})
