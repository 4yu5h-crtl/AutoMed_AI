from backend.tools.data_inspector import analyze_dataset
from backend.logger import send_log

def data_inspector_node(state):
    send_log("data_inspector", "Data Inspector Running...")

    dataset_path = state["dataset_path"]
    send_log("data_inspector", f"Scanning dataset at: {dataset_path}")

    # Call tool
    stats = analyze_dataset(dataset_path)

    # Save to state
    state["dataset_stats"] = stats

    send_log("data_inspector", "Dataset Stats:")
    send_log("data_inspector", str(stats))
    send_log("data_inspector", "Finished.")

    return state
