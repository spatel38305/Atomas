def toColor(i):
    colors = [
        (100,100,100),
        (200,200,200),
        (255,255,255),
        (255,0,0),
        (0,255,0),
        (0,0,255),
        (255,255,0),
        (255,0,255),
        (0,255,255),
        (100,255,255)
    ]
    return colors[i % len(colors)]