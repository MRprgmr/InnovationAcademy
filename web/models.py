from datetime import datetime
from io import BytesIO

from PIL.Image import Image
from django.core.files import File
from django.db import models
from django.dispatch import receiver


class Certificate(models.Model):
    full_name = models.CharField(max_length=100, verbose_name="Ism Familiya")
    start_date = models.DateField(verbose_name="Boshlanish sana")
    end_date = models.DateField(verbose_name="Tugash sana")
    created_at = models.DateTimeField(verbose_name="Berilgan sana", auto_now_add=True)
    source_image = models.ImageField(verbose_name="Sertifikat nusxasi", upload_to='', null=True, blank=True)
    certificate_id = models.CharField(max_length=25, verbose_name="Certificate ID", blank=True, null=True, unique=True)

    def __str__(self):
        return self.certificate_id

    def save(self, *args, **kwargs):
        if self.certificate_id is None:
            self.certificate_id = str(int(datetime.now().timestamp()))
        super(Certificate, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Sertifikat"
        verbose_name_plural = "Sertifikatlar"


from utils.certificate_generator import generate_certificate


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
        img.save(fp=f'media/{instance.certificate_id}.jpg')
