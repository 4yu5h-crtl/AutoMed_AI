from langgraph.graph import StateGraph
from backend.pipeline_state import PipelineState

# Import agents
from backend.agents.data_inspector_agent import data_inspector_node
from backend.agents.augmentation_agent import augmentation_agent_node
from backend.agents.model_selection_agent import model_selection_agent_node
from backend.agents.model_trainer_agent import model_trainer_node


def build_pipeline():
    # Initialize graph with our state type
    graph = StateGraph(PipelineState)

    # Add agent nodes
    graph.add_node("data_inspector", data_inspector_node)
    graph.add_node("augmentation", augmentation_agent_node)
    graph.add_node("model_selector", model_selection_agent_node)
    graph.add_node("trainer", model_trainer_node)

    # Connect nodes in order
    graph.add_edge("data_inspector", "augmentation")
    graph.add_edge("augmentation", "model_selector")
    graph.add_edge("model_selector", "trainer")

    # Entry point
    graph.set_entry_point("data_inspector")

    # End at model trainer
    graph.set_finish_point("trainer")

    # Compile graph into runnable pipeline
    return graph.compile()


test_pipeline = build_pipeline()
