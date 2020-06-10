from datetime import datetime
from django.db.models import Q
from django.shortcuts import get_list_or_404
from rest_flex_fields import FlexFieldsModelViewSet
from rest_framework.permissions import AllowAny, IsAdminUser, DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response
from . import models
from . import serializers


class PollViewset(FlexFieldsModelViewSet):
    queryset = models.Poll.objects.all()
    serializer_class = serializers.PollsSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly | IsAdminUser]

    def get_queryset(self):
        qs = super().get_queryset()
        only_active = str(self.request.query_params.get('active')).lower()
        if only_active in ['true', '1']:
            now = datetime.now().date()
            qs = qs.filter(Q(date_finish__gt=now) | Q(date_finish=None) & Q(date_start__lte=now))
        return qs


class QuestionViewset(FlexFieldsModelViewSet):
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly | IsAdminUser]


class ChoiceViewset(FlexFieldsModelViewSet):
    queryset = models.Choice.objects.all()
    serializer_class = serializers.ChoiceSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly | IsAdminUser]


class AnswerViewset(FlexFieldsModelViewSet):
    """
    GET root request (api/v1/answers):

    * Will return an unsorted list of users' answers.

    GET user's answer request (api/v1/answers/{uid}):

    * Will return expanded list of answers this particular user provides.
    """
    queryset = models.Answer.objects.all().select_related('question', 'choice')
    serializer_class = serializers.AnswerSerializer
    permit_list_expands = ['question', 'choice']
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        user_id = int(kwargs['pk'])
        queryset = models.Answer.objects.all()
        user = get_list_or_404(queryset, user_id=user_id)
        serializer = serializers.AnswerSerializer(user, many=True, expand=['question', 'choice'])
        return Response(serializer.data)
