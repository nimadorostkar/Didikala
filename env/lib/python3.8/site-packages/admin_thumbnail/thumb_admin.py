#coding: utf-8

__author__ = 'flaviocaetano'

from django.contrib.admin import ModelAdmin
from django.db import models

from django.shortcuts import render

class ThumbAdmin(ModelAdmin):

    def __init__(self, model, admin_site):
        self.model = model

        super(ThumbAdmin, self).__init__(model, admin_site)


    def get_attr(self, f, request):
        def callable(obj):
            field = getattr(obj, f.attname)
            test = render(request, 'thumb.html', {'image': field, 'obj': obj})
            return test.content

        return callable


    def changelist_view(self, request, extra_context=None):
        result = list(self.list_display)

        for field_name in result:
            try:
                field = self.model._meta.get_field_by_name(field_name)[0]
            except models.FieldDoesNotExist, e:
                continue

            if isinstance(field, models.ImageField):
                attr = self.get_attr(field, request)
                attr.__name__ = '%s%s' % (attr.__name__, field_name)
                attr.short_description = field.verbose_name
                attr.allow_tags = True

                result[result.index(field_name)] = attr

        self.list_display = tuple(result)

        return super(ThumbAdmin, self).changelist_view(request, extra_context)