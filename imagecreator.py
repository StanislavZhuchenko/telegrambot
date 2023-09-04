from PIL import Image, ImageDraw, ImageFont
from parser import formatted_summary_of_year, summary_results_of_year, pretty_event_results, event_results
from driver_standing import driverstandings

# txt = formatted_summary_of_year(summary_results_of_year(2023))
# txt = pretty_event_results(event_results('Italy', 2020, 'Qualifying')[0])
txt = pretty_event_results(driverstandings(2023))


def pretty_image(string: str):
    l_txt = string.split('\n')
    im = Image.new('RGB', (100, 100), color=0)
    fnt = ImageFont.truetype("Courier", size=40)
    draw = ImageDraw.Draw(im)
    textlen = draw.textbbox((0, 0), string, font=fnt)
    im = Image.new('RGB', (textlen[2] + textlen[1], textlen[3] + textlen[1] + 10), color=0)

    draw = ImageDraw.Draw(im)
    w = 10
    for a in l_txt:
        draw.text((10, w), a, font=fnt, fill=(255, 255, 255))
        w += 35

    im.save("test.png")
    return im


if __name__ == '__main__':
    pretty_image(txt)
