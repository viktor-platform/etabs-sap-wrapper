"""
Basic usage example for ETABS Wrapper.

This script demonstrates how to connect to ETABS and retrieve table results.

Prerequisites:
- ETABS must be running with a model open
- The model should have been analyzed (results available)
"""

from etabs_wrapper import ETABSClient
from etabs_wrapper import ETABSConnectionError


def main():
    """Main example function."""
    try:
        # Connect to running ETABS instance
        print("Connecting to ETABS...")
        client = ETABSClient.from_running_instance()
        print("Connected successfully!")

        # Example 1: Get frame element forces
        print("\n" + "=" * 60)
        print("Example 1: Frame Element Forces")
        print("=" * 60)

        frame_forces = client.results.tables.element_forces_frames(
            load_cases=["DEAD"],  # Specify load cases
            load_combinations=[],  # No combinations
            group_name="",  # All groups
        )

        print(f"\nRetrieved {len(frame_forces)} frame force records")
        print("\nFirst 5 rows:")
        print(frame_forces.head())

        # Example 2: Get joint displacements
        print("\n" + "=" * 60)
        print("Example 2: Joint Displacements")
        print("=" * 60)

        displacements = client.results.tables.joint_displacements(
            load_cases=["DEAD"],
            load_combinations=[],
            group_name="",
        )

        print(f"\nRetrieved {len(displacements)} displacement records")
        print("\nFirst 5 rows:")
        print(displacements.head())

        # Example 3: Get base reactions
        print("\n" + "=" * 60)
        print("Example 3: Base Reactions")
        print("=" * 60)

        reactions = client.results.tables.base_reactions(load_cases=["DEAD"], load_combinations=[])

        print(f"\nRetrieved {len(reactions)} base reaction records")
        print(reactions)

        # Example 4: Direct API access
        print("\n" + "=" * 60)
        print("Example 4: Direct API Access")
        print("=" * 60)

        # Get model filename using direct API call
        ret, filename = client.model.GetModelFilename()
        print(f"Current model file: {filename}")

        # Example 5: Export results to CSV
        print("\n" + "=" * 60)
        print("Example 5: Export to CSV")
        print("=" * 60)

        output_file = "frame_forces.csv"
        frame_forces.to_csv(output_file, index=False)
        print(f"Frame forces exported to: {output_file}")

        print("\n" + "=" * 60)
        print("Examples completed successfully!")
        print("=" * 60)

    except ETABSConnectionError as e:
        print(f"\nError: {e}")
        print("\nPlease ensure:")
        print("1. ETABS is running")
        print("2. A model is open")
        print("3. The model has been analyzed (run analysis)")

    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
