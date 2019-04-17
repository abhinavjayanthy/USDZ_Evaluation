from PIL import Image, ImageDraw, ImageFont

W, H = 100, 100


def create_image(price, stock_name,position):
    img = Image.new('RGBA', (W, H), (255, 0, 0, 0))
    fnt = ImageFont.truetype('/Library/Fonts/Arial.ttf', 15)
    draw = ImageDraw.Draw(img)
    text = '$' + str(price * 5)
    w, h = draw.textsize(text)
    draw.text(((W - w) / 2, (H - h) / 2), text, font=fnt, fill=(0, 0, 0))
    img.save('/Users/Abhinav/Documents/USDZ/CNBC/PriceImages/' + stock_name + str(position) + '.png')
    return '/Users/Abhinav/Documents/USDZ/CNBC/PriceImages/' + stock_name + str(position) +'.png'
