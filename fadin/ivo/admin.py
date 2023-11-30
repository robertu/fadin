from django.contrib import admin

from .models import Company, Customer, Invoice, InvoiceItem, Item


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1
    readonly_fields = ("amount", "item_price")

    def item_price(self, obj):
        return obj.item.price


class InvoiceAdmin(admin.ModelAdmin):
    fields = (
        "number",
        "due_date",
        "seller",
        "buyer",
        "amount",
        "created_at",
        "created_by",
    )
    readonly_fields = (
        "amount",
        "created_at",
        "created_by",
    )
    list_display = (
        "number",
        "due_date",
        "seller",
        "buyer",
        "amount",
        "created_at",
        "created_by",
    )
    list_filter = (
        "seller",
        "buyer",
        "created_at",
        "created_by",
    )
    search_fields = (
        "number",
        "seller__name",
        "buyer__name",
        "created_by__username",
        "invoiceitem__item__name",
    )

    inlines = (InvoiceItemInline,)

    def get_form(self, request, obj=None, **kwargs):
        form = super(InvoiceAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["number"].initial = Invoice.generate_number()
        form.base_fields["due_date"].initial = Invoice.generate_due_date()
        return form

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Company)
admin.site.register(Customer)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Item)
