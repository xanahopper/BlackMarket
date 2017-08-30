from io import BytesIO

from PIL import Image, ImageFont, ImageDraw

path_prefix = 'black_market/service/image/'


def create_share_me_image(student, path):

    template_file = path_prefix + 'template/BlackMarketShare.jpg'

    background = Image.open(template_file)

    back_img = add_student_name_and_avatar(student, background)
    drawImage = ImageDraw.Draw(back_img)

    student_id = student.id
    if len(str(student_id)) == 1:
        student_id = '00%s' % student_id

    if len(str(student_id)) == 2:
        student_id = '0%s' % student_id

    sentence = 'I am the No.%s Black Market user' % student_id

    font = ImageFont.truetype(path_prefix + 'font/Palatino.ttc', 34)
    textSize = drawImage.textsize(sentence, font=font)
    x = round((back_img.size[0] - textSize[0]) / 2)
    drawImage.text((x, 650), sentence, font=font, fill='grey')

    # TODO add app_qrcode_image to the back_img
    app_qrcode_image = get_app_qrcode_by_path(path)

    qrcode_img = Image.open(BytesIO(app_qrcode_image.data))

    x = round((back_img.size[0] - qrcode_img.size[0]) / 2)
    background.paste(qrcode_img, (x, 745))

    img_io = BytesIO()
    back_img.save(img_io, 'JPEG', quality=80)

    return img_io


def create_share_post_image(student, path, supply, demand):

    template_file = path_prefix + 'template/BlackMarketShare.jpg'

    background = Image.open(template_file)

    back_img = add_student_name_and_avatar(student, background)
    drawImage = ImageDraw.Draw(back_img)

    if supply and demand:
        sentence_supply = '供给: %s' % supply
        sentence_demand = '需求: %s' % demand
        font = ImageFont.truetype(path_prefix + 'font/AdobeSongStd-Light.otf', 34)
        textSize = drawImage.textsize(sentence_supply, font=font)
        x = round((back_img.size[0] - textSize[0]) / 2)
        drawImage.text((x, 625), sentence_supply, font=font, fill='grey')

        textSize = drawImage.textsize(sentence_demand, font=font)
        x = round((back_img.size[0] - textSize[0]) / 2)
        drawImage.text((x, 690), sentence_demand, font=font, fill='grey')

    elif supply and not demand:
        sentence_supply = '供给: %s' % supply
        font = ImageFont.truetype(path_prefix + 'font/AdobeSongStd-Light.otf', 34)
        textSize = drawImage.textsize(sentence_supply, font=font)
        x = round((back_img.size[0] - textSize[0]) / 2)
        drawImage.text((x, 650), sentence_supply, font=font, fill='grey')

    elif demand and not supply:
        sentence_demand = '需求: %s' % demand
        font = ImageFont.truetype(path_prefix + 'font/AdobeSongStd-Light.otf', 34)
        textSize = drawImage.textsize(sentence_demand, font=font)
        x = round((back_img.size[0] - textSize[0]) / 2)
        drawImage.text((x, 650), sentence_demand, font=font, fill='grey')

    app_qrcode_image = get_app_qrcode_by_path(path)
    qrcode_img = Image.open(BytesIO(app_qrcode_image.data))

    x = round((back_img.size[0] - qrcode_img.size[0]) / 2)
    background.paste(qrcode_img, (x, 745))

    img_io = BytesIO()
    back_img.save(img_io, 'JPEG', quality=80)

    return img_io


def add_student_name_and_avatar(student, background):
    avatar_image = student.avatar
    avatar = Image.open(BytesIO(avatar_image))
    back_img = draw_circle_avatar(avatar, background)
    font = ImageFont.truetype(path_prefix + 'font/AdobeSongStd-Light.otf', 30)
    drawImage = ImageDraw.Draw(back_img)
    textSize = drawImage.textsize(student.username, font=font)
    x = round((back_img.size[0] - textSize[0]) / 2)
    drawImage.text((x, 550), student.username, font=font, fill='grey')
    return back_img


def draw_circle_avatar(im, background):
    im = im.resize((180, 180))
    bigsize = (im.size[0] * 3, im.size[1] * 3)
    # 遮罩对象
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    # 画椭圆的方法
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(im.size, Image.ANTIALIAS)
    im.putalpha(mask)
    x = round((background.size[0] - im.size[0]) / 2)
    background.paste(im, (x, 350), im)
    return background


def get_app_qrcode_by_path(path):
    from black_market.intergration.wechat import wechat
    return wechat.get_app_qrcode_by_path(path)
