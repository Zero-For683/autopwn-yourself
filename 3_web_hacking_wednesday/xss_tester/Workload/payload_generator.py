from skeleton import SKELETONS # Phase 1 payloads
from events_tags import all_tags, non_interactive_events # For phase 2 / Full matrix payloads


def generate_core_payloads(
    context: str,
    tag: str = None,
    evt: str = None,
    marker: str = None,
    b64_payload: str = None
) -> list[str]:
    """
    Generate the core set of XSS payloads for the given context.

    context: one of the keys in SKELETONS (html_data, attribute, js_string, url, css)
    tag: the HTML tag name (for html_data, attribute, css contexts)
    evt: event handler name (for attribute contexts)
    marker: the unique marker to insert in the payload (e.g. 'z0f863')
    b64_payload: Base64-encoded JS snippet (for url context templates)

    Returns a list of raw (unencoded) payload strings.
    """
    # prepare standard payload expression
    payload_expr = f"alert('{marker}')" if marker else ''

    # collect formatting parameters
    params = {
        'tag': tag,
        'evt': evt,
        'payload': payload_expr,
        'b64_payload': b64_payload,
    }

    # get the core templates for this context
    templates = SKELETONS.get(context, [])

    # format each template with the params
    core_payloads = []
    for tpl in templates:
        try:
            core_payloads.append(tpl.format(**params))
        except KeyError:
            # missing param for this context; skip
            continue

    return core_payloads
