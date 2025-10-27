# Quick Start Guide

## Installation (30 seconds)

```bash
# Install from GitLab
pip install git+https://gitlab.viktor.ai/jmikec/etabs-wrapper.git

# Or with uv
uv pip install git+https://gitlab.viktor.ai/jmikec/etabs-wrapper.git
```

## Basic Usage (1 minute)

### 1. Open ETABS with a model

Make sure ETABS is running and a model is open.

### 2. Run this code

```python
from etabs_wrapper import ETABSClient

# Connect to ETABS
client = ETABSClient.from_running_instance()

# Get frame forces
forces = client.results.tables.element_forces_frames(
    load_cases=["DEAD"],
    load_combinations=[]
)

# Display results
print(forces.head())

# Export to CSV
forces.to_csv("frame_forces.csv", index=False)
```

## Common Operations

### Get Joint Displacements

```python
displacements = client.results.tables.joint_displacements(
    load_cases=["DEAD", "LIVE"],
    load_combinations=[],
    group_name="ALL"
)
```

### Get Base Reactions

```python
reactions = client.results.tables.base_reactions(
    load_combinations=["COMB1", "COMB2"]
)
```

### Get Any Table

```python
# Use the generic method for any ETABS table
df = client.results.tables.get_table(
    "Story Forces",
    group_name="ALL"
)
```

### Direct API Access

```python
# Access raw ETABS API for anything not wrapped
ret = client.model.Analyze.RunAnalysis()
ret, filename = client.model.GetModelFilename()
```

## Package Structure

The package is organized into logical submodules:

```python
from etabs_wrapper import ETABSClient

client = ETABSClient.from_running_instance()

# Results operations
client.results.tables.element_forces_frames(...)
client.results.tables.joint_displacements(...)
client.results.tables.base_reactions(...)

# Direct API access (for anything not wrapped)
client.model.Analyze.RunAnalysis()

# Future: Analysis operations
# client.analysis.run()
# client.analysis.load_cases.add(...)

# Future: Model operations
# client.model.materials.add_concrete(...)
# client.model.sections.add_ibeam(...)
```

## Working with Results

All table methods return pandas DataFrames:

```python
# Get results
forces = client.results.tables.element_forces_frames(cases=["DEAD"])

# Pandas operations
max_moment = forces["M3"].max()
critical_elements = forces[forces["M3"] > 1000]

# Export
forces.to_csv("forces.csv")
forces.to_excel("forces.xlsx")

# Plotting
import matplotlib.pyplot as plt
forces["M3"].hist()
plt.show()
```

## Error Handling

```python
from etabs_wrapper import ETABSClient, ETABSConnectionError

try:
    client = ETABSClient.from_running_instance()
    forces = client.results.tables.element_forces_frames(load_cases=["DEAD"])
except ETABSConnectionError:
    print("ETABS is not running or no model is open")
except RuntimeError as e:
    print(f"Failed to retrieve table: {e}")
```

## Full Example

```python
"""Complete example: Extract and analyze frame forces."""

from etabs_wrapper import ETABSClient, ETABSConnectionError

def main():
    try:
        # Connect
        print("Connecting to ETABS...")
        client = ETABSClient.from_running_instance()

        # Get model info
        ret, filename = client.model.GetModelFilename()
        print(f"Connected to: {filename}")

        # Get forces
        print("\nRetrieving frame forces...")
        forces = client.results.tables.element_forces_frames(
            load_cases=["DEAD", "LIVE"],
            load_combinations=["COMB1"]
        )

        # Analyze
        print(f"Retrieved {len(forces)} records")
        print(f"Max moment: {forces['M3'].max():.2f}")

        # Export
        forces.to_csv("frame_forces.csv", index=False)
        print("Results exported to frame_forces.csv")

    except ETABSConnectionError as e:
        print(f"Connection failed: {e}")
        print("Ensure ETABS is running with a model open")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
```

## What Tables Are Available?

The exact table names depend on your ETABS version. Common tables include:

- "Element Forces - Frames"
- "Element Forces - Beams"
- "Joint Displacements"
- "Base Reactions"
- "Story Forces"
- "Story Drifts"
- "Modal Participating Mass Ratios"
- "Modal Periods And Frequencies"

Use the generic `get_table()` method with any table name:

```python
df = client.results.tables.get_table("Story Drifts")
```

## Troubleshooting

**"Could not connect to running ETABS instance"**
- Ensure ETABS is running
- Ensure a model is open

**"Failed to retrieve table"**
- Model may not be analyzed - run analysis first
- Table name might be incorrect
- Load case name might not exist

**Package not found**
- Verify installation: `pip list | grep etabs-wrapper`
- Reinstall: `pip install --force-reinstall git+https://gitlab.viktor.ai/jmikec/etabs-wrapper.git`

## Next Steps

- **Full Documentation**: See [README.md](README.md)
- **Installation Details**: See [INSTALLATION.md](INSTALLATION.md)
- **Architecture**: See [ARCHITECTURE.md](ARCHITECTURE.md)
- **Examples**: Check [examples/basic_usage.py](examples/basic_usage.py)

## Support

- GitLab Issues: https://gitlab.viktor.ai/jmikec/etabs-wrapper/-/issues
- Repository: https://gitlab.viktor.ai/jmikec/etabs-wrapper
