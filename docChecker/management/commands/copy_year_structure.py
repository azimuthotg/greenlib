from django.core.management.base import BaseCommand
from docChecker.models import Year, CategoryGroup, Category, Issue, Indicator


class Command(BaseCommand):
    help = 'คัดลอกโครงสร้างข้อมูล (CategoryGroup, Category, Issue, Indicator) จากปีหนึ่งไปยังอีกปีหนึ่ง ไม่รวม Evidence'

    def add_arguments(self, parser):
        parser.add_argument('--from-year', type=str, help='ปีต้นทาง (เช่น 2567)', required=True)
        parser.add_argument('--to-year', type=str, help='ปีปลายทาง (เช่น 2568)', required=True)
        parser.add_argument('--to-year-desc', type=str, help='คำอธิบายปีปลายทาง', default='')

    def handle(self, *args, **options):
        from_year_name = options['from_year']
        to_year_name = options['to_year']
        to_year_desc = options['to_year_desc'] or f'ปีการศึกษา {to_year_name}'

        # ตรวจสอบปีต้นทาง
        try:
            source_year = Year.objects.get(year_name__contains=from_year_name)
            self.stdout.write(f'พบปีต้นทาง: {source_year.year_name}')
        except Year.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'ไม่พบปีต้นทาง: {from_year_name}'))
            return

        # สร้างหรือหาปีปลายทาง
        target_year, created = Year.objects.get_or_create(
            year_name__contains=to_year_name,
            defaults={'year_name': f'ปีการศึกษา {to_year_name}', 'year_description': to_year_desc}
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'สร้างปีใหม่: {target_year.year_name}'))
        else:
            self.stdout.write(f'พบปีปลายทาง: {target_year.year_name}')
            
            # ตรวจสอบว่ามีข้อมูลอยู่แล้วหรือไม่
            existing_groups = target_year.category_groups.count()
            if existing_groups > 0:
                confirm = input(f'ปี {target_year.year_name} มีข้อมูล {existing_groups} กลุ่มหมวดอยู่แล้ว ต้องการลบและสร้างใหม่? (y/N): ')
                if confirm.lower() != 'y':
                    self.stdout.write('ยกเลิกการดำเนินการ')
                    return
                else:
                    # ลบข้อมูลเก่า (Evidence จะถูกลบตาม cascade)
                    target_year.category_groups.all().delete()
                    self.stdout.write('ลบข้อมูลเก่าเรียบร้อย')

        # เริ่มคัดลอกข้อมูล
        self.stdout.write('เริ่มคัดลอกข้อมูล...')
        
        copied_groups = 0
        copied_categories = 0
        copied_issues = 0
        copied_indicators = 0

        for source_group in source_year.category_groups.all():
            # คัดลอก CategoryGroup
            new_group = CategoryGroup.objects.create(
                year=target_year,
                group_name=source_group.group_name,
                group_description=source_group.group_description
            )
            copied_groups += 1
            self.stdout.write(f'  คัดลอกกลุ่ม: {new_group.group_name}')

            for source_category in source_group.categories.all():
                # คัดลอก Category
                new_category = Category.objects.create(
                    category_group=new_group,
                    category_name=source_category.category_name,
                    category_description=source_category.category_description
                )
                copied_categories += 1

                for source_issue in source_category.issues.all():
                    # คัดลอก Issue
                    new_issue = Issue.objects.create(
                        category=new_category,
                        issue_name=source_issue.issue_name,
                        issue_description=source_issue.issue_description
                    )
                    copied_issues += 1

                    for source_indicator in source_issue.indicators.all():
                        # คัดลอก Indicator (ไม่คัดลอก Evidence)
                        new_indicator = Indicator.objects.create(
                            issue=new_issue,
                            indicator_name=source_indicator.indicator_name,
                            indicator_description=source_indicator.indicator_description
                        )
                        copied_indicators += 1

        # แสดงผลสรุป
        self.stdout.write(self.style.SUCCESS('\nคัดลอกข้อมูลเสร็จสิ้น!'))
        self.stdout.write(f'กลุ่มหมวด: {copied_groups} รายการ')
        self.stdout.write(f'หมวดหมู่: {copied_categories} รายการ')
        self.stdout.write(f'ประเด็น: {copied_issues} รายการ')
        self.stdout.write(f'ตัวชี้วัด: {copied_indicators} รายการ')
        self.stdout.write(f'\nคัดลอกจาก: {source_year.year_name}')
        self.stdout.write(f'ไปยัง: {target_year.year_name}')
        self.stdout.write(self.style.WARNING('\nหมายเหตุ: Evidence (หลักฐาน) ไม่ได้ถูกคัดลอก ต้องแนบใหม่สำหรับปี 2568'))