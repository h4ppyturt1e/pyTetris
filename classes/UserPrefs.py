"""
UserPrefs.py -- UserPrefs class for tetris

Author: Ryan Nicholas Permana (2024)
"""

import pygame as pg
from Constants import *
from os import path

class UserPrefs:
    def __init__(self, username):
        self.keybinds = {
            "left": pg.K_LEFT,
            "right": pg.K_RIGHT,
            "down": pg.K_DOWN,
            "rotateCW": pg.K_UP,
            "rotateCCW": pg.K_z,
            "hardDrop": pg.K_SPACE,
            "reset": pg.K_r,
        }
        self.DAS = 133
        self.ARR = 10
        self.SDF = 20
        self.username = username
        
    def __str__(self):
        res = f"Keybinds:\n"
        for action, key in self.keybinds.items():
            res += f"{action}: {key}\n"
        res += f"DAS: {self.DAS}\n"
        res += f"ARR: {self.ARR}\n"
        res += f"SDF: {self.SDF}\n"
        return res

    def setKeybind(self, action, key):
        if action not in self.keybinds.keys():
            print(repr(action))
            raise ValueError("Invalid action")
        
        try:
            self.keybinds[action] = key
        except KeyError:
            print("Invalid action")
            
    def setDAS(self, value):
        self.DAS = value
    
    def setARR(self, value):
        self.ARR = value
    
    def setSDF(self, value):
        self.SDF = value
    
    def generateKeybinds(self):
        pg.init()
        screen = pg.display.set_mode((800, 600))
        pg.display.set_caption("Set Keybinds")

        font = pg.font.SysFont(None, 36)
        done = False
        current_action = None

        while not done:
            screen.fill((0, 0, 0))

            # Display instructions
            instructions = font.render('Press a key to set the bind for the action', True, (255, 255, 255))
            screen.blit(instructions, (20, 20))

            # Display current keybinds
            y = 60
            for action, key in self.keybinds.items():
                key_name = pg.key.name(key)
                text = font.render(f'{action}: {key_name}', True, (255, 255, 255))
                screen.blit(text, (20, y))
                y += 30

            pg.display.flip()
            
            if current_action is not None:
                message = font.render(f'Choose a new key bind for {current_action}', True, (255, 255, 255))
                screen.blit(message, (20, 560))
                pg.display.flip()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                elif event.type == pg.KEYDOWN:
                    if current_action:
                    # Check if the key is already bound to another action
                        key_already_bound = False
                        for action, key in self.keybinds.items():
                            if action != current_action and key == event.key:
                                key_already_bound = True
                                break

                        if key_already_bound:
                            print("This key is already bound to another action. Choose a different key.")
                        else:
                            self.setKeybind(current_action, event.key)
                            current_action = None
                    else:
                        # Check if the pressed key corresponds to a valid action
                        if event.key in self.keybinds.values():
                            # Find which action corresponds to the pressed key
                            for action, key in self.keybinds.items():
                                if key == event.key:
                                    current_action = action
                                    break
                                
            pg.time.wait(100)
            

        pg.quit()

    def adjustSettings(self):
        pg.init()
        screen = pg.display.set_mode((400, 400))
        pg.display.set_caption("Adjust Settings")

        font = pg.font.SysFont(None, 36)
        done = False
        selected_setting = None
        
        # Define rectangles for buttons
        das_button = pg.Rect(50, 80, 300, 40)
        arr_button = pg.Rect(50, 130, 300, 40)
        sdf_button = pg.Rect(50, 180, 300, 40)

        def draw_buttons():
            # Instruction at the top
            instruction_text = font.render('Click a setting to change', True, (255, 255, 255))
            screen.blit(instruction_text, (50, 10))

            # Draw DAS button and text
            pg.draw.rect(screen, (0, 128, 255), das_button)  # Light blue button
            das_text = font.render(f'DAS: {self.DAS}', True, (255, 255, 255))
            screen.blit(das_text, (60, 85))

            # Draw ARR button and text
            pg.draw.rect(screen, (0, 128, 255), arr_button)  # Light blue button
            arr_text = font.render(f'ARR: {self.ARR}', True, (255, 255, 255))
            screen.blit(arr_text, (60, 135))

            # Draw SDF button and text
            pg.draw.rect(screen, (0, 128, 255), sdf_button)  # Light blue button
            sdf_text = font.render(f'SDF: {self.SDF}', True, (255, 255, 255))
            screen.blit(sdf_text, (60, 185))

        def draw_selection_text():
            if selected_setting:
                if selected_setting == 'DAS':
                    selected_min = DAS_MIN
                    selected_max = DAS_MAX
                elif selected_setting == 'ARR':
                    selected_min = ARR_MIN
                    selected_max = ARR_MAX
                elif selected_setting == 'SDF':
                    selected_min = SDF_MIN
                    selected_max = SDF_MAX
                else:
                    selected_min = 0
                    selected_max = 0
                lines = [
                    f'You are modifying {selected_setting}',
                    f'Range: {selected_min} - {selected_max}',
                    'Left and Right to modify',
                    'Enter to save'
                ]
                y = 250
                for line in lines:
                    line_text = font.render(line, True, (255, 255, 255))
                    screen.blit(line_text, (50, y))
                    y += 30  # Adjust spacing between lines as needed

        last_key_press_time = 0
        
        while not done:
            screen.fill((0, 0, 0))
            draw_buttons()
            draw_selection_text()
            
            keys_pressed = pg.key.get_pressed()
            current_time = pg.time.get_ticks()

            if selected_setting:
                if keys_pressed[pg.K_RIGHT] or keys_pressed[pg.K_LEFT]:
                    if key_hold_start_time is None:
                        key_hold_start_time = current_time  # Start timing key hold duration

                    if current_time - last_key_press_time > KEY_REPEAT_DELAY:
                        change_amount = 5 if (current_time - key_hold_start_time > ACCELERATED_CHANGE_DELAY) else 1

                        if keys_pressed[pg.K_RIGHT]:
                            if selected_setting == 'DAS':
                                self.DAS = min(self.DAS + change_amount, DAS_MAX)
                            elif selected_setting == 'ARR':
                                self.ARR = min(self.ARR + change_amount, ARR_MAX)
                            elif selected_setting == 'SDF':
                                self.SDF = min(self.SDF + change_amount, SDF_MAX)
                            last_key_press_time = current_time
                        elif keys_pressed[pg.K_LEFT]:
                            if selected_setting == 'DAS':
                                self.DAS = max(self.DAS - change_amount, DAS_MIN)
                            elif selected_setting == 'ARR':
                                self.ARR = max(self.ARR - change_amount, ARR_MIN)
                            elif selected_setting == 'SDF':
                                self.SDF = max(self.SDF - change_amount, SDF_MIN)
                            last_key_press_time = current_time
                else:
                    key_hold_start_time = None  # Reset if no key is pressed
                    
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                elif event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if das_button.collidepoint(mouse_pos):
                        selected_setting = 'DAS'
                    elif arr_button.collidepoint(mouse_pos):
                        selected_setting = 'ARR'
                    elif sdf_button.collidepoint(mouse_pos):
                        selected_setting = 'SDF'
                elif event.type == pg.KEYDOWN:
                    if selected_setting:
                        if event.key == pg.K_RETURN:
                            selected_setting = None
                    else:
                        if event.key == pg.K_1:
                            selected_setting = 'DAS'
                        elif event.key == pg.K_2:
                            selected_setting = 'ARR'
                        elif event.key == pg.K_3:
                            selected_setting = 'SDF'

            pg.display.flip()
        pg.quit()

    def writeToPrefs(self):
        prefsFileName = f"{self.username}.prefs"
        with open(prefsFileName, "w") as prefsFile:
            for action, key in self.keybinds.items():
                if action in {"DAS", "ARR", "SDF"}:
                    continue
                key = pg.key.name(key)
                prefsFile.write(f"'{action}':{key}\n")
            prefsFile.write("\n")
            prefsFile.write(f"DAS:{self.DAS}\n")
            prefsFile.write(f"ARR:{self.ARR}\n")
            prefsFile.write(f"SDF:{self.SDF}\n")
    
    def readFromPrefs(self):
        # check existence of prefs file
        if not path.exists(f"{self.username}.prefs"):
            return
        
        pg.init()
        prefsFileName = f"{self.username}.prefs"
        with open(prefsFileName, "r") as prefsFile:
            for line in prefsFile.readlines():
                if line == "\n":
                    continue
                
                line = line.strip()
                action, value = line.split(":")
                if action.strip("'") in {"left", "right", "down", "rotateCW", "rotateCCW", "hardDrop", "reset"}:
                    value = pg.key.key_code(value)
                    self.setKeybind(action.strip("'"), value)
                else:
                    value = int(value)
                    match action:
                        case "DAS":
                            self.setDAS(value)
                        case "ARR":
                            self.setARR(value)
                        case "SDF":
                            self.setSDF(value)
                        case _:
                            raise ValueError("Invalid action")
    
    
if __name__ == '__main__':
    user = "Player"
    prefs = UserPrefs(user)
    prefs.readFromPrefs()
    print(prefs)
    print()
    prefs.generateKeybinds()
    prefs.adjustSettings()
    prefs.writeToPrefs()
    print(prefs)