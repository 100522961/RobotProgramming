import math
import random

import pygame


WIDTH = 960
HEIGHT = 640
CYAN = (82, 235, 255)
WHITE = (235, 248, 255)
MUTED = (137, 173, 196)


class PulseRun:
	def __init__(self):
		pygame.init()
		pygame.display.set_caption("PULSE RUN")
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		self.clock = pygame.time.Clock()
		self.title_font = pygame.font.SysFont("dejavusans", 76, bold=True)
		self.heading_font = pygame.font.SysFont("dejavusans", 32, bold=True)
		self.body_font = pygame.font.SysFont("dejavusans", 18)
		self.small_font = pygame.font.SysFont("dejavusans", 14, bold=True)
		self.background = self.make_background()
		self.stars = [
			(random.randrange(WIDTH), random.randrange(HEIGHT), random.random() * 6.3)
			for _ in range(75)
		]
		self.state = "welcome"
		self.running = True

	def make_background(self):
		background = pygame.Surface((WIDTH, HEIGHT))
		for y in range(HEIGHT):
			blend = y / HEIGHT
			color = (7 + int(5 * blend), 15 + int(13 * blend), 34 + int(20 * blend))
			pygame.draw.line(background, color, (0, y), (WIDTH, y))
		return background

	def start_game(self):
		self.player = pygame.Vector2(WIDTH / 2, HEIGHT * 0.72)
		self.drones = [pygame.Vector2(145, 160), pygame.Vector2(810, 370)]
		self.cores = [self.random_core(), self.random_core()]
		self.score = 0
		self.lives = 3
		self.invulnerable = 0
		self.state = "playing"

	def random_core(self):
		return pygame.Vector2(random.randrange(70, WIDTH - 70), random.randrange(125, HEIGHT - 70))

	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.running = False
				elif self.state == "welcome":
					self.start_game()
				elif self.state == "game_over":
					self.start_game()

	def update(self, delta):
		keys = pygame.key.get_pressed()
		direction = pygame.Vector2(
			int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a]),
			int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w]),
		)
		if direction.length_squared():
			direction = direction.normalize()
		self.player += direction * 285 * delta
		self.player.x = max(32, min(WIDTH - 32, self.player.x))
		self.player.y = max(96, min(HEIGHT - 32, self.player.y))
		self.invulnerable = max(0, self.invulnerable - delta)

		for core in self.cores:
			if self.player.distance_to(core) < 32:
				self.score += 1
				core.update(self.random_core())

		for index, drone in enumerate(self.drones):
			to_player = self.player - drone
			if to_player.length_squared():
				drone += to_player.normalize() * (68 + min(self.score * 2, 55)) * delta
			if self.invulnerable == 0 and self.player.distance_to(drone) < 34:
				self.lives -= 1
				self.invulnerable = 1.5
				drone.update((45, 125) if index == 0 else (WIDTH - 45, HEIGHT - 80))
				if self.lives <= 0:
					self.state = "game_over"
					return

	def draw_text(self, text, font, color, center):
		image = font.render(text, True, color)
		self.screen.blit(image, image.get_rect(center=center))

	def draw_background(self, time):
		self.screen.blit(self.background, (0, 0))
		for x in range(0, WIDTH, 48):
			pygame.draw.line(self.screen, (15, 34, 55), (x, 80), (x, HEIGHT))
		for y in range(96, HEIGHT, 48):
			pygame.draw.line(self.screen, (15, 34, 55), (0, y), (WIDTH, y))
		for x, y, phase in self.stars:
			brightness = 95 + int(80 * (0.5 + 0.5 * math.sin(time * 1.6 + phase)))
			pygame.draw.circle(self.screen, (brightness, brightness + 20, min(255, brightness + 45)), (x, y), 1)

	def draw_player(self, time):
		x, y = round(self.player.x), round(self.player.y)
		pygame.draw.circle(self.screen, (15, 75, 94), (x, y), 31)
		pygame.draw.circle(self.screen, (30, 148, 164), (x, y), 23, 2)
		pygame.draw.circle(self.screen, CYAN, (x, y), 15)
		pygame.draw.rect(self.screen, (12, 38, 57), (x - 10, y - 8, 20, 16), border_radius=5)
		pygame.draw.rect(self.screen, WHITE, (x - 5, y - 4, 10, 8), border_radius=3)
		pulse = 34 + int(3 * math.sin(time * 5))
		pygame.draw.circle(self.screen, (33, 117, 141), (x, y), pulse, 1)

	def draw_drone(self, drone, time):
		x, y = round(drone.x), round(drone.y)
		pygame.draw.circle(self.screen, (73, 34, 62), (x, y), 25)
		pygame.draw.circle(self.screen, (230, 93, 133), (x, y), 19, 2)
		pygame.draw.circle(self.screen, (29, 24, 47), (x, y), 13)
		eye_offset = int(2 * math.sin(time * 5))
		pygame.draw.circle(self.screen, (255, 119, 160), (x + eye_offset, y), 5)

	def draw_core(self, core, time):
		x, y = core.x, core.y
		angle = time * 1.8
		points = []
		for index in range(4):
			theta = angle + index * math.pi / 2
			points.append((x + math.cos(theta) * 12, y + math.sin(theta) * 12))
		pygame.draw.circle(self.screen, (24, 82, 99), (round(x), round(y)), 23)
		pygame.draw.polygon(self.screen, CYAN, points)
		pygame.draw.polygon(self.screen, WHITE, points, 2)

	def draw_hud(self):
		pygame.draw.rect(self.screen, (8, 19, 37), (0, 0, WIDTH, 78))
		pygame.draw.line(self.screen, (35, 97, 119), (0, 77), (WIDTH, 77), 2)
		self.draw_text("PULSE RUN", self.small_font, CYAN, (105, 28))
		self.draw_text(f"CORES  {self.score:02d}", self.body_font, WHITE, (WIDTH // 2, 30))
		self.draw_text("LIVES", self.small_font, MUTED, (WIDTH - 126, 28))
		for index in range(self.lives):
			pygame.draw.circle(self.screen, (255, 108, 151), (WIDTH - 78 + index * 21, 51), 6)
		self.draw_text("WASD / ARROWS TO MOVE     ESC TO QUIT", self.small_font, MUTED, (WIDTH // 2, HEIGHT - 18))

	def draw_welcome(self, time):
		self.draw_text("ARCADE / 01", self.small_font, CYAN, (WIDTH // 2, 178))
		self.draw_text("PULSE", self.title_font, WHITE, (WIDTH // 2, 263))
		self.draw_text("RUN", self.title_font, CYAN, (WIDTH // 2, 339))
		self.draw_text("Recover the cores. Keep clear of the drones.", self.body_font, MUTED, (WIDTH // 2, 407))
		if int(time * 2) % 2 == 0:
			self.draw_text("PRESS ANY KEY TO START", self.body_font, WHITE, (WIDTH // 2, 490))
		self.draw_text("MOVE  WASD / ARROWS      QUIT  ESC", self.small_font, MUTED, (WIDTH // 2, 558))
		pygame.draw.line(self.screen, (33, 105, 129), (WIDTH // 2 - 90, 449), (WIDTH // 2 + 90, 449), 1)

	def draw_game_over(self):
		overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
		overlay.fill((4, 9, 22, 205))
		self.screen.blit(overlay, (0, 0))
		self.draw_text("RUN COMPLETE", self.heading_font, WHITE, (WIDTH // 2, 250))
		self.draw_text(f"CORES RECOVERED  {self.score:02d}", self.body_font, CYAN, (WIDTH // 2, 310))
		self.draw_text("PRESS ANY KEY TO PLAY AGAIN", self.body_font, MUTED, (WIDTH // 2, 380))

	def draw(self, time):
		self.draw_background(time)
		if self.state == "welcome":
			self.draw_welcome(time)
		else:
			for core in self.cores:
				self.draw_core(core, time)
			for drone in self.drones:
				self.draw_drone(drone, time)
			if self.state == "playing" and (self.invulnerable == 0 or int(self.invulnerable * 12) % 2 == 0):
				self.draw_player(time)
			self.draw_hud()
			if self.state == "game_over":
				self.draw_game_over()
		pygame.display.flip()

	def run(self):
		elapsed = 0
		while self.running:
			delta = min(self.clock.tick(60) / 1000, 0.05)
			elapsed += delta
			self.handle_events()
			if self.state == "playing":
				self.update(delta)
			self.draw(elapsed)
		pygame.quit()


if __name__ == "__main__":
	PulseRun().run()
