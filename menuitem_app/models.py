from django.db import models
from django.contrib.postgres.fields import ArrayField



def menuitem_image_path(instance, filename):
    # This function will be used to generate the upload path
    return f'menuitems/{instance.name}/{filename}'


class MenuItemExtra(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id}-{self.title}"

class MenuItemExtraItem(models.Model):
    extra = models.ForeignKey(MenuItemExtra, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.id} - {self.name}"
    

class MenuItemType(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id}-{self.title}"

class MenuItemTypeItem(models.Model):
    type = models.ForeignKey(MenuItemType, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name}"


class MenuItem(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=250)
    image = models.ImageField(upload_to=menuitem_image_path, null=True)
    ingredients = ArrayField(models.CharField(max_length=100, null=True, blank=True), default=list, null = True)
    extras = models.ManyToManyField(MenuItemExtra, blank=True)
    types = models.ManyToManyField(MenuItemType, blank=True)
    sizes_and_prices = models.JSONField(default=list)

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"
    
    def get_default_sizes_and_prices(self):
        return [{"size": "Small", "price": 0.0}]

    def save(self, *args, **kwargs):
        if not self.sizes_and_prices:
            self.sizes_and_prices = self.get_default_sizes_and_prices()
        super().save(*args, **kwargs)

