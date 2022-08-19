import locale
import textwrap
from string import ascii_letters

import qrcode
import os
from PIL import Image, ImageDraw, ImageFont
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import RadialGradiantColorMask
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer

from InnovationAcademy.settings import STATIC_ROOT
from web.models import Certificate


def ordinal_date(day: int):
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]
    return f"{day}{suffix}"


def generate_certificate(certificate: Certificate):
    img = Image.open(fp=os.path.join(STATIC_ROOT, 'certificate_template.jpg'), mode='r')
    draw = ImageDraw.Draw(im=img)

    full_name = certificate.full_name.upper()
    sd = certificate.start_date
    ed = certificate.end_date
    gd = certificate.created_at

    locale.setlocale(locale.LC_TIME, 'uz_UZ')
    text_uz = f"""{sd.strftime("%Y-yil %d-%Bdan")} {ed.strftime("%d-%Bgacha")} Innovation Academy markazida 32 soatli “Axborot-kommunikatsiya texnologiyalari” kursini muvaffaqiyatli yakunladi. """
    g_date_uz = f"Berilgan sana: {gd.strftime('%d - %B %Y')} y."

    locale.setlocale(locale.LC_TIME, 'en_US')
    text_en = f"""has successfully completed the course of "Information Technologies" conducted by Innovation Academy Center from {ordinal_date(sd.day)} of {sd.strftime('%B')} to {ordinal_date(ed.day)} of {sd.strftime('%B in %Y')}"""
    g_date_en = f"Given date: {gd.strftime('%d - %B %Y')} y."

    font = ImageFont.truetype(font=os.path.join(STATIC_ROOT, 'fonts/rockb.ttf'), size=100)

    tw, th = draw.textsize(text=full_name, font=font)
    draw.text(xy=(880, 920), text=full_name, font=font, fill='#000000', anchor='mm', align='center')
    draw.line((880 - tw // 2, 920 + th // 2, 880 + tw // 2, 920 + th // 2), fill='#000000', width=6)
    draw.text(xy=(2600, 920), text=full_name, font=font, fill='#000000', anchor='mm', align='center')
    draw.line((2600 - tw // 2, 920 + th // 2, 2600 + tw // 2, 920 + th // 2), fill='#000000', width=6)

    avg_char_width = sum(font.getlength(char) for char in ascii_letters) / len(ascii_letters)
    max_char_count = int(2600 / avg_char_width)

    font = ImageFont.truetype(font=os.path.join(STATIC_ROOT, 'fonts/rock.ttf'), size=70)

    text = textwrap.fill(text=text_uz, width=max_char_count)
    draw.text(xy=(880, 1200), text=text, font=font, fill='#000000', anchor='mm', spacing=25, align='center')

    text = textwrap.fill(text=text_en, width=max_char_count)
    draw.text(xy=(2600, 1200), text=text, font=font, fill='#000000', anchor='mm', spacing=25, align='center')

    font = ImageFont.truetype(font=os.path.join(STATIC_ROOT, 'fonts/rockb.ttf'), size=50)

    draw.text(xy=(200, 1800), text=g_date_uz, font=font, fill='#000000', align='center')
    draw.text(xy=(1920, 1800), text=g_date_en, font=font, fill='#000000', align='center')

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=1)
    qr.add_data(f"http://innovation-avademy.uz/certificate/{certificate.certificate_id}")
    img_qr = qr.make_image(image_factory=StyledPilImage, color_mask=RadialGradiantColorMask(),
                           module_drawer=RoundedModuleDrawer())
    img.paste(img_qr, (img.size[0] - img_qr.size[0] - 130, img.size[1] - img_qr.size[1] - 220))

    font = ImageFont.truetype(font=os.path.join(STATIC_ROOT, 'fonts/rockb.ttf'), size=45)
    draw.text(xy=(img.size[0] - 118 - img_qr.size[0], img.size[1] - 230), text=f"ID{certificate.certificate_id}",
              font=font, fill='#0000AA')

    return img
