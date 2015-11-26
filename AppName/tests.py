import datetime

from django.test import TestCase
from django.utils import timezone

from AppName.models import Question
# Create your tests here.

class QuestionMethodTests(TestCase):

    def test_was_published_recently(self):
        """
        :return: False for questions whose pub_date is in the future.
        """
        time = timezone.now()+ datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertEqual(future_question.was_published_recently(), False)

    def test_was_published_with_recent_question(self):
        """
        :return: True for questions within the last 24h.
        """
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=time)
        self.assertEqual(recent_question.was_published_recently(), True)

    def test_was_published_with_old_question(self):
        """
        :return: False for questions whose pub_date is older than 24h.
        """
        time = timezone.now()+ datetime.timedelta(days=1, hours=1)
        old_question = Question(pub_date=time)
        self.assertEqual(old_question.was_published_recently(), False)

