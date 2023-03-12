from http import HTTPStatus

from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.response import Response


class AddDelViewMixin:
    add_serializer = None

    def _add_del_obj(self, obj_id, model, query):
        obj = get_object_or_404(self.queryset, id=obj_id)
        serializer = self.add_serializer(obj)
        model_obj = model.objects.filter(query & Q(user=self.request.user))
        if (self.request.method in ('GET', 'POST')) and not model_obj:
            model(None, self.request.user.id, obj.id).save()
            return Response(serializer.data, status=HTTPStatus.CREATED)
        if (self.request.method in ('DELETE',)) and model_obj:
            model_obj[0].delete()
            return Response(status=HTTPStatus.NO_CONTENT)
        return Response(status=HTTPStatus.BAD_REQUEST)
