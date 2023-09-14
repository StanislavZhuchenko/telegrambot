import io

from PIL import Image, ImageDraw, ImageFont
from parser import formatted_summary_of_year, summary_results_of_year, pretty_event_results, event_results
from driver_standing import driverstandings
from features import time_execution

# txt = formatted_summary_of_year(summary_results_of_year(2023))
# txt = pretty_event_results(event_results('Austria', 2023, 'Sprint grid'))
txt = pretty_event_results(driverstandings(2002))

@time_execution
def pretty_image(string: str):
    l_txt = string.split('\n')
    im = Image.new('RGB', (100, 100), color=0)
    size_font = 20
    fnt = ImageFont.truetype("Courier New.ttf", size=size_font)
    draw = ImageDraw.Draw(im)

    textlen = draw.textbbox((0, 0), string, font=fnt)  # draw textbox to update size of image
    im = Image.new('RGB', (textlen[2] + textlen[1], textlen[3] - int((size_font/2))), color=(234, 234, 220, 1))
    draw = ImageDraw.Draw(im)

    w = 0
    count = 0
    for a in l_txt:
        # first line
        if count == 0:
            draw.text((10, 10), a.upper(), font=ImageFont.truetype("Courier New Bold.ttf", size=size_font-3), fill=(0, 0, 0))
        # second line
        elif count == 1:
            draw.text((10, w + size_font), a, font=fnt, fill=(0, 0, 0))
        # third line
        elif count == 2:
            draw.text((10, w + (size_font/2)), a, font=fnt, fill=(0, 0, 0))
            w += 3
            count += 1
        # line more than 3
        elif count > 2:
            if count % 2 == 0:
                # draw zebra
                draw.rectangle(xy=((0, w), (im.width, w + size_font)), fill=(255, 255, 255))
            draw.text((10, w), a, font=fnt, fill=(0, 0, 0))

        w += size_font
        count += 1

    image_bytes = io.BytesIO()
    im.save(image_bytes, 'jpeg')
    return image_bytes.getvalue()


if __name__ == '__main__':
    data = pretty_image(txt)
    image_bytes = io.BytesIO(data)
    with Image.open(image_bytes) as im:
        im.show()



