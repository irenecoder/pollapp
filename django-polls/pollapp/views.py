from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse,Http404,HttpResponseRedirect
from .models import Question,Choice
from django.urls import reverse
from django.views import generic
from django.utils import timezone

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'pollapp/index.html'
    context_object_name = 'quiz_list'

    def get_queryset(self):
        """return the last five published questions(not including those set to be published in the future)"""
        return Question.objects.filter(date_created__lte=timezone.now()).order_by('-date_created')[:5]
class DetailView(generic.DetailView):
    model = Question
    template_name = 'pollapp/detail.html'

    def get_queryset(self):
        """excludes any questions that are not published yet"""
        return Question.objects.filter(date_created__lte=timezone.now())
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'pollapp/results.html'
    
def vote(request,question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'pollapp/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('pollapp:results', args=(question.id,)))


