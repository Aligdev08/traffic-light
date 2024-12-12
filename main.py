import pygame
from typing import Any, List
from datetime import datetime

game_surface = pygame.display.set_mode([500, 500])

running = True
fps = 60

fpsClock = pygame.time.Clock()


class Colour:
    def __init__(self, red: int, green: int, blue: int):
        self.red = red
        self.green = green
        self.blue = blue

    def to_tuple(self) -> tuple[int, int, int]:
        return self.red, self.green, self.blue

    def shadow(self) -> 'Colour':
        shadow_red = max(0, int(self.red * 0.5))
        shadow_green = max(0, int(self.green * 0.5))
        shadow_blue = max(0, int(self.blue * 0.5))
        return Colour(shadow_red, shadow_green, shadow_blue)


Red = Colour(255, 0, 0)
Orange = Colour(255, 125, 0)
Green = Colour(0, 255, 0)
Gray = Colour(130, 130, 130)


class Circle:
    def __init__(self, fill: Colour, radius: float, centre: tuple[int, int], surface: pygame.Surface, border: int = 0,
                 border_colour: Colour = None):
        self.fill = fill
        self.radius = radius
        self.centre = centre
        self.surface = surface
        self.border = border
        self.border_colour = border_colour if border_colour is not None else Colour(0, 0, 0)

    def draw(self):
        pygame.draw.circle(self.surface, self.fill.to_tuple(), self.centre, self.radius)

        if self.border > 0:
            pygame.draw.circle(self.surface, self.border_colour.to_tuple(), self.centre, self.radius - self.border)

    def point_intersect(self, position: tuple[int, int]):
        x, y = position
        a, b = self.centre
        equation = (x - a) ** 2 + (y - b) ** 2
        return equation <= self.radius ** 2

    def set_fill(self, fill: Colour):
        self.fill = fill


class Queue:
    def __init__(self, length: int):
        self.length = length
        self.elements: List[Any] = []

    def __str__(self) -> str:
        return f"Queue({self.elements})"

    def check_is_full(self) -> bool:
        return len(self.elements) >= self.length

    def check_is_empty(self) -> bool:
        return len(self.elements) == 0

    def enqueue(self, value: Any) -> str:
        if self.check_is_full():
            return "Queue is full."
        self.elements.append(value)
        return f"Enqueued {value}"

    def dequeue(self) -> Any:
        if self.check_is_empty():
            raise "Queue is empty."
        return self.elements.pop(0)

    def get_front_pointer(self) -> Any:
        return self.elements[self.length - 1]


class Sequence:
    def __init__(self, lights: list):
        self.red_light = lights[0]
        self.orange_light = lights[1]
        self.green_light = lights[2]
        self.queue = Queue(4)
        self.running = False
        self.next_stage = datetime.now().timestamp()

    def stage_one(self):
        if self.red_light.fill != Red:
            self.red_light.set_fill(Red)
        if self.orange_light.fill != Gray:
            self.orange_light.set_fill(Gray)
        if self.green_light.fill != Gray:
            self.green_light.set_fill(Gray)

    def stage_two(self):
        if self.red_light.fill != Red:
            self.red_light.set_fill(Red)
        if self.orange_light.fill != Orange:
            self.orange_light.set_fill(Orange)
        if self.green_light.fill != Gray:
            self.green_light.set_fill(Gray)

    def stage_three(self):
        if self.red_light.fill != Gray:
            self.red_light.set_fill(Gray)
        if self.orange_light.fill != Gray:
            self.orange_light.set_fill(Gray)
        if self.green_light.fill != Green:
            self.green_light.set_fill(Green)

    def stage_four(self):
        if self.red_light.fill != Gray:
            self.red_light.set_fill(Gray)
        if self.orange_light.fill != Orange:
            self.orange_light.set_fill(Orange)
        if self.green_light.fill != Gray:
            self.green_light.set_fill(Gray)

    def start(self):
        self.running = True
        while not self.queue.check_is_full():
            self.queue.enqueue(self.stage_one)
            self.queue.enqueue(self.stage_two)
            self.queue.enqueue(self.stage_three)
            self.queue.enqueue(self.stage_four)

    def process(self):
        while self.running and not self.queue.check_is_empty() and self.next_stage < datetime.now().timestamp():
            stage = self.queue.dequeue()
            stage()
            self.next_stage = datetime.now().timestamp() + 1


red_light = Circle(
    fill=Gray,
    radius=50.0,
    centre=(250, 100),
    surface=game_surface
)

orange_light = Circle(
    fill=Gray,
    radius=50.0,
    centre=(250, 250),
    surface=game_surface
)

green_light = Circle(
    fill=Gray,
    radius=50.0,
    centre=(250, 400),
    surface=game_surface
)

traffic_lights = [
    red_light,
    orange_light,
    green_light
]

sequence = Sequence(traffic_lights)

while running:
    game_surface.fill((55, 55, 55))

    for light in traffic_lights:
        light.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            sequence.start()

    sequence.process()

    pygame.display.flip()
    fpsClock.tick(fps)
