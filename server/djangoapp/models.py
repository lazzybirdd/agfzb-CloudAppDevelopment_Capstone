from django.db import models
from django.utils.timezone import now

try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=32)

    def __str__(self):
        return str(self.id) \
            + " " + self.name \
            + " " + self.description

class CarDealer(models.Model):
    id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=32)

    STATE = [
        ('CA', 'California'),
        ('AZ', 'Arizona'),
        ('TX', 'Texas'),
        ('OR', 'Oregon')
    ]
    st = models.CharField(
        max_length=2,
        choices=STATE
    )

    address = models.CharField(max_length=100)
    zip = models.CharField(max_length=5)
    lat = models.FloatField()
    long = models.FloatField()

    full_name = models.CharField(max_length=100, default="", null=True)
    #long_name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=32)

    def __str__(self):
        return str(self.id) \
            + " " + self.short_name

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    id = models.AutoField(primary_key=True)
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)

    SEDAN = 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    TRUCK = 'truck'
    TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
        (TRUCK, 'Truck')
    ]
    type = models.CharField(
        null=False,
        max_length=16,
        choices=TYPE_CHOICES,
        default=SEDAN
    )

    dealership = models.ForeignKey(CarDealer, on_delete=models.CASCADE)
    year = models.IntegerField()

    def __str__(self):
        return str(self.id) \
            + " " + self.name \


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    dealership = models.ForeignKey(CarDealer, on_delete=models.CASCADE)
    review = models.CharField(max_length=200)
    purchase = models.BooleanField(default=True)
    purchase_date = models.DateField(auto_now_add=True)
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) \
            + " " + self.name
