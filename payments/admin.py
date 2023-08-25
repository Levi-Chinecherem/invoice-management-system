from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Student, Payment, PaymentCategory, Invoice

# Custom AdminSite class with header and title customization
class CustomAdminSite(AdminSite):
    site_header = 'School Payment Administration'
    site_title = 'School Payment Admin'

# Create instances of the custom admin site
custom_admin_site = CustomAdminSite(name='customadmin')

@admin.register(Student, site=custom_admin_site)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'department', 'level', 'school', 'sex')

@admin.register(Payment, site=custom_admin_site)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'payment_category', 'amount', 'approved')

@admin.register(PaymentCategory, site=custom_admin_site)
class PaymentCategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(Invoice, site=custom_admin_site)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('payment',)
