import autogen

config_list = [
    {
        "api_type": "open_ai",
        "api_base": "http://localhost:1234/v1",
        "api_key": "NULL"
    }
]

llm_config = {
    "request_timeout": 600,
    "seed": 42,
    "config_list": config_list,
    "temperature": 0
}

assistant = autogen.AssistantAgent(
 name="assistant",
 system_message="You are a code specializing in Python.",
 llm_config=llm_config
)

user_proxy = autogen.UserProxyAgent(
 name="user_proxy",
 human_input_mode="NEVER",
 max_consecutive_auto_reply=10,
 is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
 code_execution_config={"work_dir": "web"},
 llm_config=llm_config,
 system_message="""Replay TERMINATE if the task has been solved at full satisfaction. Otherwise, replay CONTINUE, 
 or the reason why the task is not solved yet."""
)

task = """Write a python method to print numbers 50 to 100"""

user_proxy.initiate_chat(assistant, message=task)