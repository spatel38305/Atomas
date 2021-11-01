def toColor(i):
    colors = [
        (100,100,100),
        (200,200,200),
        (255,0,0),
        (0,255,0),
        (0,0,255),
        (255,255,0),
        (255,0,255),
        (0,255,255),
        (100,255,255)
    ]
    return colors[i % len(colors)]

def applyattr(obj, key, params):
    apply(getattr(obj, key), params)

def apply(fn, params):
    if isinstance(params, list):
        fn(*params)
    elif isinstance(params, dict):
        args = []
        if 'args' in params:
            args = params['pargs']
            del params['args']
        fn(*args, **params)