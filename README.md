# robocalls
A flask app to auto-dial congress.  It will present a webpage with a form requiring a name, an email address, a telephone number, and a zipcode.  When the form is submitted, it will save the name and email to an Action Network account, look up any congressional representatives by zip code, dial their contact numbers using Twilio and play a predefined twilio flow for them.

This is built to be deployed on Heroku, but could probably be modified to fit any cloud platform.  It requires Redis, an ActionNetwork account, a ReCaptcha account and a Twilio account with a flow defined for the call.  It expects to find these environment variables at a minimum:

    SECRET_KEY: an encryption key
    ACTION_NETWORK_KEY:  Api key for ActionNetwork
    TWILIO_ACCOUNT_SID, TWILIO SECRET: credentials for Twilio
    TWILIO_FLOW_SID: The id of the flow used in the call
    TWILIO_NUMBER:  The phone number that the calls are made from, purchased from twilio
    PHONE_RECIPIENT_OVERRIDE:  If this is defined, then calls will be made to this number 
        instead of to congress reps -- used for debugging the twilio flow.
    RQ_REDIS_URL: The url of the redis service
    RECAPTCHA_PUBLIC_KEY, RECAPTCHA_PRIVATE_KEY: Recaptcha credentials
