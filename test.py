
# from PIL import Image, ImageDraw, ImageFont
#
# # create an image
# out = Image.new("RGB", (150, 100), (255, 255, 255))
#
# # get a font
# fnt = ImageFont.truetype("Arial Unicode.ttf", size=40)
# # get a drawing context
# d = ImageDraw.Draw(out)
#
# # draw multiline text
# d.multiline_text((10, 5), "Hello\nWorld", font=fnt, fill=(0, 0, 0))
#
# # out.show()
#
# width, height = (400, 400)
# image = Image.new("RGB", (width, height), "grey")
# draw = ImageDraw.Draw(image)
# font = ImageFont.truetype("Swis721 LtEx BT Light.ttf", size=12)
# text = "Hello\nWorld"
# font_width = fnt.getbbox(text)
# print(font_width)


from PIL import Image, ImageDraw, ImageFont
from parser import formatted_summary_of_year, summary_results_of_year, pretty_event_results, event_results
from driver_standing import driverstandings

# txt = formatted_summary_of_year(summary_results_of_year(2023))
# txt = pretty_event_results(event_results('Italy', 2020, 'Qualifying')[0])
txt = pretty_event_results(driverstandings(2023))
l_txt = txt.split('\n')
print(l_txt)
im = Image.new('RGB', (100, 100), color=0)
fnt = ImageFont.truetype("Courier", size=20)
draw = ImageDraw.Draw(im)
textlen = draw.textbbox((0, 0), txt, font=fnt)
# textlen = draw.multiline_textbbox((0, 0), txt, font=fnt, spacing=5)
print(textlen)
im = Image.new('RGB', (textlen[2]+textlen[1], textlen[3]+textlen[1]+2), color=(234, 234, 220, 1))


draw = ImageDraw.Draw(im)
im_height = im.height
im_width = im.width
w = 5
count = 0
for a in l_txt:
    if count % 2 == 0 and count != 0:
        draw.rectangle(xy=((0, w), (im_width, w+20)), fill=(255, 255, 255))
    draw.text((10, w), a, font=fnt, fill=(0, 0, 0))
    w += 20
    count += 1

# draw.multiline_text((0, 0), txt, font=fnt, fill=(0, 0, 0), spacing=5)





im.show()
