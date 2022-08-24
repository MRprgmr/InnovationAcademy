from django.contrib import admin

from web.models import Certificate


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'certificate_number', 'given_date', 'source_image', 'certificate_download']
    readonly_fields = ['certificate_id', 'source_image', 'certificate_download']
    search_fields = ['certificate_number', 'certificate_id']
    list_per_page = 20
