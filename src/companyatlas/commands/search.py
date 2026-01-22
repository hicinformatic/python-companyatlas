"""Company search command."""

from __future__ import annotations

from providerkit.commands.provider import _PROVIDER_COMMAND_CONFIG
from qualitybase.commands import parse_args_from_config
from qualitybase.commands.base import Command
from qualitybase.services.utils import print_header, print_separator

from companyatlas.helpers import search_company

_ARG_CONFIG = {
    **_PROVIDER_COMMAND_CONFIG,
    'query': {'type': str, 'default': ''},
}


def _search_command(args: list[str]) -> bool:
    parsed = parse_args_from_config(args, _ARG_CONFIG, prog='search')
    kwargs = {}
    kwargs['attribute_search'] = parsed.get('attr', {}).get('kwargs', {})
    output_format = parsed.get('format', 'terminal')
    raw = parsed.get('raw', False)
    query = parsed.pop('query')
    first = parsed.pop('first', False)
    pvs_companies = search_company(query, first=first, **kwargs)
    for pv in pvs_companies:
        name = pv['provider'].name
        time = pv['response_time']
        print_separator()
        print_header(f"{name} - {time}s")
        print_separator()
        print(pv['provider'].response('search_company', raw, output_format))
    return True


search_command = Command(_search_command, "Search companies (use --query query_string)")

