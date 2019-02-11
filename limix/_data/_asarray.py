def asarray(x, target, dims=None):
    from xarray import DataArray
    from ._conf import CONF

    if target not in CONF["data_names"]:
        raise ValueError(f"Unknown target name: {target}.")

    x = DataArray(x)

    if isinstance(dims, (tuple, list)):
        dims = {a: n for a, n in enumerate(dims)}
    dims = _numbered_axes(dims)
    if len(set(dims.values())) < len(dims.values()):
        raise ValueError("`dims` must not contain duplicated values.")
    x = x.rename({x.dims[axis]: name for axis, name in dims.items()})
    x = _set_missing_dim(x, CONF["data_dims"][target])
    x = x.transpose(*CONF["data_dims"][target])
    x.name = target

    return x


def _numbered_axes(dims):

    if dims is None:
        return {}

    naxes = {}
    for a, v in dims.items():
        if a == "row":
            naxes[0] = v
        elif a == "col":
            naxes[1] = v
        else:
            naxes[a] = v

    return naxes


def _set_missing_dim(arr, dims):
    unk_dims = set(arr.dims) - set(dims)
    if len(unk_dims) > 1:
        raise ValueError("Too many unknown dimension names.")
    elif len(unk_dims) == 1:
        known_dims = set(dims) - set(arr.dims)
        if len(known_dims) != 1:
            raise ValueError("Can't figure out what is the missing dimension name.")
        arr = arr.rename({unk_dims.pop(): known_dims.pop()})
    return arr
