from io import BytesIO

from PIL import Image, ImageFont, ImageDraw

from .common import add_student_name_and_avatar, get_app_qrcode_by_path, path_prefix


def create_share_me_image(student, path):

    template_file = path_prefix + 'template/BlackMarketShareMe.jpg'

    background = Image.open(template_file)

    back_img = add_student_name_and_avatar(student, background, name_y_axis=550, avatar_y_axis=350)
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
