"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import boto3
import os
from boto3.dynamodb.conditions import Key, Attr

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = os.environ["greeting_msg"]
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "to hear available metrics, ask Alexa: tell me my metrics."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = os.environ["exit_msg"]
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def query_dynamodb_metric(table,metric):
    print("The Metric is:", metric)
    response = table.get_item(
        Key={'metric':metric}
    )
    #print(response)
    #print(response['Item']['value'])
    try:
        return response['Item']['value']
    except KeyError:
        return -1
    except Exception:
        return -1

def get_metric_from_session(table, intent, session):
    session_attributes = {}
    reprompt_text = None
    metric_value = query_dynamodb_metric(table, intent['slots'][os.environ["slot_name"]]['value'].upper())
    if metric_value:
        speech_output = "The value for " + intent['slots'][os.environ["slot_name"]]['value'] + " is " + str(metric_value)
        should_end_session = True
    else:
        speech_output = "I'm not sure what that metric is. " \
                        "Please ask for another metric"
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(table, session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])

def on_launch(table, launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(table, intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name.upper() == os.environ["intent_name"].upper():
        return get_metric_from_session(table, intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(table, session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    #print("event.session.application.applicationId=" + event['session']['application']['applicationId'])
    print(event)
    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")
    indexEndRegion = context.invoked_function_arn[15:30].find(":")+15
    region = context.invoked_function_arn[15:indexEndRegion]
    dynamodb = boto3.resource('dynamodb', region_name=region, endpoint_url="https://dynamodb."+region+".amazonaws.com")
    metrics_table = dynamodb.Table(os.environ["metrics_table"])
    try:
        if event['session']['new']:
            on_session_started(metrics_table, {'requestId': event['request']['requestId']}, event['session'])
    except KeyError:
        print("Message")
        
    if event['request']['type'] == "LaunchRequest":
        return on_launch(metrics_table, event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(metrics_table, event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(metrics_table, event['request'], event['session'])
