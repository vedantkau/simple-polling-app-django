from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from models import app_models
import logging

logger = logging.getLogger('poll_results.views')

def view_poll_result(request):
    
    try:
        poll_data = app_models.polls_list.objects.get(poll_id = request.GET.get("poll_id"))

        # create aggregations to calculate response count overall and per question
        poll_responses_data = app_models.poll_responses.objects.raw("select 1 as id, question_no, answer, count(*) as question_resp_count "\
                                                                    "from models_poll_responses group by question_no, answer, poll_id "\
                                                                    "having poll_id = %s", [request.GET.get("poll_id")])                                                        
        total_response_count = len(list(app_models.poll_responses.objects.raw("select distinct response_id, 1 as id from models_poll_responses "\
                                                                    "where poll_id = %s", 
                                                                    [request.GET.get("poll_id")])))
        poll_questions_data = app_models.poll_questions.objects.filter(poll_id=request.GET.get("poll_id"))

        # create structured dictionary to be passed to page
        que_resp_stat = {}
        for questions in poll_questions_data:
            que_resp_stat[questions.question_no] = [questions.question, 
                        dict(zip(questions.question_options.split("|"), [0 for _ in range(len(questions.question_options.split("|")))]))]
        for responses in poll_responses_data:
            que_resp_stat[responses.question_no][1][responses.answer] = round((responses.question_resp_count/total_response_count)*100, 1)
        logger.info(f"Poll results found for poll_id-{request.GET.get('poll_id')} with response count of {total_response_count} requested by {request.COOKIES.get('response_id')}")

    except ObjectDoesNotExist:
        poll_data = None
        que_resp_stat = {}
        total_response_count = 0
        logger.warning(f"No data found for poll_id-{request.GET.get('poll_id')} requested by {request.COOKIES.get('response_id')}")
    except Exception as e:
        poll_data = None
        que_resp_stat = {}
        total_response_count = 0
        logger.error(f"{e}")

    return render(request, 'poll_results.html', {"poll": poll_data, "poll_stats": que_resp_stat, "total_resps": total_response_count})
