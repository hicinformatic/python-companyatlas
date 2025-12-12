"""Command-line interface for python-companyatlas."""

import json
import sys

from .backends import search_companies


def main() -> int:
    """Main CLI entry point."""
    if len(sys.argv) < 3:
        print(
            "Usage: companyatlas search <fetch> <query> "
            "[--country-code CODE] [--backend NAME] [--raw]"
        )
        print("\nCommands:")
        print("  search <fetch> <query>  Search for companies")
        print("\nFetch types:")
        print("  data       Search company data by name")
        print("  documents  Get documents by identifier")
        print("  events     Get events by identifier")
        print("\nOptions:")
        print("  --country-code CODE  Filter by country code (e.g., FR)")
        print("  --backend NAME       Force a specific backend (e.g., entdatagouv)")
        print("  --raw                Return raw API response without normalization")
        return 1

    if sys.argv[1] != "search":
        print(f"Unknown command: {sys.argv[1]}")
        print("Available commands: search")
        return 1

    if len(sys.argv) < 4:
        print("Error: fetch type and query are required")
        print("Usage: companyatlas search <fetch> <query>")
        return 1

    fetch = sys.argv[2]
    if fetch not in ["data", "documents", "events"]:
        print(f"Error: Invalid fetch type '{fetch}'. Must be 'data', 'documents', or 'events'")
        return 1

    query = sys.argv[3]

    country_code = None
    backend = None
    raw = False

    i = 4
    while i < len(sys.argv):
        if sys.argv[i] == "--country-code" and i + 1 < len(sys.argv):
            country_code = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--backend" and i + 1 < len(sys.argv):
            backend = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--raw":
            raw = True
            i += 1
        else:
            print(f"Error: Unknown option: {sys.argv[i]}")
            return 1

    try:
        result = search_companies(
            query=query,
            country_code=country_code,
            backend=backend,
            fetch=fetch,
            raw=raw,
        )

        if result.get("error"):
            print(f"Error: {result['error']}", file=sys.stderr)
            if result.get("errors"):
                for err in result["errors"]:
                    print(f"  - {err}", file=sys.stderr)
            return 1

        if result.get("backend_used"):
            print(f"Backend: {result['backend_used']}")
            print(f"Total: {result.get('total', 0)}")
            print()

        results = result.get("results", [])
        if results:
            print(json.dumps(results, indent=2, ensure_ascii=False))
        else:
            print("No results found")
            return 1

        return 0

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

