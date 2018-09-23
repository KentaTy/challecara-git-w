

# Create your views here.
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.utils import timezone

from .models import Choice, Question


# ListView汎用ビューで自動生成されるデフォルトのテンプレート名
#　　　　　　　　　　　　　　　→ <app name>/<model name>_list.html 
# <app name>はurls.pyで定義
# 自動生成されるコンテキスト変数は question_list。これに context_object_name 属性を与え、 latest_question_list を代わりに使用すると指定することで上書き。
# template_name 属性の指定で ListView に既存の "polls/index.html" テンプレートを使用するように伝える。

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """最後に公開された5つの質問を返します。（公開日時が未来のものは含まない）"""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

# DetailView汎用ビューで自動生成されるデフォルトのテンプレート名
#　　　　　　　　　　　　　　　→ <app name>/<model name>_detail.html 
# <app name>はurls.pyで定義、<model name>はDjangoモデル(Question)を使用しているため、コンテキスト変数としてふさわしいquestionという名前が自動生成。
# template_name 属性を指定すると、デフォルトでなく、指定したテンプレート名を使うようにDjango に伝えることができる。(detail部分)

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
