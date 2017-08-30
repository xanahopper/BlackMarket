from io import BytesIO

from PIL import Image, ImageFont, ImageDraw
from .common import add_student_name_and_avatar, get_app_qrcode_by_path, path_prefix


def create_share_post_image(student, path, supply, demand):

    template_file = path_prefix + 'template/BlackMarketSharePost.jpg'

    background = Image.open(template_file)

    back_img = add_student_name_and_avatar(student, background, name_y_axis=530, avatar_y_axis=320)
    drawImage = ImageDraw.Draw(back_img)

    if supply and demand:
        sentence_supply = '供给: %s' % supply
        sentence_demand = '需求: %s' % demand
        font = ImageFont.truetype(path_prefix + 'font/Hiragino-Sans-GB-W6.ttc', 34)
        textSize = drawImage.textsize(sentence_supply, font=font)
        x = round((back_img.size[0] - textSize[0]) / 2)
        drawImage.text((x, 175), sentence_supply, font=font, fill='grey')

        textSize = drawImage.textsize(sentence_demand, font=font)
        x = round((back_img.size[0] - textSize[0]) / 2)
        drawImage.text((x, 240), sentence_demand, font=font, fill='grey')

    elif supply and not demand:
        sentence_supply = '供给: %s' % supply
        font = ImageFont.truetype(path_prefix + 'font/Hiragino-Sans-GB-W6.ttc', 34)
        textSize = drawImage.textsize(sentence_supply, font=font)
        x = round((back_img.size[0] - textSize[0]) / 2)
        drawImage.text((x, 200), sentence_supply, font=font, fill='grey')

    elif demand and not supply:
        sentence_demand = '需求: %s' % demand
        font = ImageFont.truetype(path_prefix + 'font/Hiragino-Sans-GB-W6.ttc', 34)
        textSize = drawImage.textsize(sentence_demand, font=font)
        x = round((back_img.size[0] - textSize[0]) / 2)
        drawImage.text((x, 200), sentence_demand, font=font, fill='grey')

    app_qrcode_image = get_app_qrcode_by_path(path)
    qrcode_img = Image.open(BytesIO(app_qrcode_image.data))

    x = round((back_img.size[0] - qrcode_img.size[0]) / 2)
    background.paste(qrcode_img, (x, 590))

    img_io = BytesIO()
    back_img.save(img_io, 'JPEG', quality=80)

    return img_io
