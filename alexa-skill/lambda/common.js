//
// Common intent handlers.
//
'use strict'

const Alexa = require('ask-sdk-core');

const HelpIntentHandler = {
    canHandle( handlerInput )
    {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'AMAZON.HelpIntent';
    },
    handle( handlerInput )
    {
        const speakOutput = 'You can play Simon, LEGO Trivia, Musical Chairs, Hot Potato, or Race to the Top. For instructions on how to play one of these games, just ask.';

        return handlerInput.responseBuilder
            .speak( speakOutput )
            .reprompt( "What would you like to play?" )
            .getResponse();
    }
};
const CancelAndStopIntentHandler = {
    canHandle(handlerInput)
    {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && (Alexa.getIntentName(handlerInput.requestEnvelope) === 'AMAZON.CancelIntent'
                || Alexa.getIntentName(handlerInput.requestEnvelope) === 'AMAZON.StopIntent');
    },
    handle( handlerInput )
    {
        const speakOutput = 'Thanks for playing!';
        return handlerInput.responseBuilder
            .speak( speakOutput )
            .getResponse();
    }
};
const SessionEndedRequestHandler = {
    canHandle(handlerInput)
    {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'SessionEndedRequest';
    },
    handle(handlerInput)
    {
        return handlerInput.responseBuilder
            .speak( "Thanks for playing!" )
            .getResponse();
    }
};

// For unhandled intents.
// The TriviaAnswerIntent is kind of a catch all, that will be triggered by many utterances that don't match
// other intents. We just specifically want to ignore it when that happens.
const IntentReflectorHandler = {
    canHandle(handlerInput)
    {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest';
    },
    handle(handlerInput)
    {
        const intentName = Alexa.getIntentName(handlerInput.requestEnvelope);
        var speakOutput = `You just triggered the unhandled ${intentName}`;
        
        if( intentName === 'TriviaAnswerIntent' )
        {
            speakOutput = `I don't understand that.`;
        }
        
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt( "What would you like to play?" )
            .getResponse();
    }
};

// Generic error handling to capture any syntax or routing errors. If you receive an error
// stating the request handler chain is not found, you have not implemented a handler for
// the intent being invoked or included it in the skill builder below.
const ErrorHandler = {
    canHandle()
    {
        return true;
    },
    handle( handlerInput, error )
    {
        console.log( `!!!! Error handled: ${error.stack}` );
        const speakOutput = `Sorry, something went wrong. Please try again.`;

        return handlerInput.responseBuilder
            .speak( speakOutput )
            .reprompt( speakOutput )
            .getResponse();
    }
};

// The request interceptor is used for request handling testing and debugging.
// It will simply log the request in raw json format before any processing is performed.
const RequestInterceptor = {
    process(handlerInput)
    {
        let { attributesManager, requestEnvelope } = handlerInput;
        let sessionAttributes = attributesManager.getSessionAttributes();

        // Log the request for debug purposes.
        console.log(`=====Request==${JSON.stringify(requestEnvelope)}`);
        console.log(`=========SessionAttributes==${JSON.stringify(sessionAttributes, null, 2)}`);
    }
};

module.exports = {
    HelpIntentHandler,
    CancelAndStopIntentHandler,
    SessionEndedRequestHandler,
    IntentReflectorHandler,
    ErrorHandler,
    RequestInterceptor
    };