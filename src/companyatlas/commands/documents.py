from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Any

from qualitybase.commands.base import Command

from companyatlas.helpers import get_company_documents

if TYPE_CHECKING:
    from pathlib import Path


def _documents_command(args: list[str]) -> bool:
    output_format = "table"
    dir_path: str | Path | None = None
    json_path: str | Path | None = None
    query_string: str | None = None
    code: str | None = None
    first: bool = False
    raw: bool = False
    additional_args: dict[str, str | bool] = {}
    attribute_search: dict[str, str] = {}

    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--code" and i + 1 < len(args):
            code = args[i + 1]
            i += 2
        elif arg == "--attr":
            i += 1
            while i < len(args) and not args[i].startswith("--"):
                attr_arg = args[i]
                if "=" in attr_arg:
                    key, value = attr_arg.split("=", 1)
                    attribute_search[key] = value
                else:
                    print(f"Invalid attribute format: {attr_arg}. Expected format: key=value", file=sys.stderr)
                    return False
                i += 1
        elif arg == "--format" and i + 1 < len(args):
            output_format = args[i + 1]
            i += 2
        elif arg == "--dir" and i + 1 < len(args):
            dir_path = args[i + 1]
            i += 2
        elif arg == "--json" and i + 1 < len(args):
            json_path = args[i + 1]
            i += 2
        elif arg == "--filter" or arg == "--backend":
            query_string = args[i + 1]
            i += 2
        elif arg == "--first":
            first = True
            i += 1
        elif arg == "--raw":
            raw = True
            i += 1
        else:
            print(f"Unknown argument: {arg}", file=sys.stderr)
            return False

    if not code:
        print("Error: --code is required", file=sys.stderr)
        return False

    providers_args: dict[str, Any] = {
        "format": output_format,
        "json": json_path,
        "dir_path": dir_path,
        "query_string": query_string,
    }

    if attribute_search:
        providers_args["attribute_search"] = attribute_search

    if raw:
        additional_args["raw"] = True

    result = get_company_documents(code=code, first=first, additional_args=additional_args, **providers_args)

    print(result)
    return True


documents_command = Command(_documents_command, "Get company documents (use --code company_code)")

