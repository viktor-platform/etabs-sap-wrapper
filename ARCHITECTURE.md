# Package Architecture

## Overview

The ETABS Wrapper is organized into a modular structure with separate subpackages for different categories of operations. This design allows for easy extension and maintains clear separation of concerns.

## Directory Structure

```
src/etabs_wrapper/
├── __init__.py                    # Main package exports
├── client.py                      # Main ETABSClient class
├── core/                          # Core functionality
│   ├── __init__.py
│   └── connection.py              # COM connection management
├── results/                       # Results retrieval operations
│   ├── __init__.py
│   └── tables.py                  # Table results (forces, displacements, etc.)
├── analysis/                      # Analysis operations (future)
│   └── __init__.py
└── model/                         # Model manipulation (future)
    └── __init__.py
```

## Module Descriptions

### `core/` - Core Functionality

**Purpose**: Fundamental operations for connecting to ETABS and managing the COM interface.

**Current Modules**:
- `connection.py`: Handles COM object creation and connection management
  - `connect_to_instance()`: Connect to running ETABS
  - `start_new_instance()`: Start new ETABS instance
  - `ETABSConnectionError`: Custom exception for connection failures

**Future Additions**:
- Configuration management
- Logging utilities
- Error handling utilities

### `results/` - Results Retrieval

**Purpose**: Retrieve analysis results from ETABS models.

**Current Modules**:
- `tables.py`: Database table retrieval
  - `TableResults`: Class for retrieving ETABS database tables
  - Methods for specific tables (frames, joints, reactions, etc.)

**Future Additions**:
- `forces.py`: Specialized force retrieval and processing
- `displacements.py`: Displacement analysis and visualization
- `design.py`: Design check results
- `modal.py`: Modal analysis results

### `analysis/` - Analysis Operations (Placeholder)

**Purpose**: Run analysis and manage analysis settings.

**Future Functionality**:
- Run analysis
- Set analysis options
- Manage load cases
- Manage load combinations
- Modal analysis settings
- Response spectrum analysis
- Time history analysis

### `model/` - Model Manipulation (Placeholder)

**Purpose**: Create, modify, and manage ETABS models.

**Future Functionality**:
- File operations (open, save, new, close)
- Material management
- Section property definitions
- Frame/shell/solid element creation
- Group management
- Coordinate systems
- Joint/point management

## Client Architecture

### ETABSClient

The main entry point for users. Provides organized access to all functionality through properties:

```python
client = ETABSClient.from_running_instance()

# Access results operations
client.results.tables.element_forces_frames(...)

# Access model operations (future)
client.model.materials.add_concrete(...)

# Access analysis operations (future)
client.analysis.run()
```

### Property-Based Organization

The client uses properties to provide clean, hierarchical access:

```python
@property
def results(self) -> ResultsManager:
    """Access results operations."""
    return ResultsManager(self._tables)
```

This design:
- Groups related operations logically
- Provides clear IDE autocomplete
- Allows lazy initialization if needed
- Maintains clear API boundaries

## Usage Patterns

### Basic Usage

```python
from etabs_wrapper import ETABSClient

# Connect to ETABS
client = ETABSClient.from_running_instance()

# Retrieve results
df = client.results.tables.element_forces_frames(cases=["DEAD"])
```

### Hierarchical Access

The package uses a hierarchical structure:

```
ETABSClient
├── .results                      # Results operations
│   └── .tables                   # Table retrieval
│       ├── .element_forces_frames()
│       ├── .joint_displacements()
│       └── .base_reactions()
├── .analysis (future)            # Analysis operations
│   ├── .run()
│   └── .load_cases
└── .model (future)               # Model operations
    ├── .materials
    └── .sections
```

### Direct API Access

For operations not yet wrapped, users can access the raw COM object:

```python
# Use wrapped API when available
df = client.results.tables.element_forces_frames(cases=["DEAD"])

# Fall back to direct API when needed
ret = client.model.Analyze.RunAnalysis()
```

## Extension Guidelines

### Adding New Subpackages

1. Create the subpackage directory in `src/etabs_wrapper/`
2. Add `__init__.py` with exports
3. Create module files for related functionality
4. Add manager class in `client.py` if needed
5. Add property to `ETABSClient` for access

### Adding New Modules to Existing Subpackages

1. Create the new module file
2. Update subpackage `__init__.py` to export new classes/functions
3. Update manager class if needed
4. Add tests
5. Update documentation

### Example: Adding Modal Analysis

```python
# 1. Create src/etabs_wrapper/results/modal.py
class ModalResults:
    def get_modes(self): ...
    def get_participation_factors(self): ...

# 2. Update src/etabs_wrapper/results/__init__.py
from etabs_wrapper.results.modal import ModalResults
__all__ = ["TableResults", "ModalResults"]

# 3. Update client.py ResultsManager
class ResultsManager:
    def __init__(self, tables, modal):
        self._tables = tables
        self._modal = modal

    @property
    def modal(self) -> ModalResults:
        return self._modal

# 4. Update ETABSClient.__init__
self._modal = ModalResults(sap_model)

# 5. Usage
client.results.modal.get_modes()
```

## Design Principles

1. **Separation of Concerns**: Each subpackage handles a specific domain
2. **Progressive Disclosure**: Simple tasks are simple, complex tasks are possible
3. **Consistent API**: All similar operations follow the same patterns
4. **Type Safety**: Full type hints for IDE support
5. **Extensibility**: Easy to add new functionality without breaking existing code
6. **Backward Compatibility**: Direct COM access always available

## Dependencies

- **comtypes**: COM interface for ETABS
- **pandas**: DataFrame return types for table data
- **numpy**: Array operations for table processing

## Testing Strategy

Each subpackage should have corresponding test files:

```
tests/
├── test_core_connection.py
├── test_results_tables.py
├── test_analysis.py
└── test_model.py
```

## Future Considerations

### Async Support

For long-running operations (analysis, file loading), consider adding async variants:

```python
async with ETABSClient.from_running_instance_async() as client:
    await client.analysis.run_async()
```

### Caching

Results could be cached to avoid repeated API calls:

```python
@cached_property
def materials(self):
    return self._fetch_materials()
```

### Event Handling

Monitor ETABS events for reactive programming:

```python
client.events.on_analysis_complete(callback)
```
