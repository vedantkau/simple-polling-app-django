from django.shortcuts import render, redirect
from models import app_models
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import datetime
import logging

logger = logging.getLogger('respond_poll.views')

def generate_id(entity):
    now = datetime.datetime.now()
    return entity+now.strftime("%Y%m%d%H%M%S%f")


def respond_poll(request):
    if request.method == 'GET':

        # getting question, options data for a poll
        try:
            poll_data = app_models.polls_list.objects.get(poll_id=request.GET.get('poll_id'))
            if poll_data.disabled:
                poll_question_data = None
            else:
                poll_question_data = app_models.poll_questions.objects.filter(poll_id=request.GET.get('poll_id'))
                for questions in poll_question_data:
                    questions.question_options = questions.question_options.split("|")

        except ObjectDoesNotExist:
            poll_data = None
            poll_question_data = None
        except Exception as e:
            poll_data = None
            poll_question_data = None
            logger.error(f"{e}")

        # setting a cookie with a response_id to identify a user
        response_obj = render(request, 'respond_poll.html', {'poll':poll_data, 'poll_questions': poll_question_data})
        response_id = request.COOKIES.get('response_id')
        if not response_id:
            response_id = generate_id('resp')
            response_obj.set_cookie('response_id', response_id)
        if not poll_data:
            logger.warning(f"No poll data found for poll_id-{request.GET.get('poll_id')} to register response by {response_id}")
        else:
            logger.info(f"Found poll data for poll_id-{request.GET.get('poll_id')} to register response by {response_id}")
        
        return response_obj
        
    if request.method == 'POST':
        request_dict = dict(request.POST)

        poll_id = request_dict["poll_id"][0]
        response_id = request.COOKIES.get('response_id')

        if response_id:
            del request_dict["csrfmiddlewaretoken"], request_dict["poll_id"]

            # a logic to check if a user is double voting a poll
            # logic will skip saving the vote if it finds the same response_id for a poll in database
            try:
                app_models.poll_responses.objects.get(poll_id = poll_id, response_id = response_id)
                logger.info(f"Prevented duplicate response for poll_id-{request.GET.get('poll_id')} by {response_id}")
            except MultipleObjectsReturned:
                logger.info(f"Prevented duplicate response for poll_id-{request.GET.get('poll_id')} by {response_id}")
            except ObjectDoesNotExist:
                for que_no in request_dict:
                    poll_response = app_models.poll_responses(poll_id = poll_id, response_id=response_id, question_no=que_no, answer=request_dict[que_no][0])
                    poll_response.save()
                    logger.info(f"Successfully registered response ({que_no}:{request_dict[que_no][0]}) for poll_id-{poll_id} by {response_id}")
            except Exception as e:
                logger.error(f"{e}")
            
            return redirect(f'/results?poll_id={poll_id}')
        else:
            return redirect(f'/respond?poll_id={poll_id}')
