"""Company events command."""

from __future__ import annotations

from providerkit.commands.provider import _PROVIDER_COMMAND_CONFIG
from qualitybase.commands import parse_args_from_config
from qualitybase.commands.base import Command
from qualitybase.services.utils import print_header, print_separator

from companyatlas.helpers import get_company_events

_ARG_CONFIG = {
    **_PROVIDER_COMMAND_CONFIG,
    'code': {'type': str, 'default': ''},
}


def _events_command(args: list[str]) -> bool:
    parsed = parse_args_from_config(args, _ARG_CONFIG, prog='events')
    kwargs = {}
    kwargs['attribute_search'] = parsed.get('attr', {}).get('kwargs', {})
    output_format = parsed.get('format', 'terminal')
    raw = parsed.get('raw', False)
    code = parsed.pop('code')
    first = parsed.pop('first', False)
    pvs_events = get_company_events(code, first=first, **kwargs)
    for pv in pvs_events:
        print_separator()
        print_header(pv['provider'].name)
        print_separator()
        print(pv['provider'].response('get_company_events', raw, output_format))
    return True


events_command = Command(_events_command, "Get company events (use --code company_code)")

