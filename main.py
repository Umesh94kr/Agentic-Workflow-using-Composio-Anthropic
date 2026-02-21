from agent import perform_task 
from reward import call_reward_agent 
from authorising_tools import connect_tool

if __name__ == "__main__":
    user_id = input("Enter your user_id : ")
    tool = input("Enter tool you want to use 'gmail', 'notion' (check cpmposio for this) : ")
    ## check whether tool is authorised if not click on link to authorise the tool 
    connect_tool(tool, user_id)

    ## ask user about task which he want to be performed 
    task = input("Enter the task which you want agent to perform : ")
    ## call agent to do the task 
    tool_logs = perform_task(task, user_id, tool)
    ## now we have the logs let use our reward agent to check whether task is performed or not
    output = call_reward_agent(task, tool_logs)
    print("="*60)
    print(f"Task successfully performed by agent? - {output['success']}")
    print(f"Reasoning : {output['reasoning']}")
