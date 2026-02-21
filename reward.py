# For making a reward function I want to compare whether task given to agent is performed or not 

# Things form logs that I'll need 
# Tool calls and messages (with sequence)

# I'll make a langgraph agent as a reward function
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List, Annotated 
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate 

# defining llm used for evaluation 'llama3.2' must be running on your laptop
llm = ChatOllama(
    model='llama3.2',
    verbose=True,
    temperature=0.2
)

# Defining state
class RewardState(TypedDict):
    task: str 
    tool_calls_and_resps: List[str]
    success: str
    reasoning: str

# structured output validation from LLM 
class StructuredOutput(BaseModel):
    "What LLM should generate when asked to evaluate a task performed by agent."
    success: Annotated[str, Field(description="If task is successfully completed by agent then return 'Yes' else 'No'")]
    reasoning: Annotated[List[str], Field(description="Give the reasoning for whether agent completed the task or not.")]

# defining the node 

def llm_usage(state: RewardState) -> RewardState:
    template = """ 
                Given a task : {task} which is performed by an agent with logs contains tool calls : {tool_calls_and_resps}. You need to verfiy whether the assigned task is successfully completed by agent or not.
               """
    
    prompt = PromptTemplate(
        template=template,
        input_variables=['task', 'tool_calls_and_resps']
    )

    llm_outline = llm.with_structured_output(StructuredOutput)
    chain = prompt | llm_outline 
    
    response = chain.invoke({'task' : state['task'], 'tool_calls_and_resps' : state['tool_calls_and_resps']})
    state['success'] = response.success
    state['reasoning'] = response.reasoning
    return state

def make_graph():
    # making a graph 
    graph = StateGraph(RewardState)

    graph.add_node('llm_usage', llm_usage)
    
    # add edges 
    graph.add_edge(START, 'llm_usage')
    graph.add_edge('llm_usage', END)
    return graph


############################################################
############################################################
# FUNCTION TO USE REWARD AGENT
def call_reward_agent(task, tool_logs):
    # compile graph 
    graph = make_graph()
    reward_agent = graph.compile()
    inputs = {'task' : task, 'tool_calls_and_resps' : tool_logs}
    # invoke the agent 
    output = reward_agent.invoke(inputs)
    return output

if __name__ == "__main__":
    task = input("Input the task : ")
    tool_logs = input("Dummy Logs of tool for task : ")
    output = call_reward_agent(task, [tool_logs])
    print("="*60)
    print(f"Task successfully performed by agent? - {output['success']}")
    print(f"Reasoning : {output['reasoning']}")

### DUMMY DATA FOR TESTING THIS FEATURE 
# TASK : I want to send an email to my collegue lakshay.bhadana@auxo.com to congratuale him regarding AI engineer role at Auxo.

# TOOL LOGS : Tool call : 'SEND_EMAIL', to : lakshay.bhadana@auxo.com, subject : Congratualing on role for AI engineer, body: Hi Lakshay I hope you are good, Want to congratulate you for AI engineer role. Wish you more success in future. Regards, Umesh