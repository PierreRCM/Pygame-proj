import pygame as pg

pg.font.init()


class Menu:
    """Main class for all menu in the game"""

    def __init__(self, words, screen, background=None, color=(0, 0, 0), font_size=20, menu_position = "center"):

        self.screen = screen   # most of the time screen size
        self.background = background  # for the moment color but need background
        self.color = color
        self.words = words  # list of words to display
        self.font_object = pg.font.Font(None, font_size)
        self.rect_size = None
        self.rectangle = []
        self.menu_position = menu_position
        self._get_rect_size()  # size of the rect depending on the longest font


    def _get_rect_size(self):
        """input all the words we need to display get the size of the largest rectangle"""

        self.words.sort(key=len, reverse=True)  # Store words in length order, indice 0 is the longer
        longest = self.words[0]
        self.rect_size = self.font_object.size(longest)

    def _place_rectangle(self):

        screen_size = self.screen.size()

        if self.menu_position is "center":

            for i in range(len(self.words)):

                screen_center = (screen_size[0] / 2, screen_size[1] / 2)  # Tuple of the screen center
                x_rect_position = screen_center[0] - self.rect_size[0] / 2
                y_rect_position = screen_center[1] - self.rect_size[1] / 2


menu = Menu(["qsdf", "sdfqsdfqshfmq", "sdfqslfqs"], (800, 600))

