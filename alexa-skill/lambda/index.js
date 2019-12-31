// This skill connects to the EV3 MINDSTORMS Game Station Gadget.
//
// Jason Allemann
//
const Alexa = require( 'ask-sdk-core' );
const Util = require( './util' );
const Common = require( './common' );

// The custom directive to be sent by this skill
const NAMESPACE = 'Custom.Mindstorms.Gadget';
const NAME_CONTROL = 'control';

const PlayPrompt = "What would you like to play?"

// The music files to be used for the Hot Potato and Musical Chairs games.
const Music1 = '<audio src="https://raw.githubusercontent.com/jasonallemann/gamestation/master/audio/muffinman20s.mp3"/>'
const Music2 = '<audio src="https://raw.githubusercontent.com/jasonallemann/gamestation/master/audio/bunnyhop20s.mp3"/>'
const Music3 = '<audio src="https://raw.githubusercontent.com/jasonallemann/gamestation/master/audio/twirlytops20s.mp3"/>'

const IncorrectSound = '<audio src="soundbank://soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_negative_response_02"/>';
const CorrectSound = '<audio src="soundbank://soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_positive_response_01"/>';

// Randomly selects one of the three music files.
function randomMusic()
{
    var AudioSSML = Music1;
    var option = Math.floor( Math.random() * 3 );

    if( option === 0 ) { AudioSSML = Music1; }
    else if( option === 1 ) { AudioSSML = Music2; }
    else { AudioSSML = Music3; }
    
    return AudioSSML;
}

// Selects a random confirmation prefix word.
function randomConfirmation()
{
    var Response = "Okay, ";
    var option = Math.floor( Math.random() * 4 );

    if( option === 0 ) { Response = "Okay, "; }
    else if( option === 1 ) { Response = "Sure, "; }
    else if( option === 2 ) { Response = "Allright, "; }
    else { Response = "You got it, "; }
    
    return Response;
}

// Selects a random failure prefix word.
function randomFail()
{
    var Response = "Sorry ";
    var option = Math.floor( Math.random() * 4 );

    if( option === 0 ) { Response = "Sorry "; }
    else if( option === 1 ) { Response = "Too bad, "; }
    else if( option === 2 ) { Response = "Bad news "; }
    else { Response = "Oh no, "; }
    
    return Response;
}

// Selects a random failure prefix word, all with trailing commas.
function randomFail2()
{
    var Response = "Sorry, ";
    var option = Math.floor( Math.random() * 3 );

    if( option === 0 ) { Response = "Sorry, "; }
    else if( option === 1 ) { Response = "Oooh, "; }
    else { Response = "Oh no, "; }
    
    return Response;
}

// Selects a random correct word.
function randomCorrect()
{
    var Response = "Correct!";
    var option = Math.floor( Math.random() * 3 );

    if( option === 0 ) { Response = "Correct!"; }
    else if( option === 1 ) { Response = "You got it."; }
    else { Response = "Nice one."; }
    
    return Response;
}

// Selects a random success prefix word.
function randomSuccess()
{
    var Response = "Congratulations ";
    var option = Math.floor( Math.random() * 3 );

    if( option === 0 ) { Response = "Congratulations "; }
    else if( option === 1 ) { Response = "Great job "; }
    else { Response = "Good job "; }
    
    return Response;
}

const LaunchRequestHandler = {
    canHandle( handlerInput )
    {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'LaunchRequest';
    },
    handle: async function( handlerInput )
    {
        let request = handlerInput.requestEnvelope;
        let { apiEndpoint, apiAccessToken } = request.context.System;
        let apiResponse = await Util.getConnectedEndpoints(apiEndpoint, apiAccessToken);
        if ((apiResponse.endpoints || []).length === 0)
        {
            return handlerInput.responseBuilder
            .speak( `I couldn't find the game station. Make sure the EV3 is turned on and the game station program is running.` )
            .getResponse();
        }

        // Store the gadget endpointId to be used in this skill session
        let endpointId = apiResponse.endpoints[0].endpointId || [];
        Util.putSessionAttribute( handlerInput, 'endpointId', endpointId );

        return handlerInput.responseBuilder
            .speak( PlayPrompt )
            .reprompt( PlayPrompt )
            .getResponse();
    }
};

//
// Handler for when the use asks what games can be played.
//
const GameQueryIntentHandler = {
    canHandle(handlerInput)
    {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'GameQueryIntent';
    },
    handle: function( handlerInput )
    {
        console.log( '#### Game Query Handler. ####');
        return handlerInput.responseBuilder
            .speak( `You can play Simon, LEGO Trivia, Musical Chairs, Hot Potato, or Race to the Top.` )
            .reprompt( PlayPrompt )
            .getResponse();
    }
}

//
// Handler for when the use asks for instructions on how to play a game.
//
const InstructionsIntentHandler = {
    canHandle(handlerInput)
    {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'InstructionsIntent';
    },
    handle: function( handlerInput )
    {
        console.log( '#### Instructions Handler. ####');
        console.log( "#### Game: " + handlerInput.requestEnvelope.request.intent.slots.Game.value );

        let gameName = handlerInput.requestEnvelope.request.intent.slots.Game.value;

        var speechOutput = "I don't know the game " + gameName;
        if( gameName.toLowerCase() === "simon" )
        {
            speechOutput = `After I <phoneme alphabet="ipa" ph="rid">read</phoneme> a list of colors, press the corresponding buttons in the same order. `
            speechOutput += "Level 1 starts with a single color, and each level will add a random color to the sequence. "
            speechOutput += "If you reach level ten, you will win the game."
        }
        else if( gameName.toLowerCase() === "lego trivia"
            || gameName.toLowerCase() === "trivia" )
        {
            speechOutput = "When a question is being asked, the first player to press their button will have a chance to answer it."
            speechOutput += ' If they answer correctly, they will move up the game board, and another question will be asked.'
            speechOutput += ' If they answer incorrectly, the next player to press their button will have a chance to answer.'
            speechOutput += ' The first player to answer three questions correctly, wins.'
        }
        else if( gameName.toLowerCase() === "musical chairs" )
        {
            speechOutput = "Wait for the music to stop, then press your button. The player slowest to react will be eliminated from the next round. "
            speechOutput += 'The remaining players will play again, and the last player remaining is the winner.'
        }
        else if( gameName.toLowerCase() === "hot potato" )
        {
            speechOutput = "When you receive the potato, you're player will move up on the game board. To pass the potato to the next player, press your button. "
            speechOutput += "If you are caught holding the potato when the music stops, you will be eliminated from the next round. The last player remaining is the winner."
        }
        else if( gameName.toLowerCase() === "race to the top" )
        {
            speechOutput = "After I count down to the start of the race, press your button as quickly as possible. "
            speechOutput += "The faster you press your button, the quicker you will move up. The first player to the top wins."
        }

        return handlerInput.responseBuilder
            .speak( speechOutput )
            .reprompt( PlayPrompt )
            .getResponse();
    }
}

//
// Handler for when the user asks to play Simon.
//
const SimonIntentHandler = {
    canHandle(handlerInput)
    {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'SimonIntent';
    },
    handle: function( handlerInput )
    {
        const attributesManager = handlerInput.attributesManager;
        const endpointId = attributesManager.getSessionAttributes().endpointId || [];
        console.log( '#### Start playing Simon. ####');

        // Set up the directive to tell the EV3 to start playing Simon.
        const directive = Util.build(endpointId, NAMESPACE, NAME_CONTROL,
            { type: 'simonStartGame' } );
            
        // Set the token to track the event handler
        const token = handlerInput.requestEnvelope.request.requestId;
        Util.putSessionAttribute( handlerInput, 'token', token );

        return handlerInput.responseBuilder
            .speak( randomConfirmation() + `let's play Simon.` )
            .addDirective( directive )
            .addDirective( Util.buildStartEventHandler( token, 60000, {} ) )
            .getResponse();
    }
};

//
// Handler for when the user asks to play Musical Chairs.
//
const MusicalChairsIntentHandler = {
    canHandle(handlerInput)
    {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'MusicalChairsIntent';
    },
    handle: function( handlerInput )
    {
        const attributesManager = handlerInput.attributesManager;
        const endpointId = attributesManager.getSessionAttributes().endpointId || [];
        console.log( '#### Start playing musical chairs. ####');

        // Set up the directive to tell the EV3 to start playing Musical Chairs.
        const directive = Util.build(endpointId, NAMESPACE, NAME_CONTROL,
            { type: 'musicalChairsStartGame' } );
            
        // Set the token to track the event handler
        const token = handlerInput.requestEnvelope.request.requestId;
        Util.putSessionAttribute( handlerInput, 'token', token );

        return handlerInput.responseBuilder
            .speak( randomConfirmation() + `press your button when the music stops.` + randomMusic() )
            .addDirective( directive )
            .addDirective( Util.buildStartEventHandler( token, 60000, {} ) )
            .getResponse();
    }
}

//
// Hot Potato intent handler.
// Will send a 'hotPotatoStartGame' notification to the EV3 and start playing the background music.
//
const HotPotatoIntentHandler = {
    canHandle( handlerInput )
    {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'HotPotatoIntent';
    },
    handle: function( handlerInput )
    {
        const attributesManager = handlerInput.attributesManager;
        const endpointId = attributesManager.getSessionAttributes().endpointId || [];
        console.log( '#### Start playing hot potato. ####');

        // Set up the directive to tell the EV3 to start playing Hot Potoato.
        const directive = Util.build(endpointId, NAMESPACE, NAME_CONTROL,
            { type: 'hotPotatoStartGame' } );
            
        // Set the token to track the event handler
        const token = handlerInput.requestEnvelope.request.requestId;
        Util.putSessionAttribute( handlerInput, 'token', token );

        return handlerInput.responseBuilder
            .speak( randomConfirmation() + `press your button to pass the potato. Don't be caught with it when the music stops.` + randomMusic() )
            .addDirective( directive )
            .addDirective( Util.buildStartEventHandler( token, 60000, {} ) )
            .getResponse();
    }
}

//
// Handler for when the user asks to play Race to the Top.
//
const RaceIntentHandler = {
    canHandle( handlerInput )
    {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'RaceIntent';
    },
    handle: function( handlerInput )
    {
        const attributesManager = handlerInput.attributesManager;
        const endpointId = attributesManager.getSessionAttributes().endpointId || [];
        console.log( '#### Start playing race to the top. ####');

        // Directive to tell the EV3 to start playing Race to the Top.
        const directive = Util.build(endpointId, NAMESPACE, NAME_CONTROL,
            { type: 'raceStartGame' } );
            
        // Set the token to track the event handler
        const token = handlerInput.requestEnvelope.request.requestId;
        Util.putSessionAttribute( handlerInput, 'token', token );

        return handlerInput.responseBuilder
            .speak( randomConfirmation() + `tap your button to move your player up the board. Are you ready? Three<break time="0.25s"/>Two<break time="0.25s"/>One<break time="0.25s"/>Go!` )
            .addDirective( directive )
            .addDirective( Util.buildStartEventHandler( token, 60000, {} ) )
            .getResponse();
    }
}

//
// Handler for when the user asks to play Trivia.
//
const TriviaIntentHandler = {
    canHandle( handlerInput )
    {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'TriviaIntent';
    },
    handle: function( handlerInput )
    {
        const attributesManager = handlerInput.attributesManager;
        const endpointId = attributesManager.getSessionAttributes().endpointId || [];
        console.log( '#### Start playing Trivia. ####');

        // Directive to tell the EV3 to start playing Race to the Top.
        const directive = Util.build(endpointId, NAMESPACE, NAME_CONTROL,
            { type: 'triviaStartGame' } );
            
        // Set the token to track the event handler
        const token = handlerInput.requestEnvelope.request.requestId;
        Util.putSessionAttribute( handlerInput, 'token', token );

        return handlerInput.responseBuilder
            .speak( randomConfirmation() + `tap your button when you know the answer.` )
            .addDirective( directive )
            .addDirective( Util.buildStartEventHandler( token, 60000, {} ) )
            .getResponse();
    }
}

function compareTriviaAnswer( slots, answer )
{
  for( const slot in slots )
  {
    if( Object.prototype.hasOwnProperty.call( slots, slot ) && slots[slot].value !== undefined )
    {
      if( slots[slot].value.toString().toLowerCase() === answer.toString().toLowerCase() )
      {
        return true;
      }
    }
  }

  return false;
}

//
// Handler for when the user gives a trivia answer.
//
const TriviaAnswerIntentHandler = {
    canHandle( handlerInput )
    {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && handlerInput.attributesManager.getSessionAttributes().state === "WaitingForAnswer"
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'TriviaAnswerIntent';
    },
    handle: function( handlerInput )
    {
        const attributesManager = handlerInput.attributesManager;
        const endpointId = attributesManager.getSessionAttributes().endpointId || [];
        console.log( '#### Trivia Answer Handler. ####');

        var attributes = handlerInput.attributesManager.getSessionAttributes();
        attributes.state = "";
        handlerInput.attributesManager.setSessionAttributes( attributes );

        var speechOutput = randomFail2() + "that was incorrect, anyone else? " + attributes.triviaOptions;
        var commandType = 'triviaIncorrectAnswer';
        const answer = attributesManager.getSessionAttributes().triviaAnswer;
        const isCorrect = compareTriviaAnswer( handlerInput.requestEnvelope.request.intent.slots, answer );
        if( isCorrect )
        {
            speechOutput = randomCorrect();
            commandType = 'triviaCorrectAnswer';
        }

        // Directive to tell the EV3 how the answer was answered.
        const directive = Util.build(endpointId, NAMESPACE, NAME_CONTROL,
            { type: commandType } );
            
        // Set the token to track the event handler
        const token = handlerInput.requestEnvelope.request.requestId;
        Util.putSessionAttribute( handlerInput, 'token', token );

        return handlerInput.responseBuilder
            .speak( speechOutput )
            .addDirective( directive )
            .addDirective( Util.buildStartEventHandler( token, 60000, {} ) )
            .getResponse();
    }
}

//
// Handler for when the EV3 sends an event.
//
const EventsReceivedRequestHandler = {
    canHandle(handlerInput)
    {
        let { request } = handlerInput.requestEnvelope;
        console.log( 'Request type: ' + Alexa.getRequestType(handlerInput.requestEnvelope ) );
        if( request.type !== 'CustomInterfaceController.EventsReceived' ) return false;

        const attributesManager = handlerInput.attributesManager;
        let sessionAttributes = attributesManager.getSessionAttributes();
        let customEvent = request.events[0];

        // Validate event token
        if( sessionAttributes.token !== request.token )
        {
            console.log( "Event token doesn't match. Ignoring this event" );
            return false;
        }

        // Validate endpoint
        let requestEndpoint = customEvent.endpoint.endpointId;
        if( requestEndpoint !== sessionAttributes.endpointId )
        {
            console.log( "Event endpoint id doesn't match. Ignoring this event" );
            return false;
        }
        return true;
    },
    handle( handlerInput )
    {
        const attributesManager = handlerInput.attributesManager;
        const endpointId = attributesManager.getSessionAttributes().endpointId || [];
        const token = attributesManager.getSessionAttributes().token;
        var attributes = handlerInput.attributesManager.getSessionAttributes();

        let customEvent = handlerInput.requestEnvelope.request.events[0];
        let payload = customEvent.payload;
        var payloadJSON;
        let name = customEvent.header.name;

        console.log( "#### Custom Event: " + name );
        var speechOutput = "";
        var option = 0;

        //
        // Simon event handlers
        //
        if( name === 'simonSequence' )
        {
            console.log( payload )
            for( var i = 0; i < payload.length; i++ )
            {
                console.log( payload[i]);
                if( i !== 0 ) { speechOutput = speechOutput + " "; }
                speechOutput = speechOutput + payload[i];
            }
            console.log( speechOutput );

            const directive = Util.build(endpointId, NAMESPACE, NAME_CONTROL,
                { type: 'simonTest' } );

            return handlerInput.responseBuilder
                .speak( speechOutput, "REPLACE_ENQUEUED" )
                .addDirective( directive )
                .addDirective( Util.buildStartEventHandler( token, 60000, {} ) )
                .getResponse();
        }
        else if( name === 'simonEnd' )
        {
            console.log( payload );
            payloadJSON = JSON.parse( payload );
            console.log( "#### Simon level: " + payloadJSON.level + ", passed: " + payloadJSON.passed );
            if( payloadJSON.level >= 10 && payloadJSON.passed === true)
            {
                speechOutput = CorrectSound + "Congratulations! You successfully finished level ten. What would you like to play next?";
            }
            else if ( payloadJSON.level <= 1 )
            {
                speechOutput = IncorrectSound + "Wow, you aren't very good at this one. Maybe you should try another game.";
            }
            else
            {
                speechOutput = IncorrectSound + randomFail() + ", that wasn't right, but you successfully completed level ";
                speechOutput += String( payloadJSON.level - 1 );
                speechOutput += ". What would you like to play next?";
            }

            const directive = Util.build(endpointId, NAMESPACE, NAME_CONTROL,
                { type: 'simonEndGame' } );

            return handlerInput.responseBuilder
                .speak( speechOutput )
                .addDirective( directive )
                .addDirective( Util.buildStopEventHandlerDirective( handlerInput ) )
                .reprompt( PlayPrompt )
                .getResponse();
        }
        //
        // Musical Chairs event handlers
        //
        else if( name === 'musicalChairsStopMusic' )
        {
            const directive = Util.build(endpointId, NAMESPACE, NAME_CONTROL,
                { type: 'musicalChairsMusicStopped' } );

            return handlerInput.responseBuilder
                .speak( '<break time="0.25s"/>', "REPLACE_ALL" )
                .addDirective( directive )
                .addDirective( Util.buildStartEventHandler( token, 60000, {} ) )
                .getResponse();
        }
        else if( name === 'musicalChairsFinishedRound' )
        {
            console.log( payload );
            option = Math.floor( Math.random() * 4 );
            console.log( option );
            if( option === 0 ) { speechOutput = randomFail() + `${payload}, you weren't fast enough.`; }
            else if( option === 1 ) { speechOutput = randomFail() + `${payload}, you didn't quite make it.`; }
            else if( option === 2 ) { speechOutput = randomFail() + `${payload}, you didn't get a chair.`; }
            else { speechOutput = randomFail() + `${payload}, you missed out.`; }
            console.log( speechOutput );

            const directive = Util.build(endpointId, NAMESPACE, NAME_CONTROL,
                { type: 'musicalChairsNextRound' } );

            return handlerInput.responseBuilder
                .speak( speechOutput + randomMusic(), "REPLACE_ALL"  )
                .addDirective( directive )
                .getResponse();
        }
        else if( name === 'musicalChairsFinishedGame' )
        {
            console.log( payload );
            speechOutput = randomSuccess() + `${payload}! You got the last chair. What would you like to play next?`;

            const directive = Util.build(endpointId, NAMESPACE, NAME_CONTROL,
                { type: 'musicalChairsFinishGame' } );

            return handlerInput.responseBuilder
                .speak( speechOutput, "REPLACE_ALL" )
                .addDirective( directive )
                .addDirective( Util.buildStopEventHandlerDirective( handlerInput ) )
                .reprompt( PlayPrompt )
                .getResponse();
        }
        //
        // Hot potato event handlers
        //
        else if( name === 'hotPotatoStopMusic' )
        {
            const directive = Util.build(endpointId, NAMESPACE, NAME_CONTROL,
                { type: 'hotPotatoMusicStopped' } );

            return handlerInput.responseBuilder
                .speak( '<break time="0.25s"/>', "REPLACE_ALL" )
                .addDirective( directive )
                .addDirective( Util.buildStartEventHandler( token, 60000, {} ) )
                .getResponse();
        }
        else if( name === 'hotPotatoFinishedRound' )
        {
            console.log( payload );
            option = Math.floor( Math.random() * 3 );
            console.log( option );
            if( option === 0 ) { speechOutput = randomFail() + `${payload}, you ended up with the potato.`; }
            else if( option === 1 ) { speechOutput = randomFail() + `${payload}, you had the hot potato.`; }
            else { speechOutput = randomFail() + `${payload}, you had the potato.`; }

            const directive = Util.build(endpointId, NAMESPACE, NAME_CONTROL,
                { type: 'hotPotatoNextRound' } );

            return handlerInput.responseBuilder
                .speak( speechOutput + randomMusic(), "REPLACE_ALL"  )
                .addDirective( directive )
                .getResponse();
        }
        else if( name === 'hotPotatoFinishedGame')
        {
            console.log( payload );
            speechOutput = randomSuccess() + `${payload}! You won. What would you like to play next?`;

            const directive = Util.build(endpointId, NAMESPACE, NAME_CONTROL,
                { type: 'hotPotatoFinishGame' } );

            return handlerInput.responseBuilder
                .speak( speechOutput, "REPLACE_ALL" )
                .addDirective( directive )
                .addDirective( Util.buildStopEventHandlerDirective( handlerInput ) )
                .reprompt( PlayPrompt )
                .getResponse();
        }
        //
        // Race to the Top event handlers
        //
        else if( name === 'raceFinishedGame' )
        {
            console.log( payload );
            console.log( payload[0] );
            speechOutput = randomSuccess() + `${payload[0]}! You were the fastest. What would you like to play next?`;

            const directive = Util.build(endpointId, NAMESPACE, NAME_CONTROL,
                { type: 'raceFinishGame' } );

            return handlerInput.responseBuilder
                .speak( speechOutput, "REPLACE_ALL" )
                .addDirective( directive )
                .addDirective( Util.buildStopEventHandlerDirective( handlerInput ) )
                .reprompt( PlayPrompt )
                .getResponse();
        }
        //
        // Trivia event handlers
        //
        else if( name === 'triviaAskQuestion')
        {
            console.log( payload );
            payloadJSON = JSON.parse( payload );
            console.log( payloadJSON["question"] );
            console.log( payloadJSON["answer"] );
            speechOutput = payloadJSON["question"] + " " + payloadJSON["hint"];
            
            attributes.triviaAnswer = payloadJSON["answer"];
            attributes.triviaOptions = payloadJSON["hint"];
            handlerInput.attributesManager.setSessionAttributes( attributes );

            const directive = Util.build(endpointId, NAMESPACE, NAME_CONTROL,
                { type: 'triviaAskedQuestion' } );

            return handlerInput.responseBuilder
                .speak( speechOutput, "ENQUEUE" )
                .addDirective( directive )
                .getResponse();
        }
        else if( name === 'triviaAskForAnswer')
        {
            console.log( payload );
            speechOutput = `Okay ${payload}`;

            attributes.state = "WaitingForAnswer";
            handlerInput.attributesManager.setSessionAttributes( attributes );

            return handlerInput.responseBuilder
                .speak( speechOutput, "REPLACE_ALL" )
                .reprompt( `Waiting for an answer, ${payload}.` )
                .getResponse();
        }
        else if( name === 'triviaFinishedGame' )
        {
            console.log( payload );
            speechOutput = randomSuccess() + `${payload}! You really know your stuff! What would you like to play next?`;

            const directive = Util.build(endpointId, NAMESPACE, NAME_CONTROL,
                { type: 'triviaFinishGame' } );

            return handlerInput.responseBuilder
                .speak( speechOutput, "REPLACE_ALL" )
                .addDirective( directive )
                .addDirective( Util.buildStopEventHandlerDirective( handlerInput ) )
                .reprompt( PlayPrompt )
                .getResponse();
        }
        else
        {
            speechOutput = "Event not recognized.";
        }
        
        return handlerInput.responseBuilder
            .reprompt( PlayPrompt )
            .getResponse();
    }
};

const ExpiredRequestHandler = {
    canHandle( handlerInput )
    {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'CustomInterfaceController.Expired'
    },
    handle( handlerInput )
    {
        console.log("#### Custom Event Expiration Input ####");

        // Set the token to track the event handler
        const token = handlerInput.requestEnvelope.request.requestId;
        Util.putSessionAttribute(handlerInput, 'token', token);

        const attributesManager = handlerInput.attributesManager;
            return handlerInput.responseBuilder
                .getResponse();
    }
};


// Generic error handling to capture any syntax or routing errors. If you receive an error
// stating the request handler chain is not found, you have not implemented a handler for
// the intent being invoked or included it in the skill builder below.
const ErrorHandler = {
    canHandle() {
        return true;
    },
    handle(handlerInput, error) {
        console.log(`~~~~ Error handled: ${error.stack}`);
        const speakOutput = `Sorry, I had trouble doing what you asked. Please try again.`;

        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(speakOutput)
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

// The SkillBuilder acts as the entry point for your skill, routing all request and response
// payloads to the handlers above. Make sure any new handlers or interceptors you've
// defined are included below. The order matters - they're processed top to bottom.
exports.handler = Alexa.SkillBuilders.custom()
    .addRequestHandlers(
        LaunchRequestHandler,
        GameQueryIntentHandler,
        InstructionsIntentHandler,
        SimonIntentHandler,
        MusicalChairsIntentHandler,
        HotPotatoIntentHandler,
        RaceIntentHandler,
        TriviaIntentHandler,
        TriviaAnswerIntentHandler,
        EventsReceivedRequestHandler,
        ExpiredRequestHandler,
        Common.HelpIntentHandler,
        Common.CancelAndStopIntentHandler,
        Common.SessionEndedRequestHandler,
        Common.IntentReflectorHandler, // make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
    )
    .addRequestInterceptors( Common.RequestInterceptor )
    .addErrorHandlers(
        ErrorHandler,
    )
    .lambda();
