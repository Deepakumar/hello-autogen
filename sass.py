
from autogen import AssistantAgent, GroupChatManager, UserProxyAgent, config_list_from_json
from autogen.agentchat import GroupChat

import autogen
import panel as pn
import json

config_list = [
    {
        "api_base": "http://localhost:1234/v1",
        "api_type": "open_ai",
        "api_key": "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",
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
    system_message="Marketing. You Adhere to an approved plan and develop a marketing strategy for your SaaS product."""
)

Sales = AssistantAgent(
    name="Sales",
    llm_config=llm_config,
    system_message="""
    Sales.You execute an approved plan and formulate a sales strategy for your SaaS solution.".
""",
)

Planner = AssistantAgent(
    name="Planner",
    system_message="""
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
    system_message="""Product.You Adhere to an approved plan and ensure the accurate implementation of specifications for the SaaS-based product.
""",)


critic = AssistantAgent(
    name="critic",
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

# admin.register_reply(
#     [autogen.Agent, None],
#     reply_func=print_messages, 
#     config={"callback": None},
# )

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
    return f'<span style="background-color: yellow;">{value}</span>'

def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    admin.initiate_chat(
    manager,
    message=contents
)
    

template = pn.template.BootstrapTemplate(title='AutoGen Chatbot')

chat_interface = pn.chat.ChatInterface(callback=callback, user="Admin", renderers=[custom_renderer])

template.main.append(chat_interface)

chat_interface.send("Send a message!", user="System", respond=False)

template.servable();

