import os
from datetime import datetime
from io import BytesIO

from PIL.Image import Image
from django.core.files import File
from django.db import models
from django.dispatch import receiver
from django.utils.safestring import mark_safe

from InnovationAcademy.settings import BASE_DIR


class Certificate(models.Model):
    full_name = models.CharField(max_length=100, verbose_name="Ism Familiya")
    start_date = models.DateField(verbose_name="Boshlanish sana")
    end_date = models.DateField(verbose_name="Tugash sana")
    created_at = models.DateTimeField(verbose_name="Berilgan sana", auto_now_add=True)
    certificate_number = models.IntegerField(verbose_name="Sertifikat nomeri", unique=True)
    given_date = models.DateField(verbose_name="Berilgan sanasi")
    source_image = models.ImageField(verbose_name="Sertifikat nusxasi", upload_to='', null=True, blank=True)
    certificate_id = models.CharField(max_length=25, verbose_name="Certificate ID", blank=True, null=True, unique=True)

    def __str__(self):
        return self.certificate_id

    def save(self, *args, **kwargs):
        if self.certificate_id is None:
            self.certificate_id = str(int(datetime.now().timestamp()))
        super(Certificate, self).save(*args, **kwargs)

    @property
    def formatted_number(self):
        if self.certificate_number:
            return '0' * (6 - len(str(self.certificate_number))) + str(self.certificate_number)
        else:
            return ""

    def certificate_download(self):
        return mark_safe('<a href="/certificate/{0}.jpg" download>{1}</a>'.format(
            self.certificate_id, self.formatted_number))

    certificate_download.short_description = 'Download Certificate'

    class Meta:
        verbose_name = "Sertifikat"
        verbose_name_plural = "Sertifikatlar"


from web.utils.certificate_generator import generate_certificate


@receiver(models.signals.post_save, sender=Certificate)
def create_certificate(sender, instance: Certificate, *args, **kwargs):
    img: Image = generate_certificate(instance)
    if not instance.source_image:
        image_file = BytesIO()
        img.save(image_file, img.format)
        instance.source_image.save(
            f"{instance.certificate_id}.jpg",
            File(image_file),
            save=True
        )
    else:
        img.save(fp=os.path.join(BASE_DIR, f'media/{instance.certificate_id}.jpg'))
