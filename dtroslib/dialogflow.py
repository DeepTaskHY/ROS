#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import uuid
from google.cloud import dialogflow_v2 as dialogflow


class DialogflowClient:
    __client: dialogflow.SessionsClient = None
    __project_id: str = None
    __session_id: str = None
    __key_path: str = None
    __language_code: str = None

    def __init__(self,
                 project_id: str,
                 key_path: str,
                 session_id: str = None,
                 language_code: str = 'ko'):

        self.__project_id = project_id
        self.__session_id = session_id
        self.__key_path = key_path
        self.__language_code = language_code
        self.authorize_credentials()

    @property
    def project_id(self) -> str:
        return self.__project_id

    @property
    def session_id(self) -> str:
        if not self.__session_id:
            self.__session_id = str(uuid.uuid4())

        return self.__session_id

    @property
    def client(self) -> dialogflow.SessionsClient:
        if self.__client is None:
            self.__client = dialogflow.SessionsClient()

        return self.__client

    @property
    def session(self) -> str:
        return self.client.session_path(self.project_id, self.session_id)

    def authorize_credentials(self):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.__key_path

    @property
    def language_code(self) -> str:
        return self.__language_code

    def trigger_intent_event(self, event: str) -> dialogflow.types.DetectIntentResponse:
        event_input = dialogflow.types.EventInput(name=event, language_code=self.language_code)
        query_input = dialogflow.types.QueryInput(event=event_input)

        response = self.client.detect_intent(request={
            'session': self.session,
            'query_input': query_input
        })

        return response

    def detect_intent_text(self, text: str) -> dialogflow.types.DetectIntentResponse:
        text_input = dialogflow.types.TextInput(text=text, language_code=self.language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)

        response = self.client.detect_intent(request={
            'session': self.session,
            'query_input': query_input
        })

        return response
