"""
SAP2000 usage example.

This script demonstrates how to connect to SAP2000 and retrieve table results.
The API is identical to ETABS - all methods work the same way.

Prerequisites:
- SAP2000 must be running with a model open
- The model should have been analyzed (results available)
"""

from etabs_wrapper import SAP2000ConnectionError
from etabs_wrapper import SAPClient


def main():
    """Main example function."""
    try:
        # Connect to running SAP2000 instance
        print("Connecting to SAP2000...")
        client = SAPClient.from_running_instance()
        print(f"Connected successfully to {client.application_name}!")


        # Example 1: Get base reactions
        print("\n" + "=" * 60)
        print("Example 1: Base Reactions")
        print("=" * 60)

        reactions = client.results.tables.base_reactions(load_cases=["DEAD"], load_combinations=[])

        print(f"\nRetrieved {len(reactions)} base reaction records")
        print(reactions)

        # Example 4: Direct API access
        print("\n" + "=" * 60)
        print("Example 4: Direct API Access")
        print("=" * 60)

        # Get model filename using direct API call
        filename = client.model.GetModelFilename()
        print(f"Current model file: {filename}")

        # Example 5: Export results to CSV
        print("\n" + "=" * 60)
        print("Example 5: Export to CSV")
        print("=" * 60)

        output_file = "sap2000_base_reactions.csv"
        reactions.to_csv(output_file, index=False)
        print(f"Base reactions exported to: {output_file}")

        print("\n" + "=" * 60)
        print("Examples completed successfully!")
        print("=" * 60)

    except SAP2000ConnectionError as e:
        print(f"\nError: {e}")
        print("\nPlease ensure:")
        print("1. SAP2000 is running")
        print("2. A model is open")
        print("3. The model has been analyzed (run analysis)")

    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
