from io import BytesIO

from PIL import Image, ImageFont, ImageDraw

path_prefix = 'black_market/service/image/'


def add_student_name_and_avatar(student, background, name_y_axis, avatar_y_axis):
    avatar_image = student.avatar
    avatar = Image.open(BytesIO(avatar_image))
    back_img = draw_circle_avatar(avatar, background, avatar_y_axis)
    font = ImageFont.truetype(path_prefix + 'font/AdobeHeitiStd-Regular.otf', 30)
    drawImage = ImageDraw.Draw(back_img)
    textSize = drawImage.textsize(student.username, font=font)
    x = round((back_img.size[0] - textSize[0]) / 2)
    y = name_y_axis
    drawImage.text((x, y), student.username, font=font, fill='grey')
    return back_img


def draw_circle_avatar(im, background, y_axis):
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
    background.paste(im, (x, y_axis), im)
    return background


def get_app_qrcode_by_path(path):
    from black_market.intergration.wechat import wechat
    return wechat.get_app_qrcode_by_path(path)
