from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from promotional.models import PromotionalCategory, PromotionalImage


class Command(BaseCommand):
    help = 'สร้าง Group และ User สำหรับอัพโหลดสื่อประชาสัมพันธ์เท่านั้น'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='ชื่อผู้ใช้', default='uploader')
        parser.add_argument('--password', type=str, help='รหัสผ่าน', default='upload123')
        parser.add_argument('--email', type=str, help='อีเมล', default='uploader@npu.ac.th')
        parser.add_argument('--first-name', type=str, help='ชื่อจริง', default='Upload')
        parser.add_argument('--last-name', type=str, help='นามสกุล', default='User')

    def handle(self, *args, **options):
        # ข้อมูล user
        username = options['username']
        password = options['password']
        email = options['email']
        first_name = options['first_name']
        last_name = options['last_name']

        self.stdout.write('กำลังสร้าง Group และ User สำหรับอัพโหลดสื่อประชาสัมพันธ์...')

        # 1. สร้าง Group สำหรับ Upload User
        upload_group, created = Group.objects.get_or_create(
            name='Promotional Upload Users'
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('✅ สร้าง Group "Promotional Upload Users" เรียบร้อย'))
        else:
            self.stdout.write('📁 Group "Promotional Upload Users" มีอยู่แล้ว')

        # 2. กำหนด permissions ที่จำเป็น
        # สำหรับ PromotionalCategory
        category_ct = ContentType.objects.get_for_model(PromotionalCategory)
        category_permissions = [
            'view_promotionalcategory',
        ]

        # สำหรับ PromotionalImage  
        image_ct = ContentType.objects.get_for_model(PromotionalImage)
        image_permissions = [
            'add_promotionalimage',
            'change_promotionalimage', 
            'view_promotionalimage',
            'delete_promotionalimage',  # ให้ลบรูปที่ตัวเองอัพโหลดได้
        ]

        # เพิ่ม permissions เข้า group
        all_permissions = []
        
        # Category permissions
        for perm_name in category_permissions:
            try:
                perm = Permission.objects.get(
                    content_type=category_ct,
                    codename=perm_name
                )
                all_permissions.append(perm)
                self.stdout.write(f'  ✓ เพิ่ม permission: {perm_name}')
            except Permission.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  ⚠ ไม่พบ permission: {perm_name}'))

        # Image permissions
        for perm_name in image_permissions:
            try:
                perm = Permission.objects.get(
                    content_type=image_ct,
                    codename=perm_name
                )
                all_permissions.append(perm)
                self.stdout.write(f'  ✓ เพิ่ม permission: {perm_name}')
            except Permission.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  ⚠ ไม่พบ permission: {perm_name}'))

        # เพิ่ม permissions ให้ group
        upload_group.permissions.set(all_permissions)
        self.stdout.write(f'📋 เพิ่ม {len(all_permissions)} permissions ให้ group')

        # 3. สร้าง User
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'⚠ User "{username}" มีอยู่แล้ว'))
            user = User.objects.get(username=username)
            # อัพเดทข้อมูล
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.is_staff = True  # ให้เข้า admin ได้
            user.is_active = True
            user.save()
            self.stdout.write('📝 อัพเดทข้อมูล user')
        else:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_staff=True,  # ให้เข้า admin ได้
                is_active=True
            )
            self.stdout.write(self.style.SUCCESS(f'✅ สร้าง User "{username}" เรียบร้อย'))

        # 4. เพิ่ม user เข้า group
        user.groups.add(upload_group)
        self.stdout.write(f'👥 เพิ่ม user "{username}" เข้า group')

        # 5. แสดงสรุป
        self.stdout.write(self.style.SUCCESS('\n🎉 สร้าง Upload User เสร็จสิ้น!'))
        self.stdout.write('📋 รายละเอียด:')
        self.stdout.write(f'   👤 Username: {username}')
        self.stdout.write(f'   🔑 Password: {password}')
        self.stdout.write(f'   📧 Email: {email}')
        self.stdout.write(f'   📛 ชื่อ: {first_name} {last_name}')
        self.stdout.write(f'   👥 Group: {upload_group.name}')
        
        self.stdout.write('\n📝 สิทธิ์ที่ได้รับ:')
        self.stdout.write('   ✅ ดูหมวดหมู่สื่อประชาสัมพันธ์')
        self.stdout.write('   ✅ เพิ่มรูปภาพสื่อประชาสัมพันธ์')
        self.stdout.write('   ✅ แก้ไขรูปภาพสื่อประชาสัมพันธ์')
        self.stdout.write('   ✅ ลบรูปภาพสื่อประชาสัมพันธ์')
        self.stdout.write('   ✅ ดูรูปภาพสื่อประชาสัมพันธ์')
        
        self.stdout.write('\n🚀 ขั้นตอนต่อไป:')
        self.stdout.write('   1. เข้า Django Admin ด้วย username/password ด้านบน')
        self.stdout.write('   2. จะเห็นเฉพาะเมนู "สื่อประชาสัมพันธ์"')
        self.stdout.write('   3. สามารถอัพโหลดและจัดการรูปภาพได้เลย!')
        
        self.stdout.write(f'\n🔗 URL: http://localhost:8001/admin/')
        self.stdout.write('\n⚠ หมายเหตุ: User นี้ไม่สามารถเข้าถึงข้อมูลอื่นในระบบได้')