import pygame
import random

# Initialize pygame
pygame.init()


SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
WHITE = (255, 255, 255)
PLAYER_SIZE = 60
CAR_WIDTH, CAR_HEIGHT = 80, 50
LANE_HEIGHT = 100

# Set up screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Endless Crossy Road")

# Load player image and resize
player_image = pygame.image.load("raccoon.png")
player_image = pygame.transform.scale(player_image, (PLAYER_SIZE, PLAYER_SIZE))
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - PLAYER_SIZE - 10]

# Load car images for different directions and resize
car_image_left = pygame.image.load("car.png")
car_image_left = pygame.transform.scale(car_image_left, (CAR_WIDTH, CAR_HEIGHT))
car_image_right = pygame.image.load("car2.png")
car_image_right = pygame.transform.scale(car_image_right, (CAR_WIDTH, CAR_HEIGHT))

# Cars setup
car_list = []
occupied_lanes = set()
car_speed_range = [5, 10]

# Score setup
score = 0
font = pygame.font.SysFont("Arial", 30)

# Game clock
clock = pygame.time.Clock()


def create_car():
    lane_y_positions = range(0, SCREEN_HEIGHT, LANE_HEIGHT)
    free_lanes = [y for y in lane_y_positions if y not in occupied_lanes]
    if not free_lanes:
        return  # No free lanes available, skip creating a new car

    y_pos = random.choice(free_lanes)
    occupied_lanes.add(y_pos)

    # Decide car direction
    x_pos = random.choice([0, SCREEN_WIDTH - CAR_WIDTH])
    speed = random.randint(car_speed_range[0], car_speed_range[1])
    if x_pos == 0:  # Moving from left to right
        speed = abs(speed)
        direction = "right"
    else:  # Moving from right to left
        speed = -abs(speed)
        direction = "left"

    return {"pos": [x_pos, y_pos], "speed": speed, "direction": direction}


def move_cars(car_list):
    global occupied_lanes
    for car in car_list:
        car["pos"][0] += car["speed"]

    car_list = [car for car in car_list if 0 <= car["pos"][0] <= SCREEN_WIDTH]
    occupied_lanes = {car["pos"][1] for car in car_list}
    return car_list

#px= playerx , py= playery, cx= carx, cy=cary
def detect_collision(player_pos, car_list):
    px, py = player_pos
    for car in car_list:
        cx, cy = car["pos"]
        if (px < cx + CAR_WIDTH and px + PLAYER_SIZE > cx) and (py < cy + CAR_HEIGHT and py + PLAYER_SIZE > cy):
            return True
    return False


# Game Loop
running = True
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_pos[1] -= 10
    if keys[pygame.K_DOWN] and player_pos[1] < SCREEN_HEIGHT - PLAYER_SIZE:
        player_pos[1] += 10
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= 10
    if keys[pygame.K_RIGHT] and player_pos[0] < SCREEN_WIDTH - PLAYER_SIZE:
        player_pos[0] += 10

    # Add new cars
    if random.randint(0, 20) < 1:
        new_car = create_car()
        if new_car:
            car_list.append(new_car)

    # Move and draw cars with different images based on direction
    car_list = move_cars(car_list)
    for car in car_list:
        if car["direction"] == "right":
            screen.blit(car_image_right, car["pos"])
        else:
            screen.blit(car_image_left, car["pos"])

    # Draw player using image
    screen.blit(player_image, player_pos)

    # Check collision
    if detect_collision(player_pos, car_list):
        running = False

    # Update score
    if player_pos[1] <= 0:
        score += 1
        player_pos[1] = SCREEN_HEIGHT - PLAYER_SIZE - 10
        car_speed_range[0] += 1
        car_speed_range[1] += 1

    # Display score
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # Update the screen
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
