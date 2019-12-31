//
// Utility functions.
//
'use strict';

const Https = require('https');
const AWS = require('aws-sdk');
const Escape = require('lodash/escape');

const s3SigV4Client = new AWS.S3( { signatureVersion: 'v4' } );

/**
 * Get the authenticated URL to access the S3 Object. This URL expires after 60 seconds.
 * @param s3ObjectKey - the S3 object key
 * @returns {string} the pre-signed S3 URL
 */
exports.getS3PreSignedUrl = function getS3PreSignedUrl(s3ObjectKey)
{
    const bucketName = process.env.S3_PERSISTENCE_BUCKET;

    return Escape( s3SigV4Client.getSignedUrl( 'getObject', { Bucket: bucketName, Key: s3ObjectKey, Expires: 60 } ) );
};

/**
 * Builds a directive to start the EventHandler.
 * @param token - a unique identifier to track the event handler
 * @param {number} timeout - the duration to wait before sending back the expiration
 * payload to the skill.
 * @param payload - the expiration json payload
 * @see {@link https://developer.amazon.com/docs/alexa-gadgets-toolkit/receive-custom-event-from-gadget.html#start}
 */
exports.buildStartEventHandler = function (token, timeout = 30000, payload)
{
    return {
        type: "CustomInterfaceController.StartEventHandler",
        token: token,
        expiration : { durationInMilliseconds: timeout, expirationPayload: payload }
    };
};

/**
 *
 * Builds a directive to stops the active event handler.
 * The event handler is identified by the cached token in the session attribute.
 * @param {string} handlerInput - the context from Alexa Service
 * @see {@link https://developer.amazon.com/docs/alexa-gadgets-toolkit/receive-custom-event-from-gadget.html#stop}
 */
exports.buildStopEventHandlerDirective = function (handlerInput)
{
    let token = handlerInput.attributesManager.getSessionAttributes().token || '';

    return { "type": "CustomInterfaceController.StopEventHandler", "token": token }
};

/**
 * Build a custom directive payload to the gadget with the specified endpointId
 * @param {string} endpointId - the gadget endpoint Id
 * @param {string} namespace - the namespace of the skill
 * @param {string} name - the name of the skill within the scope of this namespace
 * @param {object} payload - the payload data
 * @see {@link https://developer.amazon.com/docs/alexa-gadgets-toolkit/send-gadget-custom-directive-from-skill.html#respond}
 */
exports.build = function (endpointId, namespace, name, payload)
{
    // Construct the custom directive that needs to be sent
    // Gadget should declare the capabilities in the discovery response to
    // receive the directives under the following namespace.
    return {
        type: 'CustomInterfaceController.SendDirective',
        header: {
            name: name,
            namespace: namespace
        },
        endpoint: {
            endpointId: endpointId
        },
        payload
    };
};

/**
 * A convenience routine to add the a key-value pair to the session attribute.
 * @param handlerInput - the context from Alexa Service
 * @param key - the key to be added
 * @param value - the value be added
 */
exports.putSessionAttribute = function(handlerInput, key, value)
{
    const attributesManager = handlerInput.attributesManager;
    let sessionAttributes = attributesManager.getSessionAttributes();
    sessionAttributes[key] = value;
    attributesManager.setSessionAttributes(sessionAttributes);
};


/**
 * To get a list of all the gadgets that meet these conditions,
 * Call the Endpoint Enumeration API with the apiEndpoint and apiAccessToken to
 * retrieve the list of all connected gadgets.
 *
 * @param {string} apiEndpoint - the Endpoint API url
 * @param {string} apiAccessToken  - the token from the session object in the Alexa request
 * @see {@link https://developer.amazon.com/docs/alexa-gadgets-toolkit/send-gadget-custom-directive-from-skill.html#call-endpoint-enumeration-api}
 */
exports.getConnectedEndpoints = function(apiEndpoint, apiAccessToken)
{
    // The preceding https:// need to be stripped off before making the call
    apiEndpoint = (apiEndpoint || '').replace('https://', '');

    return new Promise(((resolve, reject) => {

        const options = {
            host: apiEndpoint,
            path: '/v1/endpoints',
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + apiAccessToken
            }
        };

        const request = Https.request(options, (response) => {
            response.setEncoding('utf8');
            let returnData = '';
            response.on('data', (chunk) => {
                returnData += chunk;
            });

            response.on('end', () => {
                resolve(JSON.parse(returnData));
            });

            response.on('error', (error) => {
                reject(error);
            });
        });
        request.end();
    }));
};
