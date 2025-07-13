from typing import Annotated
import operator

from typing_extensions import TypedDict
from langchain_core.runnables import RunnableConfig


# TODO: main state and subgraph state should not be coincided
class SubgraphState(TypedDict):
    idx: int
    section1: str
    subgraph_section2s: list[str]
    collects: Annotated[
        list, operator.add
    ]

class MainState(TypedDict):
    section1s: list[str]
    section2s: list[str]
    collects: Annotated[
        list, operator.add
    ]
    summation: int


runnable_config = RunnableConfig(max_concurrency=10)



from langgraph.graph import END, START, StateGraph
from langgraph.types import Send
import time
import random


def rod(subgraphstate: SubgraphState):
    print(subgraphstate["section1"])
    print("hi from rod")
    time.sleep(0)
    return 
def ocr(subgraphstate: SubgraphState):
    print(subgraphstate["section1"])
    print("hi from ocr")
    time.sleep(0)
def tsr(subgraphstate: SubgraphState):
    print(subgraphstate["section1"])
    print("hi from tsr")
    time.sleep(random.uniform(0.5, 1.5))
    return {
        "collects": [subgraphstate["idx"]]
    }
def dla(state: MainState): ...
# def rod2tsr(state: MainState): ...
def assign_workers(state: MainState):
    """
    Assign a worker to each section in the plan

    link: https://langchain-ai.github.io/langgraph/tutorials/workflows/?h=parallel#orchestrator-worker
    """
    # Kick off section writing in parallel via Send() API
    return [
        Send(
            "rod2tsr",
            {
                "idx": i,
                "section1": s1,
                "subgraph_section2s": state["section2s"],
            }
        ) 
        for i, (s1, s2) in enumerate(zip(state["section1s"], state["section2s"]))
    ]
def chunk(state: MainState):
    collects = state["collects"]
    return {
        "summation": sum(collects)
    }


class G:
    def __init__(self, task, save_dir):
        sub_graph = StateGraph(SubgraphState)
        sub_graph.add_sequence([rod, ocr, tsr])
        sub_graph.add_edge(START, "rod")
        rod2tsr = sub_graph.compile()

        main_graph = StateGraph(MainState)
        main_graph.add_node("dla", dla)
        main_graph.add_node("rod2tsr", rod2tsr)
        main_graph.add_node("chunk", chunk)
        main_graph.add_edge(START, "dla")
        main_graph.add_conditional_edges("dla", assign_workers, ["rod2tsr"])
        main_graph.add_edge("rod2tsr", "chunk")
        main_graph.add_edge("chunk", END)
        self.compiled_main_graph = main_graph.compile()

        self.save(save_dir)


    def save(self, save_dir):
        self.compiled_main_graph.get_graph(xray=True).draw_mermaid_png(output_file_path=f"{save_dir}/temp2.png")
        with open(f"{save_dir}/graph.mermaid", "w") as f:
            f.write(self.compiled_main_graph.get_graph(xray=True).draw_mermaid())

    def invoke(self, state):
        return self.compiled_main_graph.invoke(
            state,
            config=runnable_config
        )

if __name__ == "__main__":
    graph = G("task_name", "logs")
    module = ()
    state = graph.invoke({
        "module": module,
        "section1s": [f"section1a {i}" for i in range(30)],
        "section2s": [f"section2a {i}" for i in range(30)],
    })
    print(state["collects"])
    print(state["summation"])
