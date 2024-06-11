from django.shortcuts import render
from django.http import HttpResponse
from info_graph.models import DataEntry,Month,Year
import json

def view_graph(request):
    data_entries = DataEntry.objects.all().order_by('month__year__year', 'month__month')

    labels = [f"{entry.month.month_name}" for entry in data_entries]
    greenhouse_gas_data = [entry.greenhouse_gas for entry in data_entries]
    electricity_data = [entry.electricity for entry in data_entries]
    diesel_data = [entry.diesel for entry in data_entries]
    water_data = [entry.water for entry in data_entries]
    landfill_waste_data = [entry.landfill_waste for entry in data_entries]
    paper_a4_a3_data = [entry.paper_a4_a3 for entry in data_entries]

    context = {
        'data_entries': data_entries,
        'labels': json.dumps(labels),
        'greenhouse_gas_data': json.dumps(greenhouse_gas_data),
        'electricity_data': json.dumps(electricity_data),
        'diesel_data': json.dumps(diesel_data),
        'water_data': json.dumps(water_data),
        'landfill_waste_data': json.dumps(landfill_waste_data),
        'paper_a4_a3_data': json.dumps(paper_a4_a3_data),
    }
    return render(request,'frontend/view_graph.html',context)