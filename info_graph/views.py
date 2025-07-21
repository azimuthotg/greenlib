# info_graph/views.py
from django.shortcuts import render
from django.http import HttpResponse
from info_graph.models import DataEntry,Month,Year
import json

def get_year_filtered_data(request):
    """Helper function to get year-filtered data"""
    selected_year = request.GET.get('year')
    available_years = Year.objects.all().order_by('-year')
    
    if selected_year:
        try:
            current_year_obj = Year.objects.get(year=int(selected_year))
        except (Year.DoesNotExist, ValueError):
            current_year_obj = available_years.first()
    else:
        current_year_obj = available_years.first()
    
    if current_year_obj:
        data_entries = DataEntry.objects.filter(
            month__year=current_year_obj
        ).order_by('month__month')
        current_year_display = current_year_obj.year
    else:
        data_entries = DataEntry.objects.none()
        current_year_display = "ไม่มีข้อมูล"
    
    return data_entries, available_years, current_year_display

def calculate_analysis(data_values, resource_type):
    """คำนวณข้อมูลสำหรับการวิเคราะห์"""
    if not data_values or len(data_values) == 0:
        return {
            'total': 0,
            'average': 0,
            'max_value': 0,
            'min_value': 0,
            'max_month': '',
            'min_month': '',
            'trend': 'ไม่สามารถวิเคราะห์ได้',
            'insight': 'ไม่มีข้อมูลสำหรับการวิเคราะห์'
        }
    
    # กรองข้อมูลที่ไม่เป็น None หรือ 0
    valid_data = [(i, val) for i, val in enumerate(data_values) if val is not None and val > 0]
    
    if not valid_data:
        return {
            'total': 0,
            'average': 0,
            'max_value': 0,
            'min_value': 0,
            'max_month': '',
            'min_month': '',
            'trend': 'ไม่มีการใช้งาน',
            'insight': f'ไม่มีการใช้งาน{resource_type}ในปีนี้'
        }
    
    # คำนวณค่าต่างๆ
    values_only = [val for idx, val in valid_data]
    total = sum(values_only)
    average = total / len(values_only)
    max_value = max(values_only)
    min_value = min(values_only)
    
    # หาเดือนที่มีค่าสูงสุดและต่ำสุด
    max_idx = next(idx for idx, val in valid_data if val == max_value)
    min_idx = next(idx for idx, val in valid_data if val == min_value)
    
    months = ['มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน',
              'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม']
    
    max_month = months[max_idx] if max_idx < len(months) else 'ไม่ระบุ'
    min_month = months[min_idx] if min_idx < len(months) else 'ไม่ระบุ'
    
    # วิเคราะห์แนวโน้ม (เปรียบเทียบ 6 เดือนแรกกับ 6 เดือนหลัง)
    if len(values_only) >= 6:
        first_half = sum(values_only[:6]) / 6
        second_half = sum(values_only[6:]) / len(values_only[6:]) if len(values_only) > 6 else first_half
        
        if second_half > first_half * 1.1:
            trend = 'เพิ่มขึ้น'
        elif second_half < first_half * 0.9:
            trend = 'ลดลง'
        else:
            trend = 'คงที่'
    else:
        trend = 'ข้อมูลไม่เพียงพอ'
    
    # สร้างข้อความวิเคราะห์
    if resource_type in ['ก๊าซเรือนกระจก', 'ขยะฝังกลบ']:
        if trend == 'ลดลง':
            insight = f'การลดลงของ{resource_type}เป็นสิ่งที่ดี แสดงให้เห็นถึงความพยายามในการอนุรักษ์สิ่งแวดล้อม'
        elif trend == 'เพิ่มขึ้น':
            insight = f'การเพิ่มขึ้นของ{resource_type}ควรได้รับการปรับปรุง เพื่อลดผลกระทบต่อสิ่งแวดล้อม'
        else:
            insight = f'การใช้งาน{resource_type}อยู่ในระดับคงที่ ควรมีแผนลดการใช้งานเพิ่มเติม'
    else:
        if trend == 'ลดลง':
            insight = f'การลดลงของการใช้{resource_type}แสดงถึงประสิทธิภาพในการประหยัดพลังงาน'
        elif trend == 'เพิ่มขึ้น':
            insight = f'การเพิ่มขึ้นของการใช้{resource_type}ควรพิจารณาแนวทางประหยัดพลังงาน'
        else:
            insight = f'การใช้{resource_type}อยู่ในระดับคงที่ ควรมีแผนประหยัดพลังงานเพิ่มเติม'
    
    return {
        'total': round(total, 2),
        'average': round(average, 2),
        'max_value': round(max_value, 2),
        'min_value': round(min_value, 2),
        'max_month': max_month,
        'min_month': min_month,
        'trend': trend,
        'insight': insight
    }

def view_graph(request):
    # รับพารามิเตอร์ปีจาก URL
    selected_year = request.GET.get('year')
    
    # ดึงรายการปีทั้งหมด
    available_years = Year.objects.all().order_by('-year')
    
    # กำหนดปีที่เลือก
    if selected_year:
        try:
            current_year_obj = Year.objects.get(year=int(selected_year))
        except (Year.DoesNotExist, ValueError):
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

    labels = [f"{entry.month.month_name}" for entry in data_entries]
    greenhouse_gas_data = [entry.greenhouse_gas for entry in data_entries]
    electricity_data = [entry.electricity for entry in data_entries]
    diesel_data = [entry.diesel for entry in data_entries]
    water_data = [entry.water for entry in data_entries]
    landfill_waste_data = [entry.landfill_waste for entry in data_entries]
    paper_a4_a3_data = [entry.paper_a4_a3 for entry in data_entries]

    # คำนวณค่ารวมและเฉลี่ย
    totals = {}
    averages = {}
    
    if data_entries:
        totals['greenhouse_gas'] = sum(greenhouse_gas_data)
        totals['electricity'] = sum(electricity_data)
        totals['diesel'] = sum(diesel_data)
        totals['water'] = sum(water_data)
        totals['landfill_waste'] = sum(landfill_waste_data)
        totals['paper_a4_a3'] = sum(paper_a4_a3_data)
        
        count = len(data_entries)
        averages['greenhouse_gas'] = totals['greenhouse_gas'] / count if count > 0 else 0
        averages['electricity'] = totals['electricity'] / count if count > 0 else 0
        averages['diesel'] = totals['diesel'] / count if count > 0 else 0
        averages['water'] = totals['water'] / count if count > 0 else 0
        averages['landfill_waste'] = totals['landfill_waste'] / count if count > 0 else 0
        averages['paper_a4_a3'] = totals['paper_a4_a3'] / count if count > 0 else 0
    else:
        totals = {key: 0 for key in ['greenhouse_gas', 'electricity', 'diesel', 'water', 'landfill_waste', 'paper_a4_a3']}
        averages = {key: 0 for key in ['greenhouse_gas', 'electricity', 'diesel', 'water', 'landfill_waste', 'paper_a4_a3']}

    context = {
        'data_entries': data_entries,
        'available_years': available_years,
        'current_year': current_year_display,
        'totals': totals,
        'averages': averages,
        'labels': json.dumps(labels),
        'greenhouse_gas_data': json.dumps(greenhouse_gas_data),
        'electricity_data': json.dumps(electricity_data),
        'diesel_data': json.dumps(diesel_data),
        'water_data': json.dumps(water_data),
        'landfill_waste_data': json.dumps(landfill_waste_data),
        'paper_a4_a3_data': json.dumps(paper_a4_a3_data),
    }
    return render(request,'frontend/view_graph.html',context)

def greenhouse_detail(request):
    data_entries, available_years, current_year = get_year_filtered_data(request)
    
    labels = [f"{entry.month.month_name}" for entry in data_entries]
    data = [entry.greenhouse_gas for entry in data_entries]
    
    # คำนวณการวิเคราะห์
    analysis = calculate_analysis(data, 'ก๊าซเรือนกระจก')
    
    context = {
        'data_entries': data_entries,
        'available_years': available_years,
        'current_year': current_year,
        'labels': json.dumps(labels),
        'data': json.dumps(data),
        'title': 'ข้อมูลก๊าซเรือนกระจก',
        'unit': 'kgCO2e',
        'description': 'ปริมาณการปล่อยก๊าซเรือนกระจกรายเดือน',
        'analysis': analysis,
        'resource_field': 'greenhouse_gas'  # เพิ่มฟิลด์นี้
    }
    return render(request, 'frontend/detail.html', context)

def electricity_detail(request):
    data_entries, available_years, current_year = get_year_filtered_data(request)
    
    labels = [f"{entry.month.month_name}" for entry in data_entries]
    data = [entry.electricity for entry in data_entries]
    
    # คำนวณการวิเคราะห์
    analysis = calculate_analysis(data, 'ไฟฟ้า')
    
    context = {
        'data_entries': data_entries,
        'available_years': available_years,
        'current_year': current_year,
        'labels': json.dumps(labels),
        'data': json.dumps(data),
        'title': 'ข้อมูลการใช้ไฟฟ้า',
        'unit': 'kWh',
        'description': 'ปริมาณการใช้ไฟฟ้ารายเดือน',
        'analysis': analysis,
        'resource_field': 'electricity'
    }
    return render(request, 'frontend/detail.html', context)

def diesel_detail(request):
    data_entries, available_years, current_year = get_year_filtered_data(request)
    
    labels = [f"{entry.month.month_name}" for entry in data_entries]
    data = [entry.diesel for entry in data_entries]
    
    # คำนวณการวิเคราะห์
    analysis = calculate_analysis(data, 'น้ำมันดีเซล')
    
    context = {
        'data_entries': data_entries,
        'available_years': available_years,
        'current_year': current_year,
        'labels': json.dumps(labels),
        'data': json.dumps(data),
        'title': 'ข้อมูลการใช้น้ำมันดีเซล',
        'unit': 'ลิตร',
        'description': 'ปริมาณการใช้น้ำมันดีเซลรายเดือน',
        'analysis': analysis,
        'resource_field': 'diesel'
    }
    return render(request, 'frontend/detail.html', context)

def water_detail(request):
    data_entries, available_years, current_year = get_year_filtered_data(request)
    
    labels = [f"{entry.month.month_name}" for entry in data_entries]
    data = [entry.water for entry in data_entries]
    
    # คำนวณการวิเคราะห์
    analysis = calculate_analysis(data, 'น้ำ')
    
    context = {
        'data_entries': data_entries,
        'available_years': available_years,
        'current_year': current_year,
        'labels': json.dumps(labels),
        'data': json.dumps(data),
        'title': 'ข้อมูลการใช้น้ำ',
        'unit': 'ลูกบาศก์เมตร',
        'description': 'ปริมาณการใช้น้ำรายเดือน',
        'analysis': analysis,
        'resource_field': 'water'
    }
    return render(request, 'frontend/detail.html', context)

def landfill_detail(request):
    data_entries, available_years, current_year = get_year_filtered_data(request)
    
    labels = [f"{entry.month.month_name}" for entry in data_entries]
    data = [entry.landfill_waste for entry in data_entries]
    
    # คำนวณการวิเคราะห์
    analysis = calculate_analysis(data, 'ขยะฝังกลบ')
    
    context = {
        'data_entries': data_entries,
        'available_years': available_years,
        'current_year': current_year,
        'labels': json.dumps(labels),
        'data': json.dumps(data),
        'title': 'ข้อมูลขยะฝังกลบ',
        'unit': 'กิโลกรัม',
        'description': 'ปริมาณขยะฝังกลบรายเดือน',
        'analysis': analysis,
        'resource_field': 'landfill_waste'
    }
    return render(request, 'frontend/detail.html', context)

def paper_detail(request):
    data_entries, available_years, current_year = get_year_filtered_data(request)
    
    labels = [f"{entry.month.month_name}" for entry in data_entries]
    data = [entry.paper_a4_a3 for entry in data_entries]
    
    # คำนวณการวิเคราะห์
    analysis = calculate_analysis(data, 'กระดาษ')
    
    context = {
        'data_entries': data_entries,
        'available_years': available_years,
        'current_year': current_year,
        'labels': json.dumps(labels),
        'data': json.dumps(data),
        'title': 'ข้อมูลการใช้กระดาษ A4/A3',
        'unit': 'กิโลกรัม (1รีม=2.5กก.)',
        'description': 'ปริมาณการใช้กระดาษรายเดือน',
        'analysis': analysis,
        'resource_field': 'paper_a4_a3'
    }
    return render(request, 'frontend/detail.html', context)