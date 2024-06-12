from django.shortcuts import render, get_object_or_404
#from greenweb.models import Category,Year, Issue, Indicator, Evidence
from info_graph.models import DataEntry,Month,Year
import json
from django.templatetags.static import static
from blogs.models import Information
from docChecker.models import Year, CategoryGroup, Category, Issue, Indicator, Evidence

def view_group(request, group_name):
    category_group = get_object_or_404(CategoryGroup, group_name=group_name)
    categories = category_group.categories.all()

    context = {
        'category_group': category_group,
        'categories': categories,
    }

    return render(request, 'frontend/view_group.html', context)

def index2(request):
    # เอาข้อมูลใน information ทั้งหมด เอาแค่ 3 record และเรียงตามวันที่ล่าสุด
    informations = Information.objects.all().order_by('-date')[:3]

    # เอาข้อมูลใน DataEntry ทั้งหมด และเรียงตามปีและเดือน
    data_entries = DataEntry.objects.all().order_by('month__year__year', 'month__month')
    labels = [f"{entry.month.month_name}" for entry in data_entries]
    greenhouse_gas_data = [entry.greenhouse_gas for entry in data_entries]
    electricity_data = [entry.electricity for entry in data_entries]
    diesel_data = [entry.diesel for entry in data_entries]
    water_data = [entry.water for entry in data_entries]
    landfill_waste_data = [entry.landfill_waste for entry in data_entries]
    paper_a4_a3_data = [entry.paper_a4_a3 for entry in data_entries]

    context = {
        'informations': informations,
        'data_entries': data_entries,
        'labels': json.dumps(labels),
        'greenhouse_gas_data': json.dumps(greenhouse_gas_data),
        'electricity_data': json.dumps(electricity_data),
        'diesel_data': json.dumps(diesel_data),
        'water_data': json.dumps(water_data),
        'landfill_waste_data': json.dumps(landfill_waste_data),
        'paper_a4_a3_data': json.dumps(paper_a4_a3_data),
    }
    return render(request, 'frontend/index2.html', context)

def view_pdf(request,id_pdf):
    pdf_url = static(f'pdf/{id_pdf}.pdf')
    return render(request, 'frontend/view_pdf.html',{'pdf_url':pdf_url})

def view_pdf_doc(request,id_pdf):
    pdf_url = static(f'pdf/{id_pdf}.pdf')
    return render(request, 'frontend/view_pdf_doc.html',{'pdf_url':pdf_url})

def view_category(request):
    categories = Category.objects.all()
    issues = Issue.objects.all()
    indicators = Indicator.objects.all()
    evidences = Evidence.objects.all()
    return render(request, 'frontend/view_category.html', {'categories': categories, 'issues': issues, 'indicators': indicators, 'evidences': evidences})

def view_document(request):
    return render(request,'frontend/view_document.html')

def view_promotional(request):
    return render(request,'frontend/view_promotional.html')

def blog_detail(request,id_blog):
    url = f'frontend/blog_detail_{id_blog}.html'
    print(url)
    return render(request,url)

def blog_list(request):
    informations = Information.objects.all().order_by('-date')
    for info in informations:
        info.thai_date = thai_date(info.date)
    return render(request, 'frontend/blog_list.html', {'informations': informations})

def blog_detail(request, pk):
    information = Information.objects.get(pk=pk)
    return render(request, 'frontend/blog_detail.html', {'information': information})

def thai_date(date):
    months = [
        "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
        "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
    ]
    # แปลงวันที่เป็นรูปแบบไทย (วัน เดือน พ.ศ.)
    return "{} {} {}".format(date.day, months[date.month - 1], date.year + 543)  # บวก 543 เพื่อแปลงปี ค.ศ. เป็น พ.ศ.