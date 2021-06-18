from django.contrib import admin

# Register your models here.
from eshop_comment.models import Comment, RateComment


class CommentAdmin(admin.ModelAdmin):
    list_display = ['product', 'subject', 'j_create_at','j_update_at', 'status']
    readonly_fields = ('product', 'subject', 'advantage', 'disadvantage', 'advice', 'user_id', 'ip', 'update_at')
    list_filter = ['status']
    list_editable = ['status']


class RateCommentAdmin(admin.ModelAdmin):
    list_display = ['product', 'attribute', 'rate']
    readonly_fields = ('product', 'attribute', 'rate')


admin.site.register(Comment, CommentAdmin)
admin.site.register(RateComment, RateCommentAdmin)
