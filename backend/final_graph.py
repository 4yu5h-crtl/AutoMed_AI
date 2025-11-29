from backend.pipeline_graph import test_pipeline
from backend.pipeline_state import PipelineState

# Set dataset path
state = PipelineState(dataset_path=r"d:\Projects\My_Personal_Projects\8_MumbaiHacks\Prototype\data")

# Run ONLY Agent 1 + Agent 2
final_state = test_pipeline.invoke(state)

print("\n=== FINAL STATE ===")
print(final_state)
