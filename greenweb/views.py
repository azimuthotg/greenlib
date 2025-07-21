from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
#from greenweb.models import Category,Year, Issue, Indicator, Evidence
from info_graph.models import DataEntry,Month,Year
import json
from django.templatetags.static import static
from blogs.models import Information
from docChecker.models import Year, CategoryGroup, Category, Issue, Indicator, Evidence

def view_group(request, group_name, year_name=None):
    if year_name:
        # หาปีที่ระบุ
        year = get_object_or_404(Year, year_name__contains=year_name)
        category_group = get_object_or_404(CategoryGroup, group_name=group_name, year=year)
    else:
        # ใช้ปีล่าสุด (เริ่มต้น)
        latest_year = Year.objects.order_by('-year_id').first()
        if latest_year:
            category_group = get_object_or_404(CategoryGroup, group_name=group_name, year=latest_year)
        else:
            category_group = get_object_or_404(CategoryGroup, group_name=group_name)
    
    categories = category_group.categories.all()
    
    # ส่งรายการปีทั้งหมดไปยัง template สำหรับ dropdown
    all_years = Year.objects.all().order_by('-year_id')

    context = {
        'category_group': category_group,
        'categories': categories,
        'all_years': all_years,
        'current_year': category_group.year,
    }

    return render(request, 'frontend/view_group.html', context)

def index2(request, selected_year=None):
    # เอาข้อมูลใน information ทั้งหมด เอาแค่ 3 record และเรียงตามวันที่ล่าสุด
    informations = Information.objects.all().order_by('-date')[:3]

    # ดึงรายการปีทั้งหมด
    from info_graph.models import Year as InfoYear
    available_years = InfoYear.objects.all().order_by('-year')
    
    # กำหนดปีที่เลือก
    if selected_year:
        try:
            current_year_obj = InfoYear.objects.get(year=selected_year)
        except InfoYear.DoesNotExist:
            current_year_obj = available_years.first()
    else:
        # ถ้าไม่ระบุปี ใช้ปีล่าสุด
        current_year_obj = available_years.first()
    
    # เอาข้อมูลใน DataEntry ของปีที่เลือก และเรียงตามเดือน
    if current_year_obj:
        data_entries = DataEntry.objects.filter(
            month__year=current_year_obj
        ).order_by('month__month')
        current_year_display = current_year_obj.year
    else:
        data_entries = DataEntry.objects.none()
        current_year_display = "ไม่มีข้อมูล"
    
    # สร้างข้อมูลสำหรับกราฟ
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
        'available_years': available_years,
        'current_year': current_year_display,
        'labels': json.dumps(labels),
        'greenhouse_gas_data': json.dumps(greenhouse_gas_data),
        'electricity_data': json.dumps(electricity_data),
        'diesel_data': json.dumps(diesel_data),
        'water_data': json.dumps(water_data),
        'landfill_waste_data': json.dumps(landfill_waste_data),
        'paper_a4_a3_data': json.dumps(paper_a4_a3_data),
    }
    return render(request, 'frontend/index2.html', context)

def get_chart_data_ajax(request, year):
    """AJAX endpoint สำหรับดึงข้อมูลกราฟตามปี"""
    try:
        from info_graph.models import Year as InfoYear
        
        # หาปีที่ระบุ
        year_obj = InfoYear.objects.get(year=year)
        
        # เอาข้อมูลใน DataEntry ของปีที่เลือก
        data_entries = DataEntry.objects.filter(
            month__year=year_obj
        ).order_by('month__month')
        
        # สร้างข้อมูลสำหรับกราฟ
        chart_data = {
            'labels': [entry.month.month_name for entry in data_entries],
            'greenhouse_gas_data': [entry.greenhouse_gas for entry in data_entries],
            'electricity_data': [entry.electricity for entry in data_entries],
            'diesel_data': [entry.diesel for entry in data_entries],
            'water_data': [entry.water for entry in data_entries],
            'landfill_waste_data': [entry.landfill_waste for entry in data_entries],
            'paper_a4_a3_data': [entry.paper_a4_a3 for entry in data_entries],
            'current_year': year,
            'success': True
        }
        
        return JsonResponse(chart_data)
        
    except InfoYear.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': f'ไม่พบข้อมูลปี {year}'
        })
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'error': str(e)
        })

def view_pdf(request,id_pdf):
    pdf_url = static(f'pdf/{id_pdf}.pdf')
    return render(request, 'frontend/view_pdf.html',{'pdf_url':pdf_url})

def view_pdf_doc(request,id_pdf):
    pdf_url = static(f'pdf/{id_pdf}.pdf')
    print(pdf_url)
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
    # Redirect ไปยังระบบสื่อประชาสัมพันธ์ใหม่
    from django.shortcuts import redirect
    return redirect('promotional:list')

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