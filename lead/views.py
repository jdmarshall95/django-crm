from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from openpyxl import Workbook

import datetime

from .forms import AddLeadForm
from .models import Lead

from client.models import Client
from team.models import Team

@login_required
def leads_list(request):
    leads = Lead.objects.filter(created_by=request.user)

    return render(request, 'lead/leads_list.html', {
        'leads': leads
    })

@login_required
def leads_detail(request, pk):
    lead = Lead.objects.filter(created_by=request.user).get(pk=pk)

    return render(request, 'lead/leads_detail.html', {
        'lead':lead
    })

@login_required
def leads_delete(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
    lead.delete()

    messages.success(request, 'Запись была успешно удалена.')

    return redirect('leads_list')

@login_required
def leads_edit(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)

    if request.method == 'POST':
        form = AddLeadForm(request.POST, instance=lead)

        if form.is_valid():
            form.save()

            messages.success(request, 'Запись была успешно изменена.')

            return redirect('leads_list')
    else:
        form = AddLeadForm(instance=lead)

    return render(request, 'lead/edit_lead.html',{
        'form': form
    })    

@login_required
def add_lead(request):
    team = Team.objects.filter(created_by=request.user)[0]

    if request.method == 'POST':
        form = AddLeadForm(request.POST)

        if form.is_valid():
            team = Team.objects.filter(created_by=request.user)[0]
            
            lead = form.save(commit=False)

            lead.created_by = request.user
            lead.team = team
            
            lead.save()

            messages.success(request, 'Запись была успешно добавлена.')

            return redirect('leads_list') 
        
    else:
        form = AddLeadForm()

    return render(request, 'lead/add_lead.html', {
        'form': form,
        'team':team
    })

@login_required
def convert_to_client(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
    team = Team.objects.filter(created_by=request.user)[0]      

    client = Client.objects.create(
        name=lead.name,
        email=lead.email,
        description=lead.description,
        created_by=request.user,
        team=team,
    )

    lead.converted_to_client = True
    lead.save()

    messages.success(request, 'Лид был успешно конвертирован в клиента.')

    return redirect('leads_list')

@login_required
def export_to_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    filename = str(datetime.datetime.now()) + "leads.xlsx" 
    response['Content-Disposition'] = 'attachment; filename="%s"' %filename

    wb = Workbook()
    ws = wb.active
    ws.title = "Лиды" 

    # Add headers
    headers = ["Имя", "Приоритет", "Статус"]
    ws.append(headers)

    # Add data from the model
    leads = Lead.objects.filter(created_by=request.user)
    for lead in leads:
        ws.append([lead.name, lead.priority, lead.status])

    # Save the workbook to the HttpResponse
    wb.save(response)
    return response

