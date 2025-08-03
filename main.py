from browser import document, html, timer, bind
import random

GAME_WIDTH = 800
GAME_HEIGHT = 800
SPEED = 80  # ms per frame
SPACE_SIZE = 25
BODY_PARTS = 5
SNAKE_COLOR = "#FF0000"
FOOD_COLOR = "#FFFF00"
BACKGROUND_COLOR = "#000000"

canvas = document["game-canvas"]
ctx = canvas.getContext("2d")
score = 0
direction = "down"
game_running = False
snake = []
food = None
move_timer = None

def draw_rect(x, y, color):
    ctx.fillStyle = color
    ctx.fillRect(x, y, SPACE_SIZE, SPACE_SIZE)

def draw_oval(x, y, color):
    ctx.beginPath()
    ctx.arc(x + SPACE_SIZE/2, y + SPACE_SIZE/2, SPACE_SIZE/2, 0, 2*3.14159)
    ctx.fillStyle = color
    ctx.fill()
    ctx.closePath()

def draw_snake():
    for part in snake:
        draw_rect(part[0], part[1], SNAKE_COLOR)

def draw_food():
    draw_oval(food[0], food[1], FOOD_COLOR)

def place_food():
    while True:
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        if [x, y] not in snake:
            return [x, y]

def reset_game(ev=None):
    global snake, food, direction, score, game_running, move_timer
    if move_timer:
        timer.clear_interval(move_timer)
    ctx.clearRect(0, 0, GAME_WIDTH, GAME_HEIGHT)
    direction = "down"
    score = 0
    document["score"].text = f"Score: {score}"
    snake = [[0, 0] for _ in range(BODY_PARTS)]
    food = place_food()
    game_running = True
    draw()
    move_timer = timer.set_interval(next_turn, SPEED)

def draw():
    ctx.fillStyle = BACKGROUND_COLOR
    ctx.fillRect(0, 0, GAME_WIDTH, GAME_HEIGHT)
    draw_snake()
    draw_food()

def next_turn():
    global food, score, game_running, move_timer
    if not game_running:
        return
    x, y = snake[0]
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE
    new_head = [x, y]
    if (x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT or new_head in snake):
        game_over()
        return
    snake.insert(0, new_head)
    if new_head == food:
        score += 1
        document["score"].text = f"Score: {score}"
        food = place_food()
    else:
        snake.pop()
    draw()

def game_over():
    global game_running, move_timer
    game_running = False
    if move_timer:
        timer.clear_interval(move_timer)
    ctx.fillStyle = "red"
    ctx.font = "70px consolas"
    ctx.textAlign = "center"
    ctx.fillText("GAME OVER", GAME_WIDTH // 2, GAME_HEIGHT // 2)

@bind(document, "keydown")
def on_keydown(ev):
    global direction
    if not game_running:
        return
    key = ev.key
    if key in ("ArrowUp", "w") and direction != "down":
        direction = "up"
    elif key in ("ArrowDown", "s") and direction != "up":
        direction = "down"
    elif key in ("ArrowLeft", "a") and direction != "right":
        direction = "left"
    elif key in ("ArrowRight", "d") and direction != "left":
        direction = "right"

document["start-btn"].bind("click", reset_game)