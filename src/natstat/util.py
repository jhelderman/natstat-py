def format_range_offset_param(possible: list[str | None], offset: int | None) -> str:
    # NatStat appears to only allow one range parameter
    range_param = None
    for p in possible:
        if p is not None:
            range_param = p
            break
    if range_param is None and offset is not None:
        range_param = "_"
    if range_param is not None and offset is not None:
        return f"/{range_param}/{offset}"
    elif range_param is not None and offset is None:
        return f"/{range_param}"
    else:
        return ""
