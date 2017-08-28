from PIL import Image, ImageFont, ImageDraw

from io import BytesIO


def create_share_me_image(student):

    path_prefix = 'black_market/service/image/'

    background = Image.open(path_prefix + 'template/share_me.jpg')

    avatar_image = student.avatar

    avatar = Image.open(BytesIO(avatar_image))

    back_img = draw_circle_avatar(avatar, background)

    font = ImageFont.truetype(path_prefix + 'font/HelveticaNeue.dfont', 30)

    drawImage = ImageDraw.Draw(back_img)
    textSize = drawImage.textsize(student.username, font=font)
    x = (background.size[0] - textSize[0]) / 2
    drawImage.text((x, 550), student.username, font=font, fill='grey')

    student_id = student.id
    if len(str(student_id)) == 1:
        student_id = '00%s' % student_id

    if len(str(student_id)) == 2:
        student_id = '0%s' % student_id

    sentence = 'I am the No.%s Black Market user' % student_id

    font = ImageFont.truetype(path_prefix + 'font/Palatino.ttc', 34)

    drawImage.text((220, 650), sentence, font=font, fill='grey')

    img_io = BytesIO()
    back_img.save(img_io, 'JPEG', quality=50)

    return img_io


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
    background.paste(im, (400, 350), im)
    return background
