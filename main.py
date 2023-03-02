
from ChatGPTAccessInterface import ChatGPTAccessInterface
from secret_config import *

def main():
    # "gpt-3.5-turbo", "text-davinci-002"
    chat = ChatGPTAccessInterface(TOKEN, "gpt-3.5-turbo")
    # chat.listModels()
    # print(chat.request("请用中文给我介绍一些电影"))
    chat.requestStream("请用中文给我介绍一些电影")

if __name__ == '__main__':
    main()