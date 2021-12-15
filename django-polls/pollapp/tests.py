from django.test import TestCase
import datetime
from django.utils import timezone
from .models import Question
from django.urls import reverse


# Create your tests here.

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """was_published_recently() returns False for questions whose pub_date is in the future"""
        time= timezone.now() + datetime.timedelta(days=30)
        future_question = Question(date_created = time)
        self.assertIs(future_question.was_published_recently(),False)
    def was_published_recently_with_old_question(self):
        """was_published_recently() returns False for questions whose pub_date is older than 1 day"""
        time = timezone.now() - datetime.timedelta(days=1,seconds=1)
        old_question=Question(date_created=time)
        self.assertIs(old_question.was_published_recently(),False)

    def test_was_published_recently_with_recent_question(self):
        """was_published_recently() returns True for questions whose pub_date
        is within the last day."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(date_created=time)
        self.assertIs(recent_question.was_published_recently(), True)
    def create_question(quiz_text,days):
        """create a question with the given question_text and published the given number of days offset to now ."""
        time = timezone.now() + datetime.timedelta(days=days)
        return Question.objects.create(quiz_text=quiz_text,date_created=time)

    class QuestionINdexViewTests(TestCase):
        def test_no_questions(self):
            """if no questiona exist, an  appropriate message is displayed"""
            response = self.client.get(reverse('pollapp:index'))
            self.assertEqual(response.status_code,200)
            self.assertContains(response,"No polls are available")
            self.assertQuerysetEqual(response.context['quiz_list'],[])

        def test_past_question(self):
            """questions with a pub_date in the past are displayed on the index page"""
            question = create_question(quiz_text="past question",days=-30)
            response = self.client.get(reverse('pollapp:index'))
            self.assertQuerysetEqual(response.context['quiz_list'],[question])
        def test_future_question(self):
            """questions with a pub_date in the future aren't displayed on the index page"""
            create_question(quiz_text="future question",days=30)
            response = self.client.get(reverse('pollapp:index'))
            self.assertContains(response, "No polls are available")
            self.assertQuerysetEqual((response.context['quiz_list'],[]))
        def test_future_and_past_question(self):
            """even if future and past questions exist, only past questions are displayed"""
            question = create_question(quiz_text="Past question",days=-30)
            create_question(quiz_text="Future question",days=30)
            response = self.client.get(reverse('pollapp:index'))
            self.assertQuerysetEqual(response.context['quiz_list'],[question],)
        def test_two_past_questions(self):
            """THe questions index page may display multiple questions"""
            question1 = create_question(quiz_text="past question 1", days=-30)
            question2 = create_question(quiz_text="past question 2", days=-5)
            response = self.client.get(reverse('pollapp:index'))
            self.assertQuerysetEqual(response.context['quiz_list'],[question1,question2])

    class QuestionDetailViewTests(TestCase):
        def test_future_question(self):
            """the detail view of a question with a pub_date in the future returns a 404 not found"""
            future_question = create_question(quiz_text="future question",days=5)
            url = reverse('pollapp:detail',args=(future_question.id,))
            response = self.client.get(url)
            self.assertEqual(response.status_code,404)
        def test_past_question(self):
            """the detail view of a question with a pub_date in the past displays the question text"""
            past_question = create_question(quiz_text="past question",days=-5)
            url = reverse('pollapp:detail',args=(past_question.id,))
            response = self.client.get(url)
            self.assertContains(response,past_question.quiz_text)

