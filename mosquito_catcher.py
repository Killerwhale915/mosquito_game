import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mosquito Catcher Game")

# Load individual weapon images using relative paths
base_path = os.path.dirname(__file__)  # Directory of the script
weapon_files = [
    os.path.join(base_path, "image/1.png"),
    os.path.join(base_path, "image/2.png"),
    os.path.join(base_path, "image/3.png"),
    os.path.join(base_path, "image/4.png"),
    os.path.join(base_path, "image/5.png")
]
weapon_size = 100  # Increase weapon size
weapons = [pygame.transform.scale(pygame.image.load(f), (weapon_size, weapon_size)) for f in weapon_files]

# Load larger image for 4th weapon
weapon_4_large = pygame.transform.scale(pygame.image.load(weapon_files[3]), (300, 300))

selected_weapon_index = 0

# Load the mosquito images
mosquito_image = pygame.image.load(os.path.join(base_path, "image/mosquito.png"))
mosquito_image = pygame.transform.scale(mosquito_image, (65, 65))

# Load the mosquito dead image
mosquito_dead_image = pygame.image.load(os.path.join(base_path, "image/mosquito_dead.png"))
mosquito_dead_image = pygame.transform.scale(mosquito_dead_image, (65, 65))

# Mosquito settings
mosquito_spawn_interval = 500  # Spawn every 0.5 seconds (adjusted for faster spawning)
mosquito_lifetime = 3000  # Mosquito stays for 3 seconds
last_spawn_time = pygame.time.get_ticks()
mosquito_list = []
dead_mosquitoes = []  # List to store dead mosquitoes for fade out effect

# Weapon Selection Area (adjusted height)
weapon_area_height = weapon_size + 20  # Adjust height based on weapon size
weapon_area_rect = pygame.Rect(0, HEIGHT - weapon_area_height, WIDTH, weapon_area_height)

# Font for score
font = pygame.font.Font(None, 36)
score = 0
missed_mosquitoes = 0

# Experience and level settings
experience = 0
max_experience = 100  # Experience needed to fill the bar
level = 1

# Experience bar dimensions
exp_bar_width = 150  # Set the width of the experience bar to be shorter
exp_bar_height = 20

# Fade out effect variables
fade_out = False
fade_alpha = 255

# Calculate total width of all weapons
total_width = len(weapons) * (weapon_size + 20) - 20

# Titles for each level range
titles = [
    "모기한테 물린사람", "모기 때문에 깬 사람", "모기 쫓다가 놓친 사람", "Knight", "Gladiator",
    "Champion", "Hero", "Legend", "Master", "Grandmaster",
    "Epic", "Mythic", "Guardian", "Savior", "Warlord",
    "Conqueror", "Titan", "Immortal", "Godlike", "Ultimate"
]

# Function to get the title based on level
def get_title(level):
    # Determine the index for the title
    index = min((level - 1) // 5, len(titles) - 1)
    return titles[index]

# Main game loop
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if a weapon is clicked
            start_x = (WIDTH - total_width) // 2  # Start drawing from the center
            weapon_clicked = False
            for i, weapon in enumerate(weapons):
                weapon_rect = weapon.get_rect(topleft=(start_x + i * (weapon_size + 20), HEIGHT - weapon_area_height + 10))
                if weapon_rect.collidepoint(mouse_pos):
                    selected_weapon_index = i
                    weapon_clicked = True
                    break

            # Trigger the event when 4th weapon is selected and the screen (outside weapon area) is clicked
            if selected_weapon_index == 3 and not weapon_clicked:
                # Add score for all mosquitoes
                score += len(mosquito_list)
                experience += len(mosquito_list) * 10  # Increase experience
                # Add dead mosquitoes to the dead_mosquitoes list
                for mosquito in mosquito_list:
                    dead_mosquitoes.append((mosquito[0], mosquito[1], 255))  # Add dead mosquito for fade out
                mosquito_list.clear()  # Clear all mosquitoes
                fade_out = True  # Start fade out effect
                fade_alpha = 255  # Reset alpha

                # Handle level up if experience exceeds max_experience
                while experience >= max_experience:
                    experience -= max_experience
                    level += 1  # Increase level

            # Check if mosquito is clicked
            weapon_cursor_rect = pygame.Rect(
                mouse_pos[0] - weapon_size // 2,
                mouse_pos[1] - weapon_size // 2,
                weapon_size,
                weapon_size
            )
            for mosquito in mosquito_list[:]:
                mosquito_rect = pygame.Rect(mosquito[0], mosquito[1], 65, 65)
                if weapon_cursor_rect.colliderect(mosquito_rect):
                    mosquito_list.remove(mosquito)
                    dead_mosquitoes.append((mosquito[0], mosquito[1], 255))  # Add dead mosquito for fade out
                    score += 1
                    experience += 10  # Increase experience for each mosquito caught

                    # Handle level up if experience exceeds max_experience
                    while experience >= max_experience:
                        experience -= max_experience
                        level += 1  # Increase level


    # Clear the screen
    screen.fill(WHITE)

    # Get current time
    current_time = pygame.time.get_ticks()

    # Spawn mosquitoes rapidly
    if current_time - last_spawn_time > mosquito_spawn_interval:
        x = random.randint(0, WIDTH - 65)
        y = random.randint(0, HEIGHT - weapon_area_height - 65)  # Keep above weapon area
        mosquito_list.append((x, y, current_time))
        last_spawn_time = current_time

    # Draw mosquitoes and check if they are missed
    for mosquito in mosquito_list[:]:
        if current_time - mosquito[2] > mosquito_lifetime:
            mosquito_list.remove(mosquito)
            missed_mosquitoes += 1
        else:
            screen.blit(mosquito_image, (mosquito[0], mosquito[1]))

    # Draw dead mosquitoes with fade out effect
    for dead_mosquito in dead_mosquitoes[:]:
        x, y, alpha = dead_mosquito
        mosquito_dead_image.set_alpha(alpha)
        # Center the dead mosquito image over the original position
        screen.blit(mosquito_dead_image, (x - mosquito_dead_image.get_width() // 2, y - mosquito_dead_image.get_height() // 2))
        alpha -= 5  # Decrease alpha for fade out effect
        if alpha <= 0:
            dead_mosquitoes.remove(dead_mosquito)
        else:
            dead_mosquitoes[dead_mosquitoes.index(dead_mosquito)] = (x, y, alpha)

    # Always draw selected weapon image as cursor
    if fade_out and selected_weapon_index == 3:
        # Draw the 4th weapon large with fade out effect
        weapon_4_large.set_alpha(fade_alpha)
        screen.blit(weapon_4_large, weapon_4_large.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        fade_alpha -= 5  # Reduce alpha to fade out
        if fade_alpha <= 0:
            fade_out = False  # Stop fade out
    else:
        weapon_rect = weapons[selected_weapon_index].get_rect(center=mouse_pos)
        screen.blit(weapons[selected_weapon_index], weapon_rect.topleft)
    
    pygame.mouse.set_visible(False)  # Hide default mouse cursor

    # Draw weapon selection area and weapons centered
    pygame.draw.rect(screen, BLUE, weapon_area_rect, 2)
    start_x = (WIDTH - total_width) // 2  # Start drawing from the center
    for i, weapon in enumerate(weapons):
        weapon_rect = weapon.get_rect(topleft=(start_x + i * (weapon_size + 20), HEIGHT - weapon_area_height + 10))
        screen.blit(weapon, weapon_rect)
        # Highlight the selected weapon
        if i == selected_weapon_index:
            pygame.draw.rect(screen, RED, weapon_rect, 3)

    # Draw the score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (WIDTH - 150, 10))

    # Draw missed count
    missed_text = font.render(f"Missed: {missed_mosquitoes}", True, BLACK)
    screen.blit(missed_text, (WIDTH - 150, 50))

    # Draw experience bar within screen boundaries
    exp_fill = min((experience / max_experience) * exp_bar_width, exp_bar_width)
    pygame.draw.rect(screen, BLACK, (10, 10, exp_bar_width, exp_bar_height), 2)  # Bar outline
    pygame.draw.rect(screen, GREEN, (10, 10, exp_fill, exp_bar_height))  # Filled part

    # Get current title based on level
    title = get_title(level)

    # Draw level text and title below experience bar
    level_text = font.render(f"Level: {level}", True, BLACK)
    screen.blit(level_text, (10, 35))

    # Draw the title
    title_text = font.render(f"Title: {title}", True, BLACK)
    screen.blit(title_text, (10, 60))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
