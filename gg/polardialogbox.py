# polardialogbox.py
#
# GameGenerator is free to use, modify, and redistribute for any purpose
# that is both educational and non-commercial, as long as this paragraph
# remains unmodified and in its entirety in a prominent place in all
# significant portions of the final code. No warranty, express or
# implied, is made regarding the merchantability, fitness for a
# particular purpose, or any other aspect of the software contained in
# this module.

import pygame
import gg.colors


class PolarDialogBox:
    """A modal dialog box to ask the user a yes-no ("polar") question.

    The answer can be selected by the user by clicking the appropriate
    button with the mouse, pressing the Y or N keys, or using the arrow
    keys to select a button and then pressing Enter. Escape kills the
    dialog box with no action taken.

    Instances of this class should be created using a 'with' statement.
    """
    YES_BUTTON = 0
    NO_BUTTON = 1

    def __init__(self, screen, clock, size=(400, 200)):
        """Initializes the values of the box."""
        self.size = size
        self.font_size = 28
        self.font_color_prompt = gg.colors.MEDIUM_DARK_GRAY
        self.font_color_buttons = gg.colors.WHITE
        self.background_color = gg.colors.LIGHT_GRAY
        self.border_color = gg.colors.GRAY
        self.button_color_default = gg.colors.GRAY
        self.border_width = 3
        self.shadow_x_offset = 3
        self.shadow_y_offset = 3
        self._screen = screen
        self._screen_rect = screen.get_rect()
        self._clock = clock
        self._font = pygame.font.Font(None, self.font_size)
        self._box_rect = None
        self._button_yes_rect = None
        self._button_no_rect = None
        self._button_ctr_offset = 20
        self._focused_button = self.YES_BUTTON
        self._active_button = None

        if (pygame.event.get_blocked(pygame.KEYDOWN) or
            pygame.event.get_blocked(pygame.MOUSEMOTION) or
            pygame.event.get_blocked(pygame.MOUSEBUTTONDOWN) or
            pygame.event.get_blocked(pygame.MOUSEBUTTONUP)):
            pygame.event.set_allowed([pygame.KEYDOWN, pygame.MOUSEMOTION,
                                      pygame.MOUSEBUTTONDOWN,
                                      pygame.MOUSEBUTTONUP])

        pygame.mouse.set_visible(True)

    def __enter__(self):
        """Return the box instance upon entering."""
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Remove the mouse cursor on window exit."""
        pygame.mouse.set_visible(False)

    def get_answer(self, prompt_text):
        """Display the dialog box and wait for the user's response.

        The return value is true if the answer is yes, false otherwise.
        """
        self._render_box(prompt_text)

        while True:
            self._render_buttons()
            is_answer_yes = self._get_input()

            if is_answer_yes is not None:
                return is_answer_yes

            if self._clock is not None:
                self._clock.tick(60)

    def _render_box(self, prompt_text):
        """Draw the dialog box centered on the screen."""
        box, box_rect = gg.utils._get_surface(self.size, self.background_color)

        # Blit the prompt text onto the box
        prompt, prompt_rect = gg.utils._get_rendered_text(
            self._font, prompt_text, self.font_color_prompt)
        prompt_rect.centerx = box_rect.centerx
        prompt_rect.y = box_rect.height * 0.25
        box.blit(prompt, prompt_rect)

        # Draw the border
        if self.border_width > 0:
            pygame.draw.rect(box, self.border_color,
                             box_rect, self.border_width)

        # Center the box and give the rect to the instance
        box_rect.center = self._screen_rect.center
        self._box_rect = box_rect

        # Make the box shadow
        box_shadow = box.copy()
        box_shadow.fill(gg.colors.MEDIUM_DARK_GRAY)
        box_shadow_rect = box_rect.move(self.shadow_x_offset,
                                        self.shadow_y_offset)

        # Put the box on the screen
        self._screen.blit(box_shadow, box_shadow_rect)
        self._screen.blit(box, box_rect)
        pygame.display.update([box_shadow_rect, box_rect])

    def _render_buttons(self):
        """Draw the Yes and No buttons in their current state."""
        button_yes, button_yes_rect = self._get_button('Yes', self.YES_BUTTON)
        button_no, button_no_rect = self._get_button('No', self.NO_BUTTON)

        if self._button_yes_rect is None or self._button_no_rect is None:
            self._button_yes_rect = button_yes_rect
            self._button_no_rect = button_no_rect

        self._screen.blit(button_yes, button_yes_rect)
        self._screen.blit(button_no, button_no_rect)
        pygame.display.update([button_yes_rect, button_no_rect])

    def _get_button(self, text, button_specifier):
        """Return a button surface containing the text."""
        size = (90, 40)

        if button_specifier == self._active_button:
            # Invert the colors when active
            background_color = self.font_color_buttons
            text_color = self.button_color_default
        else:
            background_color = self.button_color_default
            text_color = self.font_color_buttons

        button, button_rect = gg.utils._get_surface(size, background_color)
        text, text_rect = gg.utils._get_rendered_text(self._font,
                                                      text, text_color)
        gg.utils._blit_text_to_surface(text, button, text_rect, button_rect)

        # Draw the border if this button has the focus
        if button_specifier == self._focused_button:
            pygame.draw.rect(button, gg.colors.BLACK, button_rect,
                             self.border_width)

        # Position the button in the right place
        if button_specifier == self.YES_BUTTON:
            button_rect.right = (self._box_rect.centerx
                                 - self._button_ctr_offset)
        else:
            button_rect.left = self._box_rect.centerx + self._button_ctr_offset

        button_rect.y = self._box_rect.centery + self._button_ctr_offset

        return (button, button_rect)

    def _get_input(self):
        """Return true if the user answers yes, false otherwise.

        If the input doesn't correspond to a final answer, such as
        moving focus from one button to another, then the return value
        is None.
        """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    self._focused_button = self.YES_BUTTON
                    self._active_button = self.YES_BUTTON
                    return True
                elif event.key == pygame.K_n:
                    self._focused_button = self.NO_BUTTON
                    self._active_button = self.NO_BUTTON
                    return False
                elif event.key == pygame.K_ESCAPE:
                    return False
                elif (event.key == pygame.K_RETURN or
                      event.key == pygame.K_KP_ENTER):
                    if self._focused_button == self.YES_BUTTON:
                        self._active_button = self.YES_BUTTON
                        return True
                    self._active_button = self.NO_BUTTON
                    return False
                elif (event.key == pygame.K_LEFT and
                      self._focused_button == self.NO_BUTTON):
                    self._focused_button = self.YES_BUTTON
                elif (event.key == pygame.K_RIGHT and
                      self._focused_button == self.YES_BUTTON):
                    self._focused_button = self.NO_BUTTON
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                if self._button_yes_rect.collidepoint(mouse_pos):
                    self._focused_button = self.YES_BUTTON
                elif self._button_no_rect.collidepoint(mouse_pos):
                    self._focused_button = self.NO_BUTTON
                elif self._active_button is not None:
                    self._active_button = None
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self._button_yes_rect.collidepoint(mouse_pos):
                    self._active_button = self.YES_BUTTON
                elif self._button_no_rect.collidepoint(mouse_pos):
                    self._active_button = self.NO_BUTTON
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self._button_yes_rect.collidepoint(mouse_pos):
                    return True
                elif self._button_no_rect.collidepoint(mouse_pos):
                    return False
        return None
