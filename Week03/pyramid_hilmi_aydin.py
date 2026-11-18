def calculate_pyramid_height(number_of_blocks):
    # Initialize the height of the pyramid
    height = 0
    # Blocks required for the current layer
    layer_blocks = 1

    # Continue building layers as long as there are enough blocks
    while number_of_blocks >= layer_blocks:
        # Subtract used blocks from the total
        number_of_blocks -= layer_blocks
        # Increase pyramid height by 1
        height += 1
        # Next layer needs one more block
        layer_blocks += 1

    return height
