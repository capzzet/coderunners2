from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'



class Tender(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    purchase_name = models.CharField(max_length=100, verbose_name='Наименование закупки')
    purchase_method = models.CharField(max_length=100, verbose_name='Метод закупки')
    purchase_number = models.CharField(max_length=100, verbose_name='Номер закупки')
    purchase_type = models.CharField(max_length=100, verbose_name='Вид закупок')
    organization_name = models.CharField(max_length=100, verbose_name='Наименование организации')
    planned_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Планируемая сумма')
    publication_date = models.DateTimeField(verbose_name='Дата опубликования')
    proposal_deadline = models.DateTimeField(verbose_name='Срок подачи предложений поставщиков')

    def __str__(self):
        return self.purchase_name

@receiver(pre_save, sender=Tender)
def assign_user(sender, instance, **kwargs):
    if not instance.user:
        instance.user = User.objects.get(username='root')