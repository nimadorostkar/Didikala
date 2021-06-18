from .signals import object_viewed_signal
from functools import wraps


# we should use this with CBV
class ObjectViewMixin:
    def dispatch(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except self.model.DoesNotExist:
            instance = None

        if request.user.is_authenticated and instance is not None:
            object_viewed_signal.send(instance.__class__, instance=instance, request=request)

        return super(ObjectViewMixin, self).dispatch(request, *args, **kwargs)

# for FBV i use this code on the function view directly
#  add this code where you want to record it in history
#  object_viewed_signal.send(product.__class__, instance=product, request=request)
