from django.db import models


class Poll(models.Model):
    name = models.CharField(max_length=64, blank=False)
    description = models.CharField(max_length=256, blank=True)
    date_start = models.DateField(null=True, db_index=True)
    date_finish = models.DateField(null=True, db_index=True)

    def __str__(self):
        return self.name


class AnswerType:
    TEXT = 'text'
    SINGLE = 'one_choice'
    MULTIPLE = 'mult_choice'
    STATE = [
        (TEXT, 'text'),
        (SINGLE, 'one_choice'),
        (MULTIPLE, 'mult_choice'),
    ]


class Question(models.Model):
    question = models.CharField(max_length=512, unique=True)
    type = models.CharField(max_length=24, choices=AnswerType.STATE, default=AnswerType.SINGLE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, db_index=True)

    def __str__(self):
        return self.question


class Choice(models.Model):
    text = models.CharField(max_length=512)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, db_index=True)

    def __str__(self):
        return self.text


class Answer(models.Model):
    user_id = models.IntegerField(null=False, db_index=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True)
    text = models.TextField(max_length=2048, null=True)
