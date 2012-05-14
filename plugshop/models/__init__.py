from django.utils.translation import ugettext as _
from django.db import models

from plugshop import settings
from plugshop.utils import load_class

from plugshop.models.product import *
from plugshop.models.category import *
from plugshop.models.option import *
from plugshop.models.product_options import *
from plugshop.models.shipping import *
from plugshop.models.order import *
from plugshop.models.order_products import *

__all__ = [
    'ProductAbstract',
    'CategoryAbstract',
    'ProductOptionsAbstract', 
    'OptionAbstract',
    'ShippingTypeAbstract',
    'ShippingAbstract',
    'OrderAbstract',
    'OrderProductsAbstract',
]

def import_default(name, settings, where=[]):
    default_name = "%s_DEFAULT" % name
    model = getattr(settings, name)
    default_model = getattr(settings, default_name)

    cls = load_class(model)

    if model == default_model:
        #setattr(cls._meta, 'app_label', 'plugshop')
        where.append(default_model.split('.')[-1])

for m in ['PRODUCT_MODEL', 
            'CATEGORY_MODEL',
            'OPTION_MODEL',
            'PRODUCT_OPTIONS_MODEL',
            'SHIPPING_TYPE_MODEL',
            'SHIPPING_MODEL',
            'ORDER_MODEL',
            'ORDER_PRODUCTS_MODEL']:
    import_default(m, settings, __all__)

print __all__

models.ManyToManyField(load_class(settings.OPTION_MODEL),  
                        through=load_class(settings.PRODUCT_OPTIONS_MODEL),
                        related_name="products",
                        verbose_name=_('option list')
                    ).contribute_to_class(load_class(settings.PRODUCT_MODEL), 
                                                        'options')

models.ForeignKey(load_class(settings.CATEGORY_MODEL),
                        verbose_name=_('category'),
                        related_name='products',
                        blank=True,
                        null=True
                    ).contribute_to_class(load_class(settings.PRODUCT_MODEL), 
                                                        'category')

models.ManyToManyField(load_class(settings.PRODUCT_MODEL),
                        through=load_class(settings.ORDER_PRODUCTS_MODEL),
                        related_name="products",
                        verbose_name=_('products')
                    ).contribute_to_class(load_class(settings.ORDER_MODEL), 
                                                        'products')