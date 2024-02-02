import os
import secrets
from PIL import Image
from flask_webapp import mail
from flask import url_for, current_app
from flask_mail import Message


def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	f_name, f_extension = os.path.splitext(form_picture.filename)
	picture_filename = random_hex + f_extension
	picture_path = os.path.join(current_app.root_path, 'static/profiles', picture_filename)

	"""resize the picture before saving it to file"""

	output_size = (125, 125)
	new_image = Image.open(form_picture)
	new_image.thumbnail(output_size)

	new_image.save(picture_path)
	return picture_filename


def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password Reset Request',
					sender = os.environ.get('ACCOUNT_EMAIL'),
					recipients=[user.email])
	msg.body = f'''Follow this link to reset your password:
{url_for('reset_token', token=token, _external=True)} '''

	mail.send(msg)

