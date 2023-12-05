
from autogen import AssistantAgent, GroupChatManager, UserProxyAgent, config_list_from_json
from autogen.agentchat import GroupChat

import autogen
import panel as pn
import json
import datetime

config_list = [
    {
        "api_base": "http://localhost:1234/v1",
        "api_type": "open_ai",
        "api_key": "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"
    }
]

config_list = config_list_from_json(
    env_or_file="OAI_CONFIG_LIST.json",
    file_location=".",
)

llm_config = {"config_list": config_list, "seed": 42, "request_timeout": 600,
              "temperature": 0,}

admin = UserProxyAgent(
    name="admin",
    human_input_mode="ALWAYS",
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
                      Otherwise, reply CONTINUE, or the reason why the task is not solved yet.""",
    llm_config=llm_config,
    code_execution_config=False,
)

Marketing = AssistantAgent(
    name="Marketing",
    llm_config=llm_config,
    max_consecutive_auto_reply=3,
    system_message="Marketing. You Adhere to an approved plan and develop a marketing strategy for given context"""
)

Sales = AssistantAgent(
    name="Sales",
    llm_config=llm_config,
    max_consecutive_auto_reply=3,
    system_message="""
    Sales.You execute an approved plan and formulate a sales strategy for your given context.".
""",
)

Planner = AssistantAgent(
    name="Planner",
    max_consecutive_auto_reply=3,
    system_message=""",
                    Planner.Propose a plan and iteratively refine it based on feedback from the admin and 
                    critic until it obtains admin approval. 
                    Begin by providing a clear explanation of the plan, 
                    specifying which steps are carried out by the Marketing, Sales,critic, and Product teams.
                    """,
    llm_config=llm_config,
)

Product = AssistantAgent(
    name="Product",
    llm_config=llm_config,
    max_consecutive_auto_reply=3,
    system_message="""Product.You Adhere to an approved plan and ensure the accurate implementation of specifications for given context.
""",)


critic = AssistantAgent(
    name="critic",
    max_consecutive_auto_reply=3,
    system_message="""critic.Thoroughly review the plan and claims from other agents and offer feedback. Additionally,
    ensure the plan includes verifiable information, such as source URLs.""",
    llm_config=llm_config,
)
groupchat = GroupChat(
    agents=[Sales,Marketing,Product,Planner,critic],
    messages=[],
    max_round=500,
)
manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)
avatar = {admin.name:"👨‍💼", Marketing.name:"👩‍💻", Sales.name:"👩‍🔬", Planner.name:"🗓", Product.name:"🛠", critic.name:'📝'}

def print_messages(recipient, messages, sender, config):
    try:
        _avatar = avatar.get(messages[-1].get('name', 'admin'))
        _user = messages[-1].get('name', 'Assistant')
        _message = messages[-1].get('content','')
        if _user != 'admin':
            chat_interface.send(_message, _user, avatar=_avatar, respond=False)
        return False, None
    except Exception as e:
        print("An error occurred:", e)

admin.register_reply(
    [autogen.Agent, None],
    reply_func=print_messages, 
    config={"callback": None},
)

Marketing.register_reply(
    [autogen.Agent, None],
    reply_func=print_messages, 
    config={"callback": None},
)

Sales.register_reply(
    [autogen.Agent, None],
    reply_func=print_messages, 
    config={"callback": None},
)

Planner.register_reply(
    [autogen.Agent, None],
    reply_func=print_messages, 
    config={"callback": None},
)

Product.register_reply(
    [autogen.Agent, None],
    reply_func=print_messages, 
    config={"callback": None},
)

critic.register_reply(
    [autogen.Agent, None],
    reply_func=print_messages, 
    config={"callback": None},
)

pn.extension(design="material")

def custom_renderer(value):
    return value

def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    admin.initiate_chat(
    manager,
    message=contents
)

def clear_callback(event):
    groupchat.clear()
    print('Clearning Agent Chat History')  

template = pn.template.BootstrapTemplate(title='AutoGen Chatbot')

chat_interface = pn.chat.ChatInterface(callback=callback, user="Admin", renderers=[custom_renderer])
chat_interface.css = [
    {
        "selector": ".bk.chat-entry",
        "props": [
            ("font-size", "24px"),  
        ],
    },
    {
        "selector": ".bk.chat-avatar img",
        "props": [
            ("width", "50px"),  
            ("height", "50px"),  
        ],
    },
    {
        "selector": ".bk-panel-models-markup-HTML",
        "props": [
            ("font-size", "20px"),  
        ],
    }
]

clear_button = pn.widgets.Button(name='Clear Session')
clear_button.on_click(clear_callback)

template.main.append(pn.Row(clear_button, chat_interface))


current_time = datetime.datetime.now()
current_hour = current_time.hour

if current_hour < 12:
    chat_interface.send("Good morning! Admin..", user="System", respond=False)
else:
    chat_interface.send("Good evening! Admin..", user="System", respond=False)

template.servable();

