"""Company documents command."""

from __future__ import annotations

from providerkit.commands.provider import _PROVIDER_COMMAND_CONFIG
from qualitybase.commands import parse_args_from_config
from qualitybase.commands.base import Command
from qualitybase.services.utils import print_header, print_separator

from companyatlas.helpers import get_company_documents

_ARG_CONFIG = {
    **_PROVIDER_COMMAND_CONFIG,
    'code': {'type': str, 'default': ''},
}


def _documents_command(args: list[str]) -> bool:
    parsed = parse_args_from_config(args, _ARG_CONFIG, prog='documents')
    kwargs = {}
    kwargs['attribute_search'] = parsed.get('attr', {}).get('kwargs', {})
    output_format = parsed.get('format', 'terminal')
    raw = parsed.get('raw', False)
    code = parsed.pop('code')
    first = parsed.pop('first', False)
    pvs_documents = get_company_documents(code, first=first, **kwargs)
    for pv in pvs_documents:
        name = pv['provider'].name
        time = pv['response_time']
        print_separator()
        print_header(f"{name} - {time}s")
        print_separator()
        print(pv['provider'].response('get_company_documents', raw, output_format))
    return True


documents_command = Command(_documents_command, "Get company documents (use --code company_code)")

