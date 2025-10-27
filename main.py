"""
Quick test script for ETABS Wrapper.

Run this to test the installation and connection to ETABS.
"""

from etabs_wrapper import ETABSClient
from etabs_wrapper import ETABSConnectionError


def main():
    """Test ETABS connection and basic functionality."""
    print("ETABS Wrapper - Quick Test")
    print("=" * 60)

    try:
        print("\nAttempting to connect to ETABS...")
        client = ETABSClient.from_running_instance()
        print("✓ Connection successful!")

        # Try to get model filename
        ret, filename = client.model.GetModelFilename()
        if ret == 0:
            print(f"✓ Current model: {filename}")
        else:
            print("✓ Connected, but no model file saved yet")

        print("\n" + "=" * 60)
        print("ETABS Wrapper is working correctly!")
        print("See examples/basic_usage.py for more examples.")
        print("=" * 60)

    except ETABSConnectionError as e:
        print(f"\n✗ Connection failed: {e}")
        print("\nPlease ensure:")
        print("  1. ETABS is running")
        print("  2. A model is open")
        print("\nThen try running this script again.")

    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
