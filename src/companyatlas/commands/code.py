"""Company search by reference command."""

from __future__ import annotations

from providerkit.commands.provider import _PROVIDER_COMMAND_CONFIG
from qualitybase.commands import parse_args_from_config
from qualitybase.commands.base import Command
from qualitybase.services.utils import print_header, print_separator

from companyatlas.helpers import search_company_by_reference

_ARG_CONFIG = {
    **_PROVIDER_COMMAND_CONFIG,
    'code': {'type': str, 'default': ''},
}


def _code_command(args: list[str]) -> bool:
    parsed = parse_args_from_config(args, _ARG_CONFIG, prog='code')
    kwargs = {}
    kwargs['attribute_search'] = parsed.get('attr', {}).get('kwargs', {})
    output_format = parsed.get('format', 'terminal')
    raw = parsed.get('raw', False)
    code = parsed.pop('code')
    first = parsed.pop('first', False)
    pvs_companies = search_company_by_reference(code, first=first, **kwargs)
    for pv in pvs_companies:
        print_separator()
        print_header(pv['provider'].name)
        print_separator()
        print(pv['provider'].response('search_company_by_reference', raw, output_format))
    return True


code_command = Command(_code_command, "Search company by reference (use --code company_code)")

