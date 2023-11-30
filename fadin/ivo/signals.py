from django.db.models.signals import post_save, pre_save

from .models import InvoiceItem

pre_save.connect(InvoiceItem.pre_save_update_signal, sender=InvoiceItem)
post_save.connect(InvoiceItem.post_save_update_signal, sender=InvoiceItem)
