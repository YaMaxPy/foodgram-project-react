from http import HTTPStatus

from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.response import Response


class AddDelViewMixin:
    add_serializer = None

    def _add_del_obj(self, obj_id, m2m_model, q):
        obj = get_object_or_404(self.queryset, id=obj_id)
        serializer = self.add_serializer(obj)
        m2m_obj = m2m_model.objects.filter(q & Q(user=self.request.user))
        if (self.request.method in ('GET', 'POST')) and not m2m_obj:
            m2m_model(None, self.request.user.id, obj.id).save()
            return Response(serializer.data, status=HTTPStatus.CREATED)
        if (self.request.method in ('DELETE',)) and m2m_obj:
            m2m_obj[0].delete()
            return Response(status=HTTPStatus.NO_CONTENT)
        return Response(status=HTTPStatus.BAD_REQUEST)
