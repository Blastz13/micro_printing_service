import os
import zipfile

from django.contrib import admin
from django.http import FileResponse

from .models import Order, Photo


class OrderPhotoInline(admin.StackedInline):
    model = Photo
    extra = 1


@admin.register(Order)
class AdminProduct(admin.ModelAdmin):
    list_display = ["last_name", "tel", "size", "quantity", "quantity_upload_photos", "date_order", "total_price"]
    list_display_links = ["last_name", "tel", "size", "quantity", "date_order", "total_price"]
    search_fields = ["last_name", "tel", "size", "quantity", "date_order", "total_price"]
    readonly_fields = ["date_order"]
    inlines = [OrderPhotoInline]
    actions = ['export_image']

    # i am idiot:)
    def export_image(self, request, queryset):
        for model in queryset:
            path = f'D:\\micro_printing_service\\zip\\{model.last_name}  {model.tel}  {model.size} x{model.quantity}={model.total_price}.zip'
            newzip = zipfile.ZipFile(f'{path}', 'w')
            for photo in Photo.objects.filter(order_id=model.pk):
                url = os.path.join('D:/micro_printing_service' + photo.photos.url)
                newzip.write(url)
        newzip.close()
        img = open(f'{path}', 'rb')
        response = FileResponse(img)
        return response

    export_image.short_description = "Экспорт фото"
