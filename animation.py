import sys
import time
from colorama import Fore, Style

def loading_animation(duration=5):
    spinner = ['|', '/', '-', '\\']
    end_time = time.time() + duration
    sys.stdout = sys.__stdout__
    # Text to display at the start
    sys.stdout.write(Fore.CYAN + Style.BRIGHT + "Upgrading WordPress..." + Style.RESET_ALL + "\n")
    sys.stdout.flush()
    
    # Start the animation
    while time.time() < end_time:
        for frame in spinner:
            sys.stdout.write(Fore.YELLOW + f'\r{frame} ' + Fore.GREEN + "Please wait..." + Style.RESET_ALL)
            sys.stdout.flush()
            time.sleep(0.1)
    
    # Finish the animation
    sys.stdout.write(Fore.GREEN + '\rUpgrade complete!        ' + Style.RESET_ALL + '\n')
    sys.stdout.flush()

def welcome_animation(duration=3):
    welcome_text = "Welcome to GitWP AutoUp!"
    num_steps = 20  # Number of steps for the text to move across the screen
    delay = duration / num_steps  # Calculate delay based on the duration and steps
    

    for step in range(num_steps):
        # Calculate spaces to move the text
        spaces = ' ' * step
        sys.stdout.write(Fore.CYAN + Style.BRIGHT + f'\r{spaces}{welcome_text}' + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(delay)
        sys.stdout = sys.__stdout__

    # Hold the final position for a moment
    time.sleep(1)

    # Clear the line after animation
    sys.stdout.write('\r' + ' ' * (len(welcome_text) + num_steps) + '\r')
    sys.stdout.flush()

    # Final welcome message
    sys.stdout.write(Fore.GREEN + "Let's get started!\n" + Style.RESET_ALL)
    sys.stdout.flush()

def end_animation(duration=3):
    closing_text = "Thank you for using GitWP AutoUp!"
    fade_steps = 10  # Number of steps for the fading effect
    delay = duration / fade_steps  # Calculate delay based on the duration and steps

    # Initial display of the message in bright white
    sys.stdout.write(Fore.WHITE + Style.BRIGHT + f'\r{closing_text}' + Style.RESET_ALL)
    sys.stdout.flush()
    time.sleep(1)  # Hold the bright message for a moment

    # Fading effect: gradually darkening the text
    for step in range(fade_steps):
        # Gradually darken the text by reducing brightness
        sys.stdout.write(Fore.LIGHTBLACK_EX + Style.DIM + f'\r{closing_text[:len(closing_text) - step]}' + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(delay)

    # Clear the line after the fade effect
    sys.stdout.write('\r' + ' ' * len(closing_text) + '\r')
    sys.stdout.flush()

    # Final goodbye message
    sys.stdout.write(Fore.GREEN + "Goodbye!\n" + Style.RESET_ALL)
    sys.stdout.flush()