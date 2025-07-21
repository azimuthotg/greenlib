from django.core.management.base import BaseCommand
from info_graph.models import Year, Month, DataEntry


class Command(BaseCommand):
    help = 'คัดลอกโครงสร้างข้อมูล Year และ Month จากปีหนึ่งไปยังอีกปีหนึ่ง (ไม่คัดลอกข้อมูล DataEntry)'

    def add_arguments(self, parser):
        parser.add_argument('--from-year', type=int, help='ปีต้นทาง (เช่น 2567)', required=True)
        parser.add_argument('--to-year', type=int, help='ปีปลายทาง (เช่น 2568)', required=True)

    def handle(self, *args, **options):
        from_year = options['from_year']
        to_year = options['to_year']

        self.stdout.write(f'กำลังคัดลอกโครงสร้างข้อมูล Info Graph จากปี {from_year} ไปปี {to_year}...')

        # 1. ตรวจสอบปีต้นทาง
        try:
            source_year = Year.objects.get(year=from_year)
            self.stdout.write(f'✅ พบปีต้นทาง: {source_year.year}')
        except Year.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'❌ ไม่พบปีต้นทาง: {from_year}'))
            return

        # 2. สร้างหรือหาปีปลายทาง
        target_year, created = Year.objects.get_or_create(year=to_year)
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'✅ สร้างปีใหม่: {target_year.year}'))
        else:
            self.stdout.write(f'📁 พบปีปลายทาง: {target_year.year}')
            
            # ตรวจสอบว่ามีข้อมูลอยู่แล้วหรือไม่
            existing_months = target_year.month_set.count()
            if existing_months > 0:
                confirm = input(f'⚠ ปี {target_year.year} มีข้อมูล {existing_months} เดือนอยู่แล้ว ต้องการลบและสร้างใหม่? (y/N): ')
                if confirm.lower() != 'y':
                    self.stdout.write('❌ ยกเลิกการดำเนินการ')
                    return
                else:
                    # ลบข้อมูลเก่า (DataEntry จะถูกลบด้วย cascade)
                    target_year.month_set.all().delete()
                    self.stdout.write('🗑 ลบข้อมูลเก่าเรียบร้อย')

        # 3. คัดลอกเดือน (ไม่คัดลอกข้อมูล DataEntry)
        self.stdout.write('📅 เริ่มคัดลอกโครงสร้างเดือน...')
        
        copied_months = 0
        source_months = Month.objects.filter(year=source_year).order_by('month')
        
        for source_month in source_months:
            new_month = Month.objects.create(
                year=target_year,
                month=source_month.month,
                month_name=source_month.month_name
            )
            copied_months += 1
            self.stdout.write(f'  📅 คัดลอกเดือน: {new_month.month_name}')

        # 4. แสดงผลสรุป
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('🎉 คัดลอกโครงสร้างเสร็จสิ้น!'))
        self.stdout.write(f'📊 สรุปผลการดำเนินการ:')
        self.stdout.write(f'   📅 เดือนที่คัดลอก: {copied_months} เดือน')
        self.stdout.write(f'   📥 จากปี: {source_year.year}')
        self.stdout.write(f'   📤 ไปยังปี: {target_year.year}')
        
        self.stdout.write('\n📝 หมายเหตุสำคัญ:')
        self.stdout.write('   ✅ คัดลอกโครงสร้าง Year และ Month เรียบร้อย')
        self.stdout.write('   ❌ ไม่ได้คัดลอกข้อมูล DataEntry (ต้องกรอกข้อมูลใหม่)')
        self.stdout.write('   🔢 ข้อมูลทั้งหมดใน DataEntry จะเป็น 0 หรือว่าง')
        
        self.stdout.write('\n🚀 ขั้นตอนต่อไป:')
        self.stdout.write('   1. เข้า Django Admin → Info Graph → Data Entry')
        self.stdout.write('   2. เพิ่มข้อมูลใหม่สำหรับแต่ละเดือนของปี 2568')
        self.stdout.write('   3. กรอกข้อมูล: ก๊าซเรือนกระจก, ไฟฟ้า, น้ำมันดีเซล, น้ำ, ขยะ, กระดาษ')
        
        self.stdout.write(f'\n🔗 URL Admin: http://localhost:8001/admin/info_graph/dataentry/')
        self.stdout.write('='*50)