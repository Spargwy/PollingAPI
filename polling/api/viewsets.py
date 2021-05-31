from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from .serializers import PollSerializer, UserAnswerSerializer
from ..models import Poll
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class PollViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = PollSerializer
    queryset = Poll.objects.all()

    @action(detail=True, methods=['post'])  # /api/polls/<pk>/answer/
    def answer(self, request):
        poll = self.get_object()
        serializer = UserAnswerSerializer(data=request.data, context={'poll': poll})
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user if request.user.is_authenticated else None, poll=poll)
            return Response({'Status': 'Your answer received'})
