# Create your views here.
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.utils import timezone
from django.views import generic

from AppName.models import Question, Choice

class IndexView(generic.ListView):
    template_name = 'AppName/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'AppName/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'AppName/results.html'

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = RequestContext(request, {'latest_question_list': latest_question_list})
#     return render(request, 'AppName/index.html', context)
#
#
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "AppName/detail.html", {"question": question})
#
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'AppName/results.html', {'question': question})


def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "AppName/detail.html", {"question":p, "error_message":"You didn't select a choice"} )
    else:
        selected_choice.votes+=1
        selected_choice.save()

    return HttpResponseRedirect(reverse('AppName:results', args=(p.id,)))
