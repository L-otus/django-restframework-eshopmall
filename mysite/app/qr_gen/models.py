from django.db import models
from app.users.models import login_user
# Create your models here.
class order_qr(models.Model):
    order_id=models.CharField(max_length=256,unique=True)
    order_user=models.ForeignKey(login_user,on_delete=models.CASCADE())
    qr_img=models.ImageField(upload_to='qr/%Y/%m/%d')
    def img_directory(self):
        return self.qr_img.name
