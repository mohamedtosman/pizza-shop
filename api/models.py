"""
Models
"""

import uuid
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    """
    Base Model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Customer(BaseModel):
    """
    Customer Model
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class CustomerInfo(BaseModel):
    """
    Customer Info Model
    """
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=50, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.customer)


class Order(BaseModel):
    """
    Order Model
    """
    PROCESSING_STATUS = 'Processing'
    DELIVERING_STATUS = 'Delivering'
    DELIVERED_STATUS = 'Delivered'
    STATUS_CHOICES = (
        (PROCESSING_STATUS, PROCESSING_STATUS),
        (DELIVERING_STATUS, DELIVERING_STATUS),
        (DELIVERED_STATUS, DELIVERED_STATUS),
    )
    customer_info = models.ForeignKey(CustomerInfo, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PROCESSING_STATUS)
    delivered_at = models.DateTimeField(null=True)

    class Meta:
        ordering = ('-created_at',)

    @property
    def delivered(self):
        """
        Check if pizza is delivered
        :return: boolean
        """
        return self.status == self.DELIVERED_STATUS

    def can_update(self):
        """
        Check if you can update pizza
        :return: boolean
        """
        if self.status in [self.DELIVERING_STATUS, self.DELIVERED_STATUS]:
            return False
        return True

    def can_update_status(self, status):
        """
        Check if you can update pizza
        :return: boolean
        """
        weighted_status = {self.PROCESSING_STATUS: 1,
                           self.DELIVERING_STATUS: 2,
                           self.DELIVERED_STATUS: 3}
        if status in weighted_status and weighted_status[status] > weighted_status[self.status]:
            return True
        return False

    def update_status(self, status, commit=True):
        """
        Update status
        :param status: boolean
        :param commit: boolean
        :return: boolean
        """
        if self.can_update_status(status):
            self.status = status
            if commit:
                self.save()

    def save(self, *args, **kwargs):
        """
        Save new order
        :param args:
        :param kwargs:
        :return:
        """
        if self.status == self.DELIVERED_STATUS and not self.delivered_at:
            self.delivered_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Order({0}) {1}'.format(self.id, str(self.customer_info))


class Pizza(BaseModel):
    """
    Pizza Model
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class PizzaOrder(BaseModel):
    """
    Pizza Order Model
    """
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name='pizzas', on_delete=models.CASCADE)

    def __str__(self):
        return '{0} {1}'.format(str(self.order), str(self.pizza))


class PizzaDetail(BaseModel):
    """
    Pizza Detail Model
    """
    SMALL_SIZE = 'Small'
    MEDIUM_SIZE = 'Medium'
    LARGE_SIZE = 'Large'
    SIZE_CHOICES = (
        (SMALL_SIZE, SMALL_SIZE),
        (MEDIUM_SIZE, MEDIUM_SIZE),
        (LARGE_SIZE, LARGE_SIZE),
    )
    size = models.CharField(max_length=20, choices=SIZE_CHOICES)
    count = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    pizza_order = models.ForeignKey(PizzaOrder, related_name='details', on_delete=models.CASCADE)

    def __str__(self):
        return 'Pizza({0} - {1})'.format(self.size, self.count)
