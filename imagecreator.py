import io

from PIL import Image, ImageDraw, ImageFont
from parser import formatted_summary_of_year, summary_results_of_year, pretty_event_results, event_results
from driver_standing import driverstandings

# txt = formatted_summary_of_year(summary_results_of_year(2023))
# txt = pretty_event_results(event_results('Italy', 2020, 'Qualifying')[0])
txt = pretty_event_results(driverstandings(2023))


def pretty_image(string: str):
    l_txt = string.split('\n')
    im = Image.new('RGB', (100, 100), color=0)
    fnt = ImageFont.truetype("Courier", size=20)
    draw = ImageDraw.Draw(im)
    textlen = draw.textbbox((0, 0), string, font=fnt)
    im = Image.new('RGB', (textlen[2] + textlen[1], textlen[3] + textlen[1]-17), color=(234, 234, 220, 1))

    draw = ImageDraw.Draw(im)
    w = 0
    count = 0
    for a in l_txt:
        if count % 2 == 0 and count != 0:
            draw.rectangle(xy=((0, w), (im.width, w+20)), fill=(255, 255, 255))
        if count == 1:
            draw.text((10, 10), a, font=fnt, fill=(0, 0, 0))
            w += 3
            count += 1
            continue
        else:
            draw.text((10, w), a, font=fnt, fill=(0, 0, 0))
        w += 20
        count += 1

    image_bytes = io.BytesIO()
    im.save(image_bytes, 'PNG')
    return image_bytes.getvalue()


if __name__ == '__main__':
    data = pretty_image(txt)
    image_bytes = io.BytesIO(data)
    with Image.open(image_bytes) as im:
        im.show()



