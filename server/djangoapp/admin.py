from django.contrib import admin
from .models import CarMake, CarModel, CarDealer, DealerReview


# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 3

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    #fields = ["name", "type", "year"]
    list_display = ["name", "type", "year"]

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    #fieldsets = [
    #    ("Make", {"fields": ["name", "description"]}),
    #    ("Model", {"fields": ["name", "type", "year"]}),
    #
    inlines = [CarModelInline]

class CarDealerAdmin(admin.ModelAdmin):

    list_display = ["short_name", "full_name", "city", "st", "address", "zip"]
    #list_display = ["short_name", "city", "st", "address", "zip"]

class DealerReviewAdmin(admin.ModelAdmin):

    #def is_purchased(self):
    #    if self.puchase == True:
    #        return True
    #    return False

    #list_display = ["name", "review", "purchase_date", "is_purchased"]
    list_display = ["name", "review", "purchase_date", "purchase"]


# Register models here
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarDealer, CarDealerAdmin)
admin.site.register(DealerReview, DealerReviewAdmin)
