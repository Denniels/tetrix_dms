"""Tetrix - Un juego tipo Tetris en tkinter.

Características:
- Pantalla de inicio con nombre del jugador y botón "Iniciar".
- 99 niveles de dificultad (nivel 1 = más fácil, nivel 99 = más difícil).
- Progreso: cada nivel requiere 1000 puntos para subir.
- Visualización de puntuación, nivel y progreso por nivel.
- Paleta colorida para cada tetrominó.
- Controles: flechas y WASD; Space para caída rápida.
- Botones clickables y activables con Enter/Space.
- Al perder: reintentar mismo nivel o comenzar desde cero.

Desarrollado por Daniel Mardones (desarrollador Python y gamer).
"""

import tkinter as tk
import random
import time

# --- Configuration ---
"""Tetrix - Un juego tipo Tetris en tkinter.

Características:
- Pantalla de inicio con nombre del jugador y botón "Iniciar".
- 99 niveles de dificultad (nivel 1 = más fácil, nivel 99 = más difícil).
- Progreso: cada nivel requiere 1000 puntos para subir.
- Visualización de puntuación, nivel y progreso por nivel.
- Paleta colorida para cada tetrominó.
- Controles: flechas y WASD; Space para caída rápida.
- Botones clickables y activables con Enter/Space.
- Al perder: reintentar mismo nivel o comenzar desde cero.

Desarrollado por Daniel Mardones (desarrollador Python y gamer).
"""

import tkinter as tk
import random

# --- Configuración ---
GRID_WIDTH = 10
GRID_HEIGHT = 20
DEFAULT_CELL_SIZE = 28
BOARD_COLOR = "#0b0620"
BG_COLOR = "#0f1724"
PALETTE = {
	'I': '#00f0f0',
	'J': '#0000f0',
	'L': '#f0a000',
	'O': '#f0f000',
	'S': '#00f000',
	'T': '#a000f0',
	'Z': '#f00000',
}

SHAPES = {
	'I': [[(0,1),(1,1),(2,1),(3,1)], [(2,0),(2,1),(2,2),(2,3)]],
	'J': [[(0,0),(0,1),(1,1),(2,1)], [(1,0),(2,0),(1,1),(1,2)], [(0,1),(1,1),(2,1),(2,2)], [(1,0),(1,1),(0,2),(1,2)]],
	'L': [[(2,0),(0,1),(1,1),(2,1)], [(1,0),(1,1),(1,2),(2,2)], [(0,1),(1,1),(2,1),(0,2)], [(0,0),(1,0),(1,1),(1,2)]],
	'O': [[(1,0),(2,0),(1,1),(2,1)]],
	'S': [[(1,0),(2,0),(0,1),(1,1)], [(1,0),(1,1),(2,1),(2,2)]],
	'T': [[(1,0),(0,1),(1,1),(2,1)], [(1,0),(1,1),(2,1),(1,2)], [(0,1),(1,1),(2,1),(1,2)], [(1,0),(0,1),(1,1),(1,2)]],
	'Z': [[(0,0),(1,0),(1,1),(2,1)], [(2,0),(1,1),(2,1),(1,2)]],
}


class Tetromino:
	def __init__(self, kind=None):
		self.kind = kind or random.choice(list(SHAPES.keys()))
		self.rot = 0
		self.blocks = SHAPES[self.kind]
		self.x = GRID_WIDTH // 2 - 2
		self.y = 0

	def shape(self):
		return self.blocks[self.rot % len(self.blocks)]

	def rotate(self):
		self.rot = (self.rot + 1) % len(self.blocks)

	def rotate_back(self):
		self.rot = (self.rot - 1) % len(self.blocks)


class Game:
	def __init__(self, root):
		self.root = root
		self.root.title('Tetrix')

		self.player = tk.StringVar(value='Jugador')
		self.level = 1
		self.score = 0
		self.level_points = 0
		self.running = False
		self.paused = False
		self.drop_interval = self.calc_interval()

		self.board = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
		self.current = None
		self.next_piece = Tetromino()

		# tamaño de celda actual (se ajusta al redimensionar)
		self.cell_size = DEFAULT_CELL_SIZE

		self._tick_id = None

		self._build_ui()
		self.update_score_labels()

	def calc_interval(self):
		# base 900ms, disminuye con el nivel; mínimo
		return max(60, 900 - (self.level - 1) * 8)

	def _build_ui(self):
		self.container = tk.Frame(self.root, bg=BG_COLOR, padx=8, pady=8)
		self.container.pack(fill='both', expand=True)

		# panel izquierdo: tablero
		left = tk.Frame(self.container, bg=BG_COLOR)
		left.pack(side='left', padx=8, fill='both', expand=True)

		# canvas principal: redimensionable
		self.canvas = tk.Canvas(left, width=GRID_WIDTH * DEFAULT_CELL_SIZE, height=GRID_HEIGHT * DEFAULT_CELL_SIZE, bg=BOARD_COLOR, highlightthickness=0)
		self.canvas.pack(fill='both', expand=True)
		self.canvas.bind('<Configure>', self.on_canvas_resize)

		# panel derecho: controles y score
		right = tk.Frame(self.container, bg=BG_COLOR)
		right.pack(side='right', fill='y', padx=8)

		tk.Label(right, text='Tetrix', bg=BG_COLOR, fg='white', font=('Helvetica', 18, 'bold')).pack(pady=(0,8))

		tk.Label(right, text='Jugador:', bg=BG_COLOR, fg='white').pack(anchor='w')
		self.name_entry = tk.Entry(right, textvariable=self.player)
		self.name_entry.pack(fill='x')

		self.start_btn = tk.Button(right, text='Iniciar', command=self.start_game, bg='#06b6d4')
		self.start_btn.pack(fill='x', pady=6)
		self.start_btn.bind('<Return>', lambda e: self.start_game())
		self.start_btn.bind('<space>', lambda e: self.start_game())

		self.pause_btn = tk.Button(right, text='Pausa', command=self.toggle_pause, bg='#f43f5e')
		self.pause_btn.pack(fill='x', pady=6)
		self.pause_btn.bind('<Return>', lambda e: self.toggle_pause())
		self.pause_btn.bind('<space>', lambda e: self.toggle_pause())

		self.reset_btn = tk.Button(right, text='Reiniciar (nivel 1)', command=self.reset_all, bg='#7c3aed')
		self.reset_btn.pack(fill='x', pady=6)
		self.reset_btn.bind('<Return>', lambda e: self.reset_all())
		self.reset_btn.bind('<space>', lambda e: self.reset_all())

		tk.Label(right, text='Puntuación:', bg=BG_COLOR, fg='white').pack(anchor='w', pady=(12,0))
		self.score_label = tk.Label(right, text='0', bg=BG_COLOR, fg='white', font=('Courier', 14))
		self.score_label.pack(anchor='w')

		tk.Label(right, text='Nivel:', bg=BG_COLOR, fg='white').pack(anchor='w', pady=(8,0))
		self.level_label = tk.Label(right, text=str(self.level), bg=BG_COLOR, fg='white', font=('Courier', 14))
		self.level_label.pack(anchor='w')

		tk.Label(right, text='Progreso (por nivel):', bg=BG_COLOR, fg='white').pack(anchor='w', pady=(8,0))
		self.progress_label = tk.Label(right, text=f'{self.level_points}/1000', bg=BG_COLOR, fg='white', font=('Courier', 12))
		self.progress_label.pack(anchor='w')

		tk.Label(right, text='Siguiente:', bg=BG_COLOR, fg='white').pack(anchor='w', pady=(12,0))
		self.next_canvas = tk.Canvas(right, width=4 * DEFAULT_CELL_SIZE, height=4 * DEFAULT_CELL_SIZE, bg=BG_COLOR, highlightthickness=0)
		self.next_canvas.pack()

		instr = "Usa ←/→ o A/D para mover, ↑ o W para rotar, ↓ o S para bajar, Space para caída rápida. Haz clic en los botones o presiona Enter/Space cuando tengan foco."
		tk.Label(right, text=instr, wraplength=220, bg=BG_COLOR, fg='white', justify='left').pack(pady=(12,0))

		# Bind controles (flechas + WASD)
		self.root.bind('<Left>', lambda e: self.move(-1))
		self.root.bind('<Right>', lambda e: self.move(1))
		self.root.bind('<Up>', lambda e: self.rotate())
		self.root.bind('<Down>', lambda e: self.soft_drop())
		self.root.bind('<space>', lambda e: self.hard_drop())
		self.root.bind('a', lambda e: self.move(-1))
		self.root.bind('d', lambda e: self.move(1))
		self.root.bind('w', lambda e: self.rotate())
		self.root.bind('s', lambda e: self.soft_drop())

		# Enter en canvas para iniciar
		self.canvas.bind('<Return>', lambda e: self.start_game())

		self.draw_grid()

	def update_score_labels(self):
		self.score_label.config(text=str(self.score))
		self.level_label.config(text=str(self.level))
		self.progress_label.config(text=f'{self.level_points}/1000')

	def draw_grid(self):
		"""Dibuja el tablero escalándolo según `self.cell_size`."""
		self.canvas.delete('all')
		cs = int(self.cell_size)
		for r in range(GRID_HEIGHT):
			for c in range(GRID_WIDTH):
				x1 = int(c * cs)
				y1 = int(r * cs)
				x2 = int(x1 + cs)
				y2 = int(y1 + cs)
				cell = self.board[r][c]
				color = cell if cell else BOARD_COLOR
				self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='#0b0b0b')

		# dibujar la pieza actual
		if self.current:
			for dx, dy in self.current.shape():
				x = self.current.x + dx
				y = self.current.y + dy
				if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
					x1 = int(x * cs)
					y1 = int(y * cs)
					x2 = int(x1 + cs)
					y2 = int(y1 + cs)
					self.canvas.create_rectangle(x1, y1, x2, y2, fill=PALETTE[self.current.kind], outline='#ffffff')

	def draw_next(self):
		self.next_canvas.delete('all')
		if not self.next_piece:
			return
		cs = max(8, int(self.cell_size))
		self.next_canvas.config(width=4 * cs, height=4 * cs)
		for dx, dy in self.next_piece.shape():
			x1 = int(dx * cs)
			y1 = int(dy * cs)
			x2 = int(x1 + cs)
			y2 = int(y1 + cs)
			self.next_canvas.create_rectangle(x1, y1, x2, y2, fill=PALETTE[self.next_piece.kind], outline='#000000')

	def spawn_piece(self):
		self.current = self.next_piece
		self.current.x = GRID_WIDTH // 2 - 2
		self.current.y = 0
		self.next_piece = Tetromino()
		self.draw_next()
		if self.check_collision(self.current, dx=0, dy=0):
			self.game_over()

	def check_collision(self, piece, dx=0, dy=0):
		for bx, by in piece.shape():
			x = piece.x + bx + dx
			y = piece.y + by + dy
			if x < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT:
				return True
			if y >= 0 and self.board[y][x]:
				return True
		return False

	def lock_piece(self):
		for bx, by in self.current.shape():
			x = self.current.x + bx
			y = self.current.y + by
			if 0 <= y < GRID_HEIGHT and 0 <= x < GRID_WIDTH:
				self.board[y][x] = PALETTE[self.current.kind]
		self.clear_lines()
		self.current = None

	def clear_lines(self):
		new_board = [row[:] for row in self.board]
		lines_cleared = 0
		to_remove = []
		for r in range(GRID_HEIGHT):
			if all(new_board[r][c] for c in range(GRID_WIDTH)):
				to_remove.append(r)

		for r in reversed(to_remove):
			del new_board[r]
			new_board.insert(0, [None for _ in range(GRID_WIDTH)])
			lines_cleared += 1

		self.board = new_board
		if lines_cleared > 0:
			gained = 100 * lines_cleared * self.level
			self.score += gained
			self.level_points += gained
			self.update_score_labels()
			self.check_level_up()

	def check_level_up(self):
		while self.level < 99 and self.level_points >= 1000:
			self.level_points -= 1000
			self.level += 1
			self.drop_interval = self.calc_interval()
			self.show_message(f'¡Nivel subido! Ahora: {self.level}', duration=800)
			self.update_score_labels()

	def show_message(self, text, duration=1000):
		x = GRID_WIDTH * self.cell_size / 2
		y = GRID_HEIGHT * self.cell_size / 2
		msg = self.canvas.create_text(x, y, text=text, fill='white', font=('Helvetica', 20, 'bold'))
		self.root.after(duration, lambda: self.canvas.delete(msg))

	def move(self, dir):
		if not self.running or self.paused or not self.current:
			return
		if not self.check_collision(self.current, dx=dir, dy=0):
			self.current.x += dir
			self.draw_grid()

	def rotate(self):
		if not self.running or self.paused or not self.current:
			return
		self.current.rotate()
		if self.check_collision(self.current, dx=0, dy=0):
			if not self.check_collision(self.current, dx=-1, dy=0):
				self.current.x -= 1
			elif not self.check_collision(self.current, dx=1, dy=0):
				self.current.x += 1
			else:
				self.current.rotate_back()
		self.draw_grid()

	def soft_drop(self):
		if not self.running or self.paused or not self.current:
			return
		if not self.check_collision(self.current, dx=0, dy=1):
			self.current.y += 1
			self.score += 1
			self.level_points += 1
			self.update_score_labels()
		else:
			self.lock_piece()
			self.spawn_piece()
		self.draw_grid()

	def hard_drop(self):
		if not self.running or self.paused or not self.current:
			return
		while not self.check_collision(self.current, dx=0, dy=1):
			self.current.y += 1
			self.score += 2
			self.level_points += 2
		self.lock_piece()
		self.spawn_piece()
		self.update_score_labels()
		self.draw_grid()

	def game_tick(self):
		if not self.running or self.paused:
			return
		if not self.current:
			self.spawn_piece()
		else:
			if not self.check_collision(self.current, dx=0, dy=1):
				self.current.y += 1
			else:
				self.lock_piece()
				self.spawn_piece()
		self.draw_grid()
		self._tick_id = self.root.after(self.drop_interval, self.game_tick)

	def start_game(self):
		# Iniciar nuevo juego en nivel 1
		if self.running:
			return
		self.level = 1
		self.score = 0
		self.level_points = 0
		self.board = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
		self.next_piece = Tetromino()
		self.current = None
		self.drop_interval = self.calc_interval()
		self.running = True
		self.paused = False
		self.update_score_labels()
		self.draw_grid()
		self.draw_next()
		self.root.focus()
		if self._tick_id:
			self.root.after_cancel(self._tick_id)
		self._tick_id = self.root.after(self.drop_interval, self.game_tick)

	def toggle_pause(self):
		if not self.running:
			return
		self.paused = not self.paused
		if not self.paused:
			self._tick_id = self.root.after(self.drop_interval, self.game_tick)
		else:
			if self._tick_id:
				self.root.after_cancel(self._tick_id)
				self._tick_id = None
		self.show_message('Pausado' if self.paused else 'Reanudado', duration=600)

	def reset_all(self):
		# reiniciar juego al nivel 1
		if self._tick_id:
			self.root.after_cancel(self._tick_id)
			self._tick_id = None
		self.level = 1
		self.score = 0
		self.level_points = 0
		self.board = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
		self.running = False
		self.paused = False
		self.current = None
		self.next_piece = Tetromino()
		self.drop_interval = self.calc_interval()
		self.update_score_labels()
		self.draw_grid()
		self.draw_next()

	def game_over(self):
		self.running = False
		if self._tick_id:
			self.root.after_cancel(self._tick_id)
			self._tick_id = None

		dlg = tk.Toplevel(self.root)
		dlg.title('Fin del juego')
		dlg.geometry('300x180')
		dlg.transient(self.root)
		tk.Label(dlg, text=f'¡Juego terminado, {self.player.get()}!', font=('Helvetica', 14)).pack(pady=8)
		tk.Label(dlg, text=f'Puntuación: {self.score}  Nivel alcanzado: {self.level}').pack(pady=4)

		def _retry():
			dlg.destroy()
			self.board = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
			# mantener nivel, reiniciar puntos
			self.score = 0
			self.level_points = 0
			self.running = True
			self.paused = False
			self.next_piece = Tetromino()
			self.current = None
			self.drop_interval = self.calc_interval()
			self.update_score_labels()
			self._tick_id = self.root.after(self.drop_interval, self.game_tick)

		def _restart_all():
			dlg.destroy()
			self.reset_all()

		b1 = tk.Button(dlg, text='Reintentar (mismo nivel)', command=_retry, bg='#06b6d4')
		b1.pack(fill='x', padx=16, pady=(8,4))
		b1.bind('<Return>', lambda e: _retry())
		b1.bind('<space>', lambda e: _retry())

		b2 = tk.Button(dlg, text='Comenzar desde nivel 1', command=_restart_all, bg='#7c3aed')
		b2.pack(fill='x', padx=16, pady=(0,8))
		b2.bind('<Return>', lambda e: _restart_all())
		b2.bind('<space>', lambda e: _restart_all())

	def on_canvas_resize(self, event):
		# actualizar tamaño de celda manteniendo la relación de aspecto del tablero
		w = max(10, event.width)
		h = max(10, event.height)
		self.cell_size = min(w / GRID_WIDTH, h / GRID_HEIGHT)
		self.draw_next()
		self.draw_grid()


def main():
	root = tk.Tk()
	app = Game(root)
	root.configure(bg=BG_COLOR)
	root.minsize(300, 400)
	root.mainloop()


if __name__ == '__main__':
	main()
