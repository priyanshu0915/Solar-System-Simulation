import pygame
import math
pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

FONT = pygame.font.SysFont("comicsans", 16)
#class named planet 
class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 250 / AU  # 1AU = 100 pixels
    TIMESTEP = 3600 * 24  # 1 day

    def __init__(self, x, y, radius, color, mass, name):#function to give initial values to different paramter
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.name = name

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):#scaling 
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (x, y), self.radius)

        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))

        # Display the planet name
        name_text = FONT.render(self.name, 1, WHITE)
        win.blit(name_text, (x - name_text.get_width()/2, y + self.radius + 5))  # Adjust the vertical position

    def attraction(self, other):#calcultion of attraction force
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

def main():
    run = True
    clock = pygame.time.Clock()
    
    sun = Planet(0, 0, 30, (255, 255, 0), 1.98892 * 10**30, "sun")
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, (100, 149, 237), 5.9742 * 10**24, "earth")
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, (188, 39, 50), 6.39 * 10**23, "mars")
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8, (80, 78, 81), 3.30 * 10**23, "mercury")
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, (255, 255, 255), 4.8685 * 10**24, "venus")
    venus.y_vel = -35.02 * 1000

    jupiter = Planet(-5.203 * Planet.AU, 0, 24, (255, 165, 0), 1.898 * 10**27, "jupiter")
    jupiter.y_vel = 5.0 * 1000

    saturn = Planet(-9.582 * Planet.AU, 0, 22, (255, 215, 0), 5.683 * 10**26, "saturn")
    saturn.y_vel = 4.0 * 1000

    uranus = Planet(-19.22 * Planet.AU, 0, 18, (135, 206, 250), 8.681 * 10**25, "uranus")
    uranus.y_vel = 3.0 * 1000

    neptune = Planet(-30.05 * Planet.AU, 0, 16, (0, 0, 139), 1.024 * 10**26, "neptune")
    neptune.y_vel = 2.0 * 1000

    planets = [sun, earth, mars, mercury, venus, jupiter, saturn, uranus, neptune]

    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN) 

        pygame.display.update()
    pygame.quit()

main()
