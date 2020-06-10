from rest_framework import routers
from polls_api import views as api_views


router = routers.DefaultRouter()
router.register(r'polls', api_views.PollViewset)
router.register(r'questions', api_views.QuestionViewset)
router.register(r'choices', api_views.ChoiceViewset)
router.register(r'answers', api_views.AnswerViewset)
