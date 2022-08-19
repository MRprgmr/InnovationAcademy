from django.contrib import admin

from web.models import Certificate


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'certificate_id', 'created_at', 'source_image']
    readonly_fields = ['created_at', 'certificate_id', 'source_image']
