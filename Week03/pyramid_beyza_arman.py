def calculate_pyramid_height(blocks):
    """Return the number of complete layers that can be built."""
    height = 0
    next_layer = 1
    while blocks >= next_layer:
        blocks -= next_layer
        height += 1
        next_layer += 1
    return height
