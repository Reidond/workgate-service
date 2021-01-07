class ChakraUiLight:
    def __init__(self):
        pass

    def get_line_color(self):
        return '#B2F5EA'

    def get_text_color(self):
        return '#234E52'

    def get_bg_color(self):
        return '#FFFFFF'

    line_color = property(get_line_color, None)
    text_color = property(get_text_color, None)
    bg_color = property(get_bg_color, None)


class ChakraUiDark:
    def __init__(self):
        pass

    def get_line_color(self):
        return '#278c7f'

    def get_text_color(self):
        return '#81E6D9'

    def get_bg_color(self):
        return '#1A202C'

    line_color = property(get_line_color, None)
    text_color = property(get_text_color, None)
    bg_color = property(get_bg_color, None)


def palette(color_mode):
    if color_mode == 'dark':
        return ChakraUiDark()
    elif color_mode == 'light':
        return ChakraUiLight()
    return ChakraUiLight()
