# info_graph/management/commands/create_year_2568.py
from django.core.management.base import BaseCommand
from info_graph.models import Year, Month, DataEntry
from greenweb.models import Year as GreenYear, Category as GreenCategory, Issue as GreenIssue, Indicator as GreenIndicator, Evidence as GreenEvidence
from docChecker.models import Year as DocYear, CategoryGroup, Category as DocCategory, Issue as DocIssue, Indicator as DocIndicator, Evidence as DocEvidence

class Command(BaseCommand):
    help = 'สร้างโครงสร้างข้อมูลปี 2568 จากปี 2567 (ยกเว้นหลักฐาน)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 เริ่มต้นการสร้างโครงสร้างข้อมูลปี 2568...'))
        
        try:
            # 1. สร้างปี 2568 สำหรับทุก app
            self.stdout.write('📅 สร้างปี 2568 สำหรับแต่ละ app...')
            
            # info_graph
            info_year_2568, created = Year.objects.get_or_create(year=2568)
            self.stdout.write(f'   ✅ info_graph Year 2568: {"สร้างใหม่" if created else "มีอยู่แล้ว"}')
            
            # greenweb
            green_year_2568, created = GreenYear.objects.get_or_create(year=2568)
            self.stdout.write(f'   ✅ greenweb Year 2568: {"สร้างใหม่" if created else "มีอยู่แล้ว"}')
            
            # docChecker
            doc_year_2568, created = DocYear.objects.get_or_create(
                year_name='2568',
                defaults={
                    'year_description': 'ปีงบประมาณ พ.ศ. 2568 (ตุลาคม 2567 - กันยายน 2568)'
                }
            )
            self.stdout.write(f'   ✅ docChecker Year 2568: {"สร้างใหม่" if created else "มีอยู่แล้ว"}')

            # 2. สร้าง Month สำหรับ info_graph ปี 2568
            self.stdout.write('\n📊 สร้าง Month สำหรับ info_graph...')
            months_data = [
                (1, 'มกราคม'), (2, 'กุมภาพันธ์'), (3, 'มีนาคม'), (4, 'เมษายน'),
                (5, 'พฤษภาคม'), (6, 'มิถุนายน'), (7, 'กรกฎาคม'), (8, 'สิงหาคม'),
                (9, 'กันยายน'), (10, 'ตุลาคม'), (11, 'พฤศจิกายน'), (12, 'ธันวาคม')
            ]

            for month_num, month_name in months_data:
                month_obj, created = Month.objects.get_or_create(
                    year=info_year_2568,
                    month=month_num,
                    defaults={'month_name': month_name}
                )
                self.stdout.write(f'   📅 {month_name}: {"สร้างใหม่" if created else "มีอยู่แล้ว"}')

            # 3. สร้าง DataEntry เปล่าสำหรับ info_graph ปี 2568
            self.stdout.write('\n📈 สร้าง DataEntry เปล่าสำหรับ info_graph...')
            for month_obj in Month.objects.filter(year=info_year_2568):
                data_entry, created = DataEntry.objects.get_or_create(
                    month=month_obj,
                    defaults={
                        'greenhouse_gas': 0,
                        'electricity': 0,
                        'diesel': 0,
                        'water': 0,
                        'landfill_waste': 0,
                        'paper_a4_a3': 0
                    }
                )
                self.stdout.write(f'   📊 DataEntry {month_obj.month_name}: {"สร้างใหม่" if created else "มีอยู่แล้ว"}')

            # 4. Copy โครงสร้าง greenweb จากปี 2567 ไปปี 2568
            self.stdout.write('\n🌿 คัดลอกโครงสร้าง greenweb จากปี 2567 ไปปี 2568...')
            green_year_2567 = GreenYear.objects.filter(year=2567).first()

            if green_year_2567:
                categories_2567 = GreenCategory.objects.filter(year=green_year_2567)
                
                for cat_2567 in categories_2567:
                    # สร้าง Category ใหม่สำหรับปี 2568
                    cat_2568, created = GreenCategory.objects.get_or_create(
                        year=green_year_2568,
                        category_name=cat_2567.category_name,
                        defaults={'order': cat_2567.order}
                    )
                    self.stdout.write(f'   📁 Category: {cat_2567.category_name} ({"สร้างใหม่" if created else "มีอยู่แล้ว"})')
                    
                    # คัดลอก Issues
                    issues_2567 = GreenIssue.objects.filter(category=cat_2567)
                    for issue_2567 in issues_2567:
                        issue_2568, created = GreenIssue.objects.get_or_create(
                            category=cat_2568,
                            issue_name=issue_2567.issue_name,
                            defaults={'order': issue_2567.order}
                        )
                        self.stdout.write(f'     📝 Issue: {issue_2567.issue_name} ({"สร้างใหม่" if created else "มีอยู่แล้ว"})')
                        
                        # คัดลอก Indicators
                        indicators_2567 = GreenIndicator.objects.filter(issue=issue_2567)
                        for indicator_2567 in indicators_2567:
                            indicator_2568, created = GreenIndicator.objects.get_or_create(
                                issue=issue_2568,
                                indicator_name=indicator_2567.indicator_name,
                                defaults={'order': indicator_2567.order}
                            )
                            self.stdout.write(f'       🎯 Indicator: {indicator_2567.indicator_name} ({"สร้างใหม่" if created else "มีอยู่แล้ว"})')
            else:
                self.stdout.write(self.style.WARNING('   ⚠️  ไม่พบข้อมูลปี 2567 ใน greenweb'))

            # 5. Copy โครงสร้าง docChecker จากปี 2567 ไปปี 2568
            self.stdout.write('\n📋 คัดลอกโครงสร้าง docChecker จากปี 2567 ไปปี 2568...')
            doc_year_2567 = DocYear.objects.filter(year_name='2567').first()

            if doc_year_2567:
                # คัดลอก CategoryGroups
                cat_groups_2567 = CategoryGroup.objects.filter(year=doc_year_2567)
                
                for group_2567 in cat_groups_2567:
                    group_2568, created = CategoryGroup.objects.get_or_create(
                        year=doc_year_2568,
                        group_name=group_2567.group_name,
                        defaults={'group_description': group_2567.group_description}
                    )
                    self.stdout.write(f'   📂 CategoryGroup: {group_2567.group_name} ({"สร้างใหม่" if created else "มีอยู่แล้ว"})')
                    
                    # คัดลอก Categories
                    categories_2567 = DocCategory.objects.filter(category_group=group_2567)
                    for cat_2567 in categories_2567:
                        cat_2568, created = DocCategory.objects.get_or_create(
                            category_group=group_2568,
                            category_name=cat_2567.category_name,
                            defaults={'category_description': cat_2567.category_description}
                        )
                        self.stdout.write(f'     📁 Category: {cat_2567.category_name} ({"สร้างใหม่" if created else "มีอยู่แล้ว"})')
                        
                        # คัดลอก Issues
                        issues_2567 = DocIssue.objects.filter(category=cat_2567)
                        for issue_2567 in issues_2567:
                            issue_2568, created = DocIssue.objects.get_or_create(
                                category=cat_2568,
                                issue_name=issue_2567.issue_name,
                                defaults={'issue_description': issue_2567.issue_description}
                            )
                            self.stdout.write(f'       📝 Issue: {issue_2567.issue_name} ({"สร้างใหม่" if created else "มีอยู่แล้ว"})')
                            
                            # คัดลอก Indicators
                            indicators_2567 = DocIndicator.objects.filter(issue=issue_2567)
                            for indicator_2567 in indicators_2567:
                                indicator_2568, created = DocIndicator.objects.get_or_create(
                                    issue=issue_2568,
                                    indicator_name=indicator_2567.indicator_name,
                                    defaults={'indicator_description': indicator_2567.indicator_description}
                                )
                                self.stdout.write(f'         🎯 Indicator: {indicator_2567.indicator_name} ({"สร้างใหม่" if created else "มีอยู่แล้ว"})')
            else:
                self.stdout.write(self.style.WARNING('   ⚠️  ไม่พบข้อมูลปี 2567 ใน docChecker'))

            # 6. สรุปผลลัพธ์
            self.stdout.write(f'\n{"="*60}')
            self.stdout.write(self.style.SUCCESS('✅ เสร็จสิ้นการสร้างโครงสร้างข้อมูลปี 2568'))
            
            # นับจำนวนข้อมูลที่สร้าง
            info_months = Month.objects.filter(year=info_year_2568).count()
            info_data_entries = DataEntry.objects.filter(month__year=info_year_2568).count()
            green_categories = GreenCategory.objects.filter(year=green_year_2568).count()
            green_issues = GreenIssue.objects.filter(category__year=green_year_2568).count()
            green_indicators = GreenIndicator.objects.filter(issue__category__year=green_year_2568).count()
            doc_groups = CategoryGroup.objects.filter(year=doc_year_2568).count()
            doc_categories = DocCategory.objects.filter(category_group__year=doc_year_2568).count()
            doc_issues = DocIssue.objects.filter(category__category_group__year=doc_year_2568).count()
            doc_indicators = DocIndicator.objects.filter(issue__category__category_group__year=doc_year_2568).count()
            
            self.stdout.write(f'\n📊 สถิติข้อมูลที่สร้าง:')
            self.stdout.write(f'   📅 info_graph: {info_months} เดือน, {info_data_entries} DataEntry')
            self.stdout.write(f'   🌿 greenweb: {green_categories} Categories, {green_issues} Issues, {green_indicators} Indicators')
            self.stdout.write(f'   📋 docChecker: {doc_groups} Groups, {doc_categories} Categories, {doc_issues} Issues, {doc_indicators} Indicators')
            
            self.stdout.write(f'\n📝 หมายเหตุ: หลักฐาน (Evidence) ไม่ได้คัดลอกมา ต้องอัพโหลดใหม่')
            self.stdout.write(self.style.SUCCESS(f'{"="*60}'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ เกิดข้อผิดพลาด: {str(e)}'))
            raise e