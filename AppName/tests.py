import datetime

from django.test import TestCase
from django.utils import timezone

from AppName.models import Question
# Create your tests here.

class QuestionMethodTewsts(TestCase):

    def test_was_published_recently(self):
        """
        esd_publiched_recently() should return False for questions whose pub_date is in the future.
        :return:
        """
        time = timezone.now()+ datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertEqual(future_question.was_published_recently(), False)
