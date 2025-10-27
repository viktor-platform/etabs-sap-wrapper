# ETABS/SAP2000 Wrapper

A Python wrapper for the CSI API (ETABS and SAP2000) that simplifies retrieving table results from structural analysis models.

## Features

- **Dual Application Support**: Works with both ETABS and SAP2000
- Easy connection to running application instances
- Simplified interface for retrieving analysis results as pandas DataFrames
- **Shared API**: Same methods work for both applications (ETABS and SAP2000 use identical COM interfaces)
- Type hints for better IDE support
- Clean, modern Python API

## Installation

### From GitLab (recommended)

```bash
pip install git+https://gitlab.viktor.ai/jmikec/etabs-wrapper.git
```

### For development

```bash
git clone https://gitlab.viktor.ai/jmikec/etabs-wrapper.git
cd etabs-wrapper
uv sync
```

## Requirements

- Python 3.10+
- ETABS installed on Windows
- comtypes, pandas, numpy

## Quick Start

### ETABS

```python
from etabs_wrapper import ETABSClient

# Connect to a running ETABS instance
client = ETABSClient.from_running_instance()

# Get frame element forces
df = client.results.tables.element_forces_frames(
    load_cases=["DEAD", "LIVE"],
    load_combinations=["COMB1"],
    group_name="ALL"
)
print(df)
```

### SAP2000

```python
from etabs_wrapper import SAPClient

# Connect to a running SAP2000 instance
client = SAPClient.from_running_instance()

# Get frame element forces (same API as ETABS!)
df = client.results.tables.element_forces_frames(
    load_cases=["DEAD", "LIVE"],
    load_combinations=["COMB1"],
    group_name="ALL"
)
print(df)
```

### Using Context Manager

```python
from etabs_wrapper import ETABSClient

with ETABSClient.from_running_instance() as client:
    # Get joint displacements
    displacements = client.results.tables.joint_displacements(
        load_cases=["DEAD"],
        group_name="Floor1"
    )
    print(displacements)
```

## Available Table Methods

The `client.results.tables` object provides the following methods:

### `get_table(table_key, group_name="")`
Generic method to retrieve any ETABS table by name.

```python
df = client.results.tables.get_table("Joint Displacements", group_name="Floor1")
```

### `element_forces_frames(load_cases=None, load_combinations=None, group_name="")`
Retrieve frame element forces (axial, shear, moment).

```python
df = client.results.tables.element_forces_frames(
    load_cases=["DEAD", "LIVE"],
    load_combinations=["COMB1", "COMB2"],
    group_name="Columns"
)
# Returns DataFrame with: Frame, OutputCase, P, V2, V3, T, M2, M3, ...
```

### `joint_displacements(load_cases=None, load_combinations=None, group_name="")`
Retrieve joint displacements (translations and rotations).

```python
df = client.results.tables.joint_displacements(
    load_cases=["DEAD"],
    load_combinations=["COMB1"]
)
# Returns DataFrame with: Joint, OutputCase, U1, U2, U3, R1, R2, R3
```

### `base_reactions(load_cases=None, load_combinations=None, group_name="")`
Retrieve base reactions (forces and moments).

```python
df = client.results.tables.base_reactions(load_combinations=["COMB1", "COMB2"])
# Returns DataFrame with: OutputCase, FX, FY, FZ, MX, MY, MZ
```

### `element_forces_beams(load_cases=None, load_combinations=None, group_name="")`
Retrieve beam element forces.

```python
df = client.results.tables.element_forces_beams(load_cases=["DEAD", "LIVE"])
```

## Advanced Usage

### Direct API Access

You can access the underlying ETABS COM object for methods not wrapped by this library:

```python
client = ETABSClient.from_running_instance()

# Direct access to ETABS API
ret = client.model.Analyze.RunAnalysis()

# Access to any ETABS API method
file_path = client.model.GetModelFilename()
print(f"Current model: {file_path}")
```

### Working with Results

All table methods return pandas DataFrames, so you can use standard pandas operations:

```python
# Get frame forces
forces = client.results.tables.element_forces_frames(load_cases=["DEAD"])

# Filter and analyze
max_moment = forces["M3"].max()
critical_frames = forces[forces["M3"] > 1000]

# Export to CSV
forces.to_csv("frame_forces.csv", index=False)

# Export to Excel
forces.to_excel("frame_forces.xlsx", index=False)
```

## Error Handling

```python
from etabs_wrapper import ETABSClient
from etabs_wrapper import ETABSConnectionError

try:
    client = ETABSClient.from_running_instance()
except ETABSConnectionError as e:
    print(f"Failed to connect to ETABS: {e}")
    # Handle error - maybe start a new instance?
```

## Development

### Running Tests

```bash
pytest tests/
```

### Linting and Formatting

```bash
ruff check src/
ruff format src/
```

## Project Structure

```
etabs-wrapper/
├── src/
│   └── etabs_wrapper/
│       ├── __init__.py              # Main exports (ETABSClient, SAPClient)
│       ├── client.py                # ETABSClient and SAPClient classes
│       ├── core/                    # Core functionality
│       │   ├── __init__.py
│       │   ├── base_client.py       # Base class (shared code)
│       │   └── connection.py        # COM connection (ETABS & SAP2000)
│       ├── results/                 # Results retrieval
│       │   ├── __init__.py
│       │   └── tables.py            # Table results (works for both apps)
│       ├── analysis/                # Analysis operations (future)
│       │   └── __init__.py
│       └── model/                   # Model manipulation (future)
│           └── __init__.py
├── examples/                        # Usage examples
│   ├── basic_usage.py              # ETABS examples
│   └── sap2000_usage.py            # SAP2000 examples
├── tests/                           # Test files
├── pyproject.toml                  # Package configuration
└── README.md                       # This file
```

## Application Support

### Why Both ETABS and SAP2000?

ETABS and SAP2000 share the **same COM API interface**. This means:
- All table names are identical
- All method signatures are the same
- Results have the same structure
- Code written for one works for the other!

The only difference is the connection - once connected, everything else is identical.

### Switching Between Applications

```python
# Same code works for both!
def get_frame_forces(client):
    return client.results.tables.element_forces_frames(
        load_cases=["DEAD"]
    )

# Use with ETABS
etabs = ETABSClient.from_running_instance()
forces = get_frame_forces(etabs)

# Use with SAP2000
sap = SAPClient.from_running_instance()
forces = get_frame_forces(sap)
```

## Future Enhancements

Future versions may include:
- Model manipulation methods
- Load case/combination management
- Section property access
- Material property access
- Export/import functionality
- Bridge design features (SAP2000-specific)

## License

[Add your license here]

## Contributing

Contributions welcome! Please open an issue or submit a merge request.

## Support

For issues or questions:
- Open an issue on GitLab: https://gitlab.viktor.ai/jmikec/etabs-wrapper/-/issues
- Check ETABS API documentation for available table names and methods

## Acknowledgments

Based on the CSI ETABS API and inspired by previous SAP2000/ETABS Python wrappers.
