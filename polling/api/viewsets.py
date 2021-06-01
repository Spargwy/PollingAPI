from django.contrib.auth import authenticate, login

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, SAFE_METHODS
from rest_framework import views
from rest_framework import status

from .permissions import AnonymousOnly
from .serializers import PollSerializer, UserAnswerSerializer, UserAnswerListSerializer
from ..models import Poll


class PollViewSet(ModelViewSet):
    serializer_class = PollSerializer
    queryset = Poll.objects.all()
    permission_classes = (AllowAny,)

    def get_permissions(self):
        permissions = super().get_permissions()
        if self.request.method not in SAFE_METHODS:
            permissions.append(IsAdminUser())
        return permissions

    @action(detail=True, methods=['post'])  # /api/polls/<pk>/answer/
    def answer(self, request, *args, **kwargs):
        poll = self.get_object()
        serializer = UserAnswerSerializer(data=request.data, context={'poll': poll})
        if serializer.is_valid(raise_exception=True):
            serializer.save(
                user=request.user if request.user.is_authenticated else None,
                poll=poll,
            )
            return Response({'Status': 'Your answer received'})

    @action(detail=False, methods=['get'], url_path=r'user-answers/(?P<user_id>\d+)')
    def get_user_answers(self, request, user_id):
        answers = request.user.answers.all()
        return Response(UserAnswerListSerializer(answers, many=True).data)


class LoginView(views.APIView):
    permission_classes = (AnonymousOnly,)

    def post(self, request, format=None):  # noqa
        data = request.data

        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
