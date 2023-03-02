import requests
import json
import openai
import os


class ChatGPTAccessInterface:
    def __init__(self, token, model="gpt-3.5-turbo"):
        self.token = token
        self.model = model

    def listModels(self):
        """
        Lists the currently available models,
        and provides basic information about each one such as the owner and availability.
        :return:
        """
        # text-davinci-002, gpt-3.5-turbo
        # openai.organization = "org-TWT930pSUibKs4ZObBUDUSgr"
        openai.api_key = self.token
        models = openai.Model.list()
        for each in models["data"]:
            print("{}, ".format(each["id"]), end="")

    ##### 非流式返回
    def __requestText(self, model_engine, prompt):
        response = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=2048,
            # n=1,
            # stop=None,
            # temperature=0.5,
        )

        # gain ChatGPT responce
        str_retcont = response.choices[0].text
        return str_retcont

    def __requestGPT(self, model_engine, prompt):
        response = openai.ChatCompletion.create(
            model=model_engine,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2048,
            n=1,
            stream=False,
        )

        # print(completion)
        str_retcont = ""
        for each_content in response.choices:
            # print(each_content)
            str_retcont += each_content["message"]["content"] + "\n"
            # print(str_retcont)
        return str_retcont

    def request(self, prompt: str) -> str:
        # set API Key
        openai.api_key = self.token

        str_retcont = ""
        if "text" in self.model:
            str_retcont = self.__requestText(self.model, prompt)
        elif "gpt" in self.model:
            str_retcont = self.__requestGPT(self.model, prompt)
        else:
            raise Exception("Error: Unsupported Models.")

        return str_retcont

    ##### 流式返回
    def __requestTextStream(self, model_engine, prompt):
        # send a Completion request to count to 100
        response = openai.Completion.create(
            model=model_engine,
            prompt=prompt,
            max_tokens=2048,
            stream=True,  # this time, we set stream=True
        )

        # create variables to collect the stream of events
        collected_events = []
        completion_text = ''
        # iterate through the stream of events
        for event in response:
            collected_events.append(event)  # save the event response
            event_text = event['choices'][0]['text']  # extract the text
            completion_text += event_text  # append the text
            print(event_text, end="")

        # print the time delay and text received
        print("Full text received: {}".format(completion_text))

    def __requestGPTStream(self, model_engine, prompt):
        response = openai.ChatCompletion.create(
            model=model_engine,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2048,
            stream=True,
        )

        # create variables to collect the stream of events
        collected_events = []
        completion_text = ''
        # iterate through the stream of events
        for event in response:
            collected_events.append(event)  # save the event response
            try:
                event_text = event['choices'][0]['delta']['content']  # extract the text
            except Exception as e:
                event_text = ""
            completion_text += event_text  # append the text
            print(event_text, end="")

        # print the time delay and text received
        print("\nFull text received: {}".format(completion_text))

    def requestStream(self, prompt: str):
        # set API Key
        openai.api_key = self.token

        if "text" in self.model:
            self.__requestTextStream(self.model, prompt)
        elif "gpt" in self.model:
            self.__requestGPTStream(self.model, prompt)
        else:
            raise Exception("Error: Unsupported Models.")
