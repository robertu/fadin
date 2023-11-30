from datetime import date, timedelta

from django.contrib.auth.models import User
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    taxid = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} ({self.taxid})"


class Customer(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    taxid = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} ({self.taxid})"


class Invoice(models.Model):
    DUE_DAYS = 14

    number = models.CharField(max_length=100, unique=True)
    due_date = models.DateField(
        default=None, null=True, blank=True, help_text=f"default is {DUE_DAYS} days"
    )
    seller = models.ForeignKey(Company, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, editable=False
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, editable=False
    )

    def __str__(self):
        return self.number

    @classmethod
    def generate_number(cls):
        today = date.today()
        year = today.year
        month = today.month
        last_invoice = (
            cls.objects.filter(created_at__year=year, created_at__month=month)
            .order_by("number")
            .last()
        )
        if last_invoice:
            last_number = int(last_invoice.number.split("/")[-1])
        else:
            last_number = 0
        new_number = last_number + 1
        return f"{year}/{month:02d}/{new_number:04d}"

    @classmethod
    def generate_due_date(cls):
        return date.today() + timedelta(days=cls.DUE_DAYS)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.number = self.generate_number()
        super().save(*args, **kwargs)

    @classmethod
    def new(cls, buyer_id, seller_id, items=[]):
        inv = cls()
        if not inv.pk:
            inv.number = cls.generate_number()
            inv.due_date = cls.generate_due_date()
        inv.buyer_id = buyer_id
        inv.seller_id = seller_id
        inv.save()
        for item in items:
            inv.invoiceitem_set.create(**item)
        return inv

    # @property
    # def items(self):
    #     return self.invoiceitem_set.all()
class Item(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, editable=False
    )

    def __str__(self):
        return f"{self.item} | {self.quantity} x {self.price} = {self.amount}"

    @staticmethod
    def pre_save_update_signal(sender, instance, **kwargs):
        if instance.price is None:
            instance.price = instance.item.price
        instance.amount = instance.price * instance.quantity

    @staticmethod
    def post_save_update_signal(sender, instance, **kwargs):
        instance.invoice.amount = instance.invoice.invoiceitem_set.all().aggregate(
            models.Sum("amount")
        )["amount__sum"]
        instance.invoice.save()
