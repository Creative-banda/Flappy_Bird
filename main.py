import sys, time, random, pygame, json
from collections import deque
import cv2 as cv, mediapipe as mp
from pathlib import Path
import math

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
pygame.init()

# Initialize required elements/environment
VID_CAP = cv.VideoCapture(0)

# Check if camera opened successfully
if not VID_CAP.isOpened():
    print("Error: Could not open camera")
    sys.exit()

# Get the screen info
screen_info = pygame.display.Info()
window_size = (screen_info.current_w, screen_info.current_h)
screen = pygame.display.set_mode(window_size, pygame.FULLSCREEN)

# Colors
BLUE = (125, 220, 232)
DARK_BLUE = (0, 150, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
GRAY = (100, 100, 100)
TRANSPARENT_BLACK = (0, 0, 0, 128)
GOLD = (255, 215, 0)  # RGB for gold

# Load sound effects and background music
pygame.mixer.init()
bg_music = pygame.mixer.Sound('assets/music/background_music3.mp3')
pipe_pass_sound = pygame.mixer.Sound('assets/music/pipe_pass.mp3')
game_over_sound = pygame.mixer.Sound('assets/music/game_over.mp3')

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

def create_transparent_surface(width, height):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)  # Supports transparency
    return surface

# High scores file handling
def load_high_scores():
    try:
        with open('high_scores.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_high_score(username, score):
    scores = load_high_scores()
    scores.append({"username": username, "score": score})
    scores.sort(key=lambda x: x["score"], reverse=True)
    scores = scores[:10]  # Keep only top 10 scores
    with open('high_scores.json', 'w') as f:
        json.dump(scores, f)

def draw_text_with_shadow(surface, text, font, color, position, shadow_color=(0, 0, 0)):
    # Draw shadow
    shadow = font.render(text, True, shadow_color)
    shadow_pos = (position[0] + 2, position[1] + 2)
    surface.blit(shadow, shadow_pos)
    # Draw main text
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)

def draw_scores_panel(surface, font):
    scores = load_high_scores()
    
    # Define the panel dimensions and position
    panel_rect = pygame.Rect(window_size[0] // 3, window_size[1] // 1.5, window_size[0] // 3, 150)
    
    # Create a semi-transparent dark blue background
    panel_surface = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
    panel_surface.fill((25, 25, 112, 200))  # RGBA: Dark Blue with transparency
    
    # Draw the semi-transparent panel and a glowing outline
    surface.blit(panel_surface, (panel_rect.x, panel_rect.y))
    pygame.draw.rect(surface, GOLD, panel_rect, 3, border_radius=15)
    
    # Draw the title "Top Scores"
    title_text = "Top Scores"
    draw_glowing_text(surface, title_text, font, WHITE, (panel_rect.centerx, panel_rect.y + 10))
    
    # Space between each score
    score_spacing = 35  # Increased spacing for better readability
    
    # Draw each score with more space between lines
    for i, score in enumerate(scores[:3]):
        score_text = f"#{i + 1} {score['username']}: {score['score']}"
        score_surf = font.render(score_text, True, WHITE)
        
        # Center the scores in the panel
        score_x = panel_rect.x + 20  # Indentation from left
        score_y = panel_rect.y + 40 + i * score_spacing
        surface.blit(score_surf, (score_x, score_y))

def draw_glowing_text(surface, text, font, color, pos):
    shadow_color = (0, 0, 0)
    shadow_offset = 5
    text_surface = font.render(text, True, shadow_color)
    surface.blit(text_surface, (pos[0] - shadow_offset, pos[1] - shadow_offset))  # Shadow
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, pos)

def draw_gradient_button(surface, rect, text, font, color, enabled):
    colors = [(0, 100, 0), (0, 255, 0)] if enabled else [(50, 50, 50), (100, 100, 100)]
    pygame.draw.rect(surface, colors[0], rect, border_radius=10)
    pygame.draw.rect(surface, colors[1], rect.inflate(-5, -5), border_radius=10)
    text_surf = font.render(text, True, color)
    surface.blit(text_surf, text_surf.get_rect(center=rect.center))

def show_start_screen():
    username = ""
    input_active = True
    global score

    # Create styled input box and button
    input_box = pygame.Rect(window_size[0] // 4, window_size[1] // 2, window_size[0] // 2, 60)
    start_button = pygame.Rect(window_size[0] // 3, window_size[1] // 2 + 100, window_size[0] // 3, 60)

    # Fonts
    title_font = pygame.font.Font("assets/fonts/FlappyBirdy.ttf", 80)  # Use a playful font
    input_font = pygame.font.SysFont("Helvetica Bold.ttf", 36)
    score_font = pygame.font.SysFont("Helvetica Bold.ttf", 32)

    # Background image
    bg_image = pygame.image.load("assets/images/flappy_bg.jpeg")
    bg_image = pygame.transform.scale(bg_image, window_size)

    # Clock for animations
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                VID_CAP.release()
                cv.destroyAllWindows()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos) and username:
                    return username
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username:
                    return username
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif len(username) < 15:  # Limit username length
                    if event.unicode.isalnum() or event.unicode == '_':  # Only allow alphanumeric and underscore
                        username += event.unicode

        # Draw the background image
        screen.blit(bg_image, (0, 0))

        # Draw title with a glowing effect
        title_text = "Flappy Bird"
        draw_glowing_text(screen, title_text, title_font, WHITE, (window_size[0] // 2, window_size[1] // 5))

        # Draw input box
        pygame.draw.rect(screen, (255, 255, 255, 200), input_box, border_radius=10)  # Semi-transparent white
        pygame.draw.rect(screen, (255, 215, 0), input_box, 3, border_radius=10)  # Golden glowing border

        # Load and draw a Flappy Bird icon near the input box
        bird_icon = pygame.image.load("assets/images/bird_sprite.png")
        bird_icon = pygame.transform.scale(bird_icon, (50, 50))
        screen.blit(bird_icon, (input_box.x - 60, input_box.y + 5))

        # Draw placeholder or username
        if not username:
            placeholder = input_font.render("Enter your username", True, (150, 150, 150))  # Gray placeholder text
            screen.blit(placeholder, (input_box.x + 10, input_box.y + 10))
        else:
            txt_surface = input_font.render(username, True, BLACK)
            screen.blit(txt_surface, (input_box.x + 10, input_box.y + 10))

        # Draw start button with gradient and hover effect
        mouse_pos = pygame.mouse.get_pos()
        button_color = (100, 200, 100) if username and start_button.collidepoint(mouse_pos) else (150, 150, 150)
        pygame.draw.rect(screen, button_color, start_button, border_radius=10)
        draw_gradient_button(screen, start_button, "Start Game", input_font, WHITE, username)

        # Draw top scores panel
        draw_scores_panel(screen, score_font)

        pygame.display.flip()
        clock.tick(30)

def draw_gradient_background(surface, color1, color2):
    """Draws a vertical gradient background."""
    for i in range(surface.get_height()):
        color = (
            color1[0] + (color2[0] - color1[0]) * i // surface.get_height(),
            color1[1] + (color2[1] - color1[1]) * i // surface.get_height(),
            color1[2] + (color2[2] - color1[2]) * i // surface.get_height(),
        )
        pygame.draw.line(surface, color, (0, i), (surface.get_width(), i))

def create_transparent_surface(width, height, alpha=150):
    """Creates a semi-transparent surface."""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.fill((0, 0, 0, alpha))  # Black with alpha transparency
    return surface

def draw_text_with_shadow(surface, text, font, color, pos):
    """Draws text with a shadow effect."""
    shadow_color = (0, 0, 0)
    shadow_offset = (2, 2)
    shadow_surface = font.render(text, True, shadow_color)
    text_surface = font.render(text, True, color)
    surface.blit(shadow_surface, (pos[0] + shadow_offset[0], pos[1] + shadow_offset[1]))
    surface.blit(text_surface, pos)

def show_countdown():
    font = pygame.font.SysFont("Helvetica Bold.ttf", 120)
    
    for i in range(3, 0, -1):
        screen.fill(BLUE)
        # Create a pulsing effect
        for size in range(120, 150, 2):
            screen.fill(BLUE)
            countdown_font = pygame.font.SysFont("Helvetica Bold.ttf", size)
            text = countdown_font.render(str(i), True, WHITE)
            text_rect = text.get_rect(center=(window_size[0]//2, window_size[1]//2))
            screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.wait(20)
        pygame.time.wait(700)

def show_game_over(username, score):
    # Stop background music and play game over sound
    bg_music.stop()
    game_over_sound.play()
    
    # Delay before capturing the reaction photo
    pygame.time.wait(1000)

    # Capture a frame from the camera
    ret, frame = VID_CAP.read()
    if ret:
        # Ensure the 'react' directory exists
        Path("react").mkdir(parents=True, exist_ok=True)
        
        # Save the captured frame as an image file in the 'react' directory
        reaction_image_path = f"react/{username}_reaction.png"
        cv.imwrite(reaction_image_path, frame)
        print(f"Reaction image saved as {reaction_image_path}")
    else:
        print("Error capturing reaction image")
    save_high_score(username, score)
    font_large = pygame.font.SysFont("assets/fonts/Helvetica Bold.ttf", int(window_size[1]/8))
    font_medium = pygame.font.SysFont("assets/fonts/Helvetica Bold.ttf", int(window_size[1]/12))
    
    # Create game over screen with animation
    alpha = 0
    while alpha < 255:
        bg_image = pygame.image.load(reaction_image_path)
        bg_image = pygame.transform.scale(bg_image, window_size)
        screen.blit(bg_image, (0, 0))
        
        if alpha > 128:
            game_over_text = font_large.render('Game Over!', True, WHITE)
            score_text = font_medium.render(f'Final Score: {score}', True, WHITE)
            tr = game_over_text.get_rect(center=(window_size[0]//2, window_size[1]//2))
            sr = score_text.get_rect(center=(window_size[0]//2, window_size[1]//2 + 100))
            screen.blit(game_over_text, tr)
            screen.blit(score_text, sr)
        
        pygame.display.flip()
        alpha += 5
        pygame.time.wait(5)
    
    pygame.time.wait(2000)
    
    # Show the start screen again
    main()

def create_circular_gradient(size, inner_color, outer_color):
    """Create a circular gradient surface."""
    width, height = size
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    center_x, center_y = width // 2, height // 2
    max_radius = min(center_x, center_y)
    
    for radius in range(max_radius, 0, -1):
        color = (
            outer_color[0] + (inner_color[0] - outer_color[0]) * radius // max_radius,
            outer_color[1] + (inner_color[1] - outer_color[1]) * radius // max_radius,
            outer_color[2] + (inner_color[2] - outer_color[2]) * radius // max_radius,
            int(255 * (radius / max_radius)),  # Alpha for smooth fade
        )
        pygame.draw.circle(surface, color, (center_x, center_y), radius)
    
    return surface

def game_loop(username):
    # Play background music
    bg_music.play(-1)  # Loop indefinitely

    # Bird and pipe init
    bird_img = pygame.image.load("assets/images/bird_sprite.png")
    bird_height = int(window_size[1] / 12)
    bird_width = int(bird_img.get_width() * (bird_height / bird_img.get_height()))
    bird_img = pygame.transform.scale(bird_img, (bird_width, bird_height))
    bird_frame = bird_img.get_rect()
    bird_frame.center = (window_size[0] // 6, window_size[1] // 2)

    pipe_frames = deque()
    pipe_img = pygame.image.load("assets/images/pipe_sprite_single.png")
    pipe_width = int(window_size[0] / 8)
    pipe_height = int(pipe_img.get_height() * (pipe_width / pipe_img.get_width()))
    pipe_img = pygame.transform.scale(pipe_img, (pipe_width, pipe_height))

    pipe_starting_template = pipe_img.get_rect()
    space_between_pipes = int(window_size[1] / 4)

    # Load background image
    background_img = pygame.image.load("assets/images/background_image.jpg")
    background_img = pygame.transform.scale(background_img, window_size)

    # Game variables
    game_clock = time.time()
    stage = 1
    pipeSpawnTimer = 0
    time_between_pipe_spawn = 40
    dist_between_pipes = window_size[0] // 2
    pipe_velocity = lambda: dist_between_pipes / time_between_pipe_spawn
    score = 0
    didUpdateScore = False
    game_is_running = True
    
    min_pipe_height = int(window_size[1] * 0.2)
    max_pipe_height = int(window_size[1] * 0.8)

    # Load high scores once at the start
    high_scores = load_high_scores()
    current_high_score = high_scores[0]["score"] if high_scores else 0

    with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as pose:
        while True:
            if not game_is_running:
                show_game_over(username, score)
                return

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    VID_CAP.release()
                    cv.destroyAllWindows()
                    pygame.quit()
                    sys.exit()

            ret, frame = VID_CAP.read()
            if not ret:
                print("Error reading frame from camera")
                continue

            # Rotate the frame to vertical orientation
            frame = cv.rotate(frame, cv.ROTATE_90_COUNTERCLOCKWISE)

            # Process the camera frame for pose detection (but don't display it)
            frame.flags.writeable = False
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            results = pose.process(frame)
            frame.flags.writeable = True

            # Draw the game background on full screen
            screen.blit(background_img, (0, 0))

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark

                # Adjust vertical mapping
                left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
                left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]

                # Use 'x' values for vertical positioning (after rotation)
                left_mid_y = (left_shoulder.x + left_wrist.x) / 2  # Adjust for rotated frame
                sensitivity_factor = 1.5
                mid_y = left_mid_y * sensitivity_factor

                bird_frame.centery = int(mid_y * window_size[1])
                if bird_frame.top < 0: bird_frame.y = 0
                if bird_frame.bottom > window_size[1]: bird_frame.y = window_size[1] - bird_frame.height

            
            # Update pipe positions
            for pf in pipe_frames:
                pf[0].x -= int(pipe_velocity())
                pf[1].x -= int(pipe_velocity())

            if len(pipe_frames) > 0 and pipe_frames[0][0].right < 0:
                pipe_frames.popleft()

            # Draw the game elements on the full screen
            screen.blit(bird_img, bird_frame)
                        
            checker = True
            for pf in pipe_frames:
                if pf[0].left <= bird_frame.x <= pf[0].right:
                    checker = False
                    if not didUpdateScore:
                        score += 1
                        didUpdateScore = True
                        pipe_pass_sound.play()  # Play pipe pass sound
                screen.blit(pipe_img, pf[1])
                screen.blit(pygame.transform.flip(pipe_img, 0, 1), pf[0])
            if checker: didUpdateScore = False

            # Create a semi-transparent overlay for the score panel in the top-left
            score_panel = create_transparent_surface(window_size[0]//4, window_size[1]//6)
            score_panel_rect = score_panel.get_rect(topleft=(10, 10))  # Position on top-left
            screen.blit(score_panel, score_panel_rect)

            font_size = int(window_size[1]/20)
            font = pygame.font.SysFont("Helvetica Bold.ttf", font_size)
            
            # Draw game information with shadow effect
            y_offset = 30  # Start from top
            texts = [
                f'Player: {username}',
                f'Stage: {stage}',
                f'Score: {score}',
                f'High Score: {current_high_score}'
            ]
            
            for text in texts:
                draw_text_with_shadow(screen, text, font, WHITE, 
                                    (20, y_offset))
                y_offset += 35

            pygame.display.flip()

            if any([bird_frame.colliderect(pf[0]) or bird_frame.colliderect(pf[1]) for pf in pipe_frames]):
                game_is_running = False

            if pipeSpawnTimer == 0:
                gap_position = random.randint(min_pipe_height, max_pipe_height - space_between_pipes)
                top = pipe_starting_template.copy()
                top.x = window_size[0]
                top.bottom = gap_position
                bottom = pipe_starting_template.copy()
                bottom.x = window_size[0]
                bottom.top = gap_position + space_between_pipes
                pipe_frames.append([top, bottom])

            pipeSpawnTimer += 1
            if pipeSpawnTimer >= time_between_pipe_spawn: 
                pipeSpawnTimer = 0

            if time.time() - game_clock >= 10:
                time_between_pipe_spawn = max(20, int(time_between_pipe_spawn * 5 / 6))
                stage += 1
                game_clock = time.time()

def check_highscore_beaten(score):
    high_scores = load_high_scores()
    if not high_scores:
        return True
    return score > high_scores[0]["score"]

def show_new_highscore_animation(score):
    font = pygame.font.SysFont("Helvetica Bold.ttf", 48)
    alpha = 0
    position = [window_size[0]//2, window_size[1]//3]
    
    for _ in range(60):  # Show animation for 60 frames
        # Create a new surface for the text
        text_surface = font.render("NEW HIGH SCORE!", True, (255, 255, 0))
        text_surface.set_alpha(abs(255 - alpha))
        text_rect = text_surface.get_rect(center=position)
        
        # Draw the text
        screen.blit(text_surface, text_rect)
        pygame.display.flip()
        
        # Update animation
        alpha = (alpha + 8) % 510  # Cycle between 0 and 510 for fade in/out effect
        position[1] += math.sin(alpha / 30) * 2  # Add slight floating effect
        
        pygame.time.wait(20)

def main():
    global score
    while True:
        # Show start screen and get username
        username = show_start_screen()
        
        # Show countdown
        show_countdown()
        
        # Start the game
        game_loop(username)
        
        # Check for new high score
        if check_highscore_beaten(score):
            show_new_highscore_animation(score)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        VID_CAP.release()
        cv.destroyAllWindows()
        pygame.quit()
        sys.exit()