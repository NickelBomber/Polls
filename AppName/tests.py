import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from AppName.models import Question


# Create your tests here.

def create_question(question_text, days):
    """
    Creates a question with the given `question_text` published the given
    number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionMethodTests(TestCase):
    def test_was_published_recently(self):
        """
         False for questions whose pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertEqual(future_question.was_published_recently(), False)

    def test_was_published_with_recent_question(self):
        """
         True for questions within the last 24h.
        """
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=time)
        self.assertEqual(recent_question.was_published_recently(), True)

    def test_was_published_with_old_question(self):
        """
         False for questions whose pub_date is older than 24h.
        """
        time = timezone.now() + datetime.timedelta(days=1, hours=1)
        old_question = Question(pub_date=time)
        self.assertEqual(old_question.was_published_recently(), False)


class QuestionViewTests(TestCase):
    def test_index_view_with_no_questions(self):
        """
         If no question exists an approriate message should be displayed
        """
        response = self.client.get(reverse(("AppName:index")))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_index_view_with_a_past_question(self):
        """
         Questions with a pub_date in the past should be displayed on the index page.
        """
        create_question(question_text="Past Question", days=-30)
        response = self.client.get(reverse(("AppName:index")))
        self.assertQuerysetEqual(
            response.context["latest_question_list"], ['<Question: Past Question>'])

    def test_index_view_with_a_future_question(self):
        """
        Questions with a pub_date in the future should not be displayed on the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('AppName:index'))
        self.assertContains(response, "No polls are available.", status_code=200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions should be displayed.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('AppName:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_index_view_with_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('AppName:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )