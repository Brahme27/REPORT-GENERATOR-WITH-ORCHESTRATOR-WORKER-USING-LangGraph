import os 
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
llm=ChatGroq(model="llama-3.3-70b-versatile")
# llm.invoke("hii babe")


from typing import Annotated,List
import operator
from typing_extensions import Literal,TypedDict
from pydantic import BaseModel,Field
from langchain_core.messages import HumanMessage,SystemMessage


class Section(BaseModel):
    name:str=Field(description="Name for this section of the report")
    description:str=Field(description="Brief overview of the main topics and concept of the section")

class Sections(BaseModel):
    sections:List[Section]=Field(
        description="Sections of the report"
    )

planner=llm.with_structured_output(Sections)


## Creating the workers Dynamically in LangGraph
from langgraph.constants import Send
# Graph state
class State(TypedDict):
    topic:str    # Report topic
    sections:List[Section]   # List of report Sections
    completed_sections:Annotated[
        list,operator.add 
    ] # All workers write to this key in parallel
    final_report:str  # Final report 

class WorkerState(TypedDict):
    section:Section
    completed_sections:Annotated[list,operator.add]
    
# Nodes

def orchestrator(state:State):
    """Orchestrator that generated a plan for the report"""

    # generate Queries
    report_sections=planner.invoke(
        [
            SystemMessage(content="Generate a plan for the report"),
            HumanMessage(content=f"Here is the report topic: {state['topic']}"),
        ]
    )

    #print("Report Sections:",report_sections)

    return {"sections":report_sections.sections}
# LLM call 

def llm_call(state:WorkerState):
    """ Worker writes a section of the report"""

    # Generate the section
    section=llm.invoke(
        [
            SystemMessage(
                content="Write a report section following the provided name and description.Include no preamble for each section.Use markdown formatter"
            ),
            HumanMessage(
                content=f"Here is the section name: {state["section"].name} and description: {state["section"].description}"
            )
        ]
    )

    return {"completed_sections":[section.content]}
# To run every worker parallely
# Conditional edge function to create llm_call workers that each write a section of the report

def assign_workers(state:State):
    """Assign a worker to each section in the plan"""

    # Kick off section writing in parallel via send() api 
    return [Send("llm_call",{"section":s}) for s in state["sections"]]
# Creating Synthesizer
def synthesizer(state:State):
    """Synthesize full report from sections"""

    #List of comoleted sections
    completed_sections=state["completed_sections"]

    # Format completed section to str to use as context for final sections
    completed_report_sections="\n\n------\n\n".join(completed_sections)

    return {"final_report":completed_report_sections}

# Build workflow
from langgraph.graph import StateGraph,START,END
orchestrator_worker_builder=StateGraph(State)

## Add the nodes
orchestrator_worker_builder.add_node("orchestrator",orchestrator)
orchestrator_worker_builder.add_node("llm_call",llm_call)
orchestrator_worker_builder.add_node("synthesizer",synthesizer)

# Add edges to connect nodes
orchestrator_worker_builder.add_edge(START,"orchestrator")
orchestrator_worker_builder.add_conditional_edges(
    "orchestrator",assign_workers,["llm_call"]
)
orchestrator_worker_builder.add_edge("llm_call","synthesizer")
orchestrator_worker_builder.add_edge("synthesizer",END)


orchestrator_worker=orchestrator_worker_builder.compile()

# Displaying the image
from IPython.display import Image,display

#display(Image(orchestrator_worker.get_graph().draw_mermaid_png()))
state=orchestrator_worker.invoke({"topic":"Create a Report on Agentic AI RAGs"})

#from IPython.display import Markdown
print(state["final_report"])