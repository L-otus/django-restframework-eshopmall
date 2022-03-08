from app.qr_gen.models import order_qr
from datetime import datetime
import qrcode
import uuid
import json

def order_generate():
    order_list = uuid.uuid1()
    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(order_list)
    qr.make(fit=True)
    order_add=order_qr.objects.create(order_id=order_list,validity=True,qr_img=qr.make_image())
    return order_add.order_id