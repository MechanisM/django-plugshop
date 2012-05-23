#encoding: utf-8
import plugshop.utils as utils

from django.contrib import admin
from django.utils.translation import ugettext as _

from mptt.admin import MPTTModelAdmin

from plugshop import settings
from plugshop.utils import load_class
from plugshop.models import *
from plugshop.utils import is_default_model

class BaseProductAdmin(admin.ModelAdmin):
    #change_list_template = 'admin/product/change_list.html'
    inlines = ()
    search_fields = ('name',)
    prepopulated_fields = {
        'slug': ('name',) 
    }
    list_display = (
        'name',
        'slug',
        #'category',
    )
    list_filter = (
        'category',
    )
    def changelist_view(self, request, extra_context=None):
        context = {}
        return super(BaseProductAdmin, self).changelist_view(request, 
                                                        extra_context=context)

if is_default_model('PRODUCT'):
    admin.site.register(load_class(settings.PRODUCT_MODEL), BaseProductAdmin)

class BaseCategoryAdmin(MPTTModelAdmin):
    change_list_template = 'admin/category/change_list.html'
    mptt_level_indent = 20
    prepopulated_fields = {
        'slug': ('name', )
    }
    list_display = (
        'name',
        'get_products',
        'slug',
    )

    def get_products(self, instance):
        return "<br/>".join(p.name for p in instance.products.all())
    get_products.allow_tags = True
    get_products.short_description = _('products')
    
if is_default_model('CATEGORY'):
    admin.site.register(load_class(settings.CATEGORY_MODEL), BaseCategoryAdmin)



class BaseOrderProductsInline(admin.TabularInline):
    model = load_class(settings.ORDER_PRODUCTS_MODEL)
    extra = 0

class BaseOrderAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    inlines = (
        BaseOrderProductsInline,
    )
    search_fields = ('number', 'user',)
    list_display = (
        'number',
        'user',
        'status',
        'created_at',
        'updated_at',
        'delivered_at',
    )
    list_editable = (
        'status',
    )
    list_filter = (
        'status', 
        'created_at',
    )
if is_default_model('ORDER'):
    admin.site.register(load_class(settings.ORDER_MODEL), BaseOrderAdmin)
