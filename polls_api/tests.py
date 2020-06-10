from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from .models import AnswerType


class PollsTestCase(APITestCase):
    url_polls = reverse('poll-list')
    url_polls_modify = lambda _, arg: reverse('poll-detail', args=[arg])
    url_questions = reverse('question-list')
    url_questions_modify = lambda _, arg: reverse('question-detail', args=[arg])
    url_choice = reverse('choice-list')
    url_choice_modify = lambda _, arg: reverse('choice-detail', args=[arg])
    url_answer = reverse('answer-list')
    url_answer_get_user = lambda _, arg: reverse('answer-detail', args=[arg])

    poll_color_models = {
        "id": 1,
        "name": "Color models",
        "description": "Poll about color models",
        "date_start": None,
        "date_finish": None
    }
    poll_drummer = {
        "id": 2,
        "name": "Drummer poll",
        "description": "Poll about drummers",
        "date_start": "2020-03-04",
        "date_finish": "2020-08-04"
    }
    poll_with_start_date = {
        "id": 1,
        "name": "Final poll",
        "description": "We cannot modify this one.",
        "date_start": "2021-06-04",
        "date_finish": None
    }
    question_color_models_1 = {
        'id': 1,
        'question': 'Select only color models.',
        'type': AnswerType.MULTIPLE,
        'poll': poll_color_models['id']
    }
    question_color_models_2 = {
        'id': 2,
        'question': 'Which color model is additive?',
        'type': AnswerType.SINGLE,
        'poll': poll_color_models['id']
    }
    question_drummer = {
        'id': 3,
        'question': 'Name your favourite drummer.',
        'type': AnswerType.TEXT,
        'poll': poll_drummer['id']
    }
    choice_color_models_1_1 = {
        'id': 1,
        'text': 'CIE',
        'question': 1
    }
    choice_color_models_1_2 = {
        'id': 2,
        'text': 'CIE LAB',
        'question': 1
    }
    choice_color_models_1_3 = {
        'id': 3,
        'text': 'RGB',
        'question': 1
    }
    choice_color_models_1_4 = {
        'id': 4,
        'text': 'YAML',
        'question': 1
    }
    choice_color_models_1_5 = {
        'id': 5,
        'text': 'JDF',
        'question': 1
    }
    choice_color_models_2_1 = {
        'id': 6,
        'text': 'CMYK',
        'question': 2
    }
    choice_color_models_2_2 = {
        'id': 7,
        'text': 'RGB',
        'question': 2
    }

    def _create_entity(self, url, data):
        user = User.objects.get_or_create(username='admin', is_superuser=True)
        self.client.force_authenticate(user=user[0])
        self.client.post(url, data)
        self.client.force_authenticate(user=None)

    def _modify_entity(self, url_modify, action: callable, data=None):
        user = User.objects.get_or_create(username='admin', is_superuser=True)
        self.client.force_authenticate(user=user[0])
        action(url_modify(1), data)
        self.client.force_authenticate(user=None)

    def _fixture_three_polls(self):
        self._create_entity(self.url_polls, self.poll_color_models)
        self._create_entity(self.url_questions, self.question_color_models_1)
        self._create_entity(self.url_questions, self.question_color_models_2)
        self._create_entity(self.url_choice, self.choice_color_models_1_1)
        self._create_entity(self.url_choice, self.choice_color_models_1_2)
        self._create_entity(self.url_choice, self.choice_color_models_1_3)
        self._create_entity(self.url_choice, self.choice_color_models_1_4)
        self._create_entity(self.url_choice, self.choice_color_models_1_5)
        self._create_entity(self.url_choice, self.choice_color_models_2_1)
        self._create_entity(self.url_choice, self.choice_color_models_2_2)
        self._create_entity(self.url_polls, self.poll_drummer)
        self._create_entity(self.url_questions, self.question_drummer)

    # readonly tests
    def test_polls_view_is_readonly(self):
        url = self.url_polls
        data = self.poll_color_models
        self.client.post(url, data)
        response = self.client.get(url)
        self.assertListEqual(response.data, [])

    def test_question_view_is_readonly(self):
        self._create_entity(self.url_polls, self.poll_color_models)
        url = self.url_questions
        self.client.post(url, self.question_color_models_2)
        response = self.client.get(url)
        self.assertListEqual(response.data, [])

    def test_choice_view_is_readonly(self):
        self._create_entity(self.url_polls, self.poll_color_models)
        self.client.post(self.url_questions, self.question_color_models_2)
        url = self.url_choice
        self.client.post(url, self.choice_color_models_2_1)
        response = self.client.get(url)
        self.assertListEqual(response.data, [])

    # authentication tests
    def test_authentication_allows_poll_creation(self):
        self._create_entity(self.url_polls, self.poll_color_models)
        result = self.client.get(self.url_polls)
        self.assertListEqual(result.data, [self.poll_color_models])

    def test_authentication_allows_question_creation(self):
        self._create_entity(self.url_polls, self.poll_color_models)
        self._create_entity(self.url_questions, self.question_color_models_1)
        result = self.client.get(self.url_questions)
        self.assertListEqual(result.data, [self.question_color_models_1])

    def test_authentication_allows_choice_creation(self):
        self._create_entity(self.url_polls, self.poll_color_models)
        self._create_entity(self.url_questions, self.question_color_models_1)
        self._create_entity(self.url_choice, self.choice_color_models_1_1)
        result = self.client.get(self.url_choice)
        self.assertListEqual(result.data, [self.choice_color_models_1_1])

    # entity modify tests
    def test_modify_poll(self):
        url = self.url_polls
        self._create_entity(url, self.poll_color_models)
        self._modify_entity(
            self.url_polls_modify,
            self.client.patch,
            data={"description": "Modified poll about color models"}
        )
        result = self.client.get(url)
        self.assertEqual(result.data[0].get('description'), 'Modified poll about color models')

    def test_modify_question(self):
        url = self.url_questions
        self._create_entity(self.url_polls, self.poll_color_models)
        self._create_entity(url, self.question_color_models_1)
        self._modify_entity(
            self.url_questions_modify,
            self.client.patch,
            data={"question": "Select only colour models."}
        )
        result = self.client.get(url)
        self.assertEqual(result.data[0].get('question'), 'Select only colour models.')

    def test_modify_choice(self):
        url = self.url_choice
        self._create_entity(self.url_polls, self.poll_color_models)
        self._create_entity(self.url_questions, self.question_color_models_1)
        self._create_entity(url, self.choice_color_models_1_1)
        self._modify_entity(
            self.url_choice_modify,
            self.client.patch,
            data={"text": "XYZ"}
        )
        result = self.client.get(url)
        self.assertEqual(result.data[0].get('text'), 'XYZ')

    # entity delete tests
    def test_delete_poll(self):
        url = self.url_polls
        self._create_entity(url, self.poll_color_models)
        self._modify_entity(self.url_polls_modify, self.client.delete)
        result = self.client.get(url)
        self.assertListEqual(result.data, [])

    def test_delete_question(self):
        url = self.url_questions
        self._create_entity(self.url_polls, self.poll_color_models)
        self._create_entity(url, self.question_color_models_1)
        self._modify_entity(self.url_questions_modify, self.client.delete)
        result = self.client.get(url)
        self.assertListEqual(result.data, [])

    def test_delete_choice(self):
        url = self.url_choice
        self._create_entity(self.url_polls, self.poll_color_models)
        self._create_entity(self.url_questions, self.question_color_models_1)
        self._create_entity(url, self.choice_color_models_1_1)
        self._modify_entity(self.url_choice_modify, self.client.delete)
        result = self.client.get(url)
        self.assertListEqual(result.data, [])

    # cannot modify poll' start date field
    def test_cannot_modify_poll_with_start_date(self):
        url = self.url_polls
        self._create_entity(url, self.poll_with_start_date)
        self._modify_entity(
            self.url_polls_modify,
            self.client.patch,
            data={"description": "Trying to modify"}
        )
        result = self.client.get(url)
        self.assertListEqual(result.data, [self.poll_with_start_date])

    # list of active polls
    def test_active_polls_list(self):
        url = self.url_polls
        self._create_entity(url, self.poll_color_models)
        self._create_entity(url, self.poll_drummer)
        self._create_entity(url, self.poll_with_start_date)
        result = self.client.get(f'{self.url_polls}?active=true')
        self.assertTrue(len(result.data) == 1)

    # answer types
    def test_answer_text(self):
        self._fixture_three_polls()
        result = self.client.post(self.url_answer, data={
            "question": 3,
            "choice": None,
            "user_id": 1,
            "text": "Tomas Haake"
        })
        self.assertEqual(result.status_code, 201)
        result = self.client.post(self.url_answer, data={
            "question": 2,
            "choice": None,
            "user_id": 1,
            "text": "Tomas Haake"
        })
        self.assertEqual(result.status_code, 400)

    def test_answer_one_choice(self):
        self._fixture_three_polls()
        result = self.client.post(self.url_answer, data={
            "question": 2,
            "choice": 1,
            "user_id": 3,
            "text": None
        })
        self.assertEqual(result.status_code, 201)
        result = self.client.post(self.url_answer, data={
            "question": 2,
            "choice": 2,
            "user_id": 3,
            "text": None
        })
        self.assertEqual(result.status_code, 400)

    def test_answer_multiple_choice(self):
        self._fixture_three_polls()
        result = self.client.post(self.url_answer, data={
            "question": 1,
            "choice": 1,
            "user_id": 2,
            "text": None
        })
        self.assertEqual(result.status_code, 201)
        result = self.client.post(self.url_answer, data={
            "question": 1,
            "choice": 2,
            "user_id": 2,
            "text": None
        })
        self.assertEqual(result.status_code, 201)

    # getting selection of user's answers
    def test_get_users_answers(self):
        self._fixture_three_polls()
        self.client.post(self.url_answer, data={
            "question": 1,
            "choice": 1,
            "user_id": 2,
            "text": None
        })
        self.client.post(self.url_answer, data={
            "question": 1,
            "choice": 2,
            "user_id": 2,
            "text": None
        })
        self.client.post(self.url_answer, data={
            "question": 2,
            "choice": 1,
            "user_id": 3,
            "text": None
        })
        self.client.post(self.url_answer, data={
            "question": 3,
            "choice": None,
            "user_id": 2,
            "text": "Tomas Haake"
        })
        result = self.client.get(self.url_answer)
        self.assertEqual(len(result.data), 4)
        result = self.client.get(self.url_answer_get_user(2))
        check = [True for x in result.data if x.get('user_id') == 2]
        self.assertTrue(len(check) == 3)
        self.assertTrue(all(check))
