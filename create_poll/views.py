from asyncio.log import logger
from django.shortcuts import redirect, render
from models import app_models
import logging
import datetime

logger = logging.getLogger('create_poll.views')

def generate_id(entity):
    now = datetime.datetime.now()
    return entity+now.strftime("%Y%m%d%H%M%S%f")

def create_poll(request):
    if request.method == 'GET':
        return render(request, 'create_poll.html')
    
    if request.method == 'POST':
        request_dict = dict(request.POST)
        poll_id = generate_id('poll')

        new_poll = app_models.polls_list(poll_id=poll_id, poll_name = request_dict["poll_name"][0], poll_description = request_dict["poll_description"][0])
        new_poll.save()
        logger.info(f"Successfully created poll with id {poll_id}")

        # after saving poll details, delete csrf token and poll details from request dictionary
        del request_dict["csrfmiddlewaretoken"], request_dict["poll_name"], request_dict["poll_description"]

        # create structured question and options dictionary
        # ex: {'Q1': [['question asked'], [option1, option2, option3]], ...}
        question_dict = {}
        for keys in request_dict.keys():
            if len(keys) == 2 and keys not in question_dict:
                question_dict[keys] = [request_dict[keys], []]
            else:
                question_dict[keys[:2]][1].append(request_dict[keys][0])
        
        # testing if no of questions is > 10 or any question contain no of options > 10
        # returning to home if test fails
        try:
            if len(question_dict.keys()) > 10:
                app_models.polls_list.objects.filter(poll_id = poll_id).delete()
                logger.warning(f"Question limit criteria is not matching for poll_id-{poll_id}, reverting the saved changes")
                return redirect('/')
            for keys in question_dict.keys():
                if len(question_dict[keys][1]) > 10:
                    app_models.polls_list.objects.filter(poll_id = poll_id).delete()
                    logger.warning(f"Question-options limit criteria is not matching for poll_id-{poll_id}, reverting the saved changes")
                    return redirect('/')
        except Exception as e:
            logger.error(f"{e}")

        # save question and options dictionary, i is used to assign question no in database
        i = 1
        for keys in question_dict.keys():
            new_question = app_models.poll_questions(poll_id = poll_id, question_no = i, question = question_dict[keys][0][0], question_options = '|'.join(question_dict[keys][1]))
            new_question.save()
            i += 1
        logger.info(f"Successfully saved question-option details ({question_dict}) for poll_id-{poll_id}")
        
        return redirect(f'/results?poll_id={poll_id}')


