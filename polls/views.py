from django.shortcuts import render, Http404,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .models import Question,Choice
from django.template import loader
from django.db.models import F
from django.urls import reverse

# Create your views here.
def index(request):
   # return HttpResponse("Hell World, You're at the Polls Index.") 
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    #output = ", ".join([q.question_text for q in latest_question_list])
    #template = loader.get_template("polls/index.html")
    context = {
        "latest_question_list": latest_question_list,
    }
    #return HttpResponse(output) 

    #Instead of using the loader, we can use the render shortcut
    #return HttpResponse(template.render(context,request))
    return render(request,"polls/index.html",context)

def detail(request,question_id): 
    #return HttpResponse("You're looking at Question %s." %question_id) 
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    context = {"question":question}
    return render(request,"polls/details.html",context)


def results(request,question_id):
    #response = "You're looking at the results of question %s."
    #return HttpResponse(response % question_id)
    question = get_object_or_404(Question, pk=question_id)
    context = {"question":question}
    return render(request,"polls/results.html",context)


#def vote(request,question_id):
#    return HttpResponse("You're Voting on Question %s." %question_id)

def vote(request,question_id): 
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        #Redisplay the Question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question":question,
                "error_message":"You didn't select a choice.",
            },
        ) 
    else:
        selected_choice.votes = F("votes") +1
        selected_choice.save()
        ## Always return an HttpResponseRedirect after succesfully dealing wit data.
        #This prevents data from being posted twice if a user hits the BAck button.
        return HttpResponseRedirect(reverse("polls:results",args=(question.id,)))