from django.contrib import admin

from web.models import Certificate


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'certificate_number', 'given_date', 'source_image', 'certificate_download']
    readonly_fields = ['certificate_id', 'source_image', 'certificate_download']
    search_fields = ['certificate_number']
    list_per_page = 20

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(CertificateAdmin, self).get_search_results(request, queryset, search_term)
        try:
            search_term_as_int = int(search_term)
        except ValueError:
            pass
        else:
            queryset = self.model.objects.filter(certificate_number=search_term_as_int)
        return queryset, use_distinct
