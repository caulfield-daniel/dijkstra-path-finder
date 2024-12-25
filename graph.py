import pygame
import random
import string
import heapq
from point import Point
from settings import *

class Graph:
    def __init__(self):
        self.points = []
        self.edges = {}
        self.shortest_path = []
        self.shortest_path_length = 0

    def generate_points(self):
        self.points = []
        letters = list(string.ascii_uppercase)
        for i in range(NUM_POINTS):
            new_point = Point(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 100), letters[i])
            if self.is_valid_point(new_point):
                self.points.append(new_point)
        self.generate_edges()
        self.print_graph()

    def is_valid_point(self, point):
        for p in self.points:
            if p.get_distance(point) < RADIUS * 2:
                return False
        return True

    def generate_edges(self):
        self.edges = {point: [] for point in self.points}
        for i in range(len(self.points)):
            for j in range(i + 1, len(self.points)):
                if random.random() < EDGE_PROB:
                    weight = random.randint(1, 10)
                    self.edges[self.points[i]].append((self.points[j], weight))
                    self.edges[self.points[j]].append((self.points[i], weight))

    def print_graph(self):
        graph_representation = {}
        for point, neighbors in self.edges.items():
            graph_representation[point.label] = [(neighbor.label, weight) for neighbor, weight in neighbors]
        print("Граф в виде словаря:")
        for point, connections in graph_representation.items():
            print(f"{point}: {connections}")

    def draw(self, screen):

        if self.shortest_path:
            for i in range(len(self.shortest_path) - 1):
                pygame.draw.line(screen, GREEN, (self.shortest_path[i].x, self.shortest_path[i].y), (self.shortest_path[i + 1].x, self.shortest_path[i + 1].y), 4)

        for point, neighbors in self.edges.items():
            for neighbor, weight in neighbors:
                pygame.draw.line(screen, GRAY, (point.x, point.y), (neighbor.x, neighbor.y), 2)
                mid_x = (point.x + neighbor.x) // 2
                mid_y = (point.y + neighbor.y) // 2
                font = pygame.font.Font(None, 24)
                text = font.render(f"{weight}", True, RED)
                text_rect = text.get_rect(center=(mid_x, mid_y))
                screen.blit(text, text_rect)

        if self.shortest_path:
            font = pygame.font.Font(None, 36)
            path_labels = ' -> '.join(point.label for point in self.shortest_path)
            text = font.render(f"Кратчайший путь: {path_labels} (Длина: {self.shortest_path_length})", True, BLACK)
            screen.blit(text, (20, 20))

        for point in self.points:
            point.draw(screen)


    def add_point(self, x, y):
        letters = list(string.ascii_uppercase)
        new_label = letters[len(self.points) % len(letters)]
        new_point = Point(x, y, new_label)
        if self.is_valid_point(new_point):
            self.points.append(new_point)
            self.generate_edges()
            self.print_graph()

    def select_point(self, pos):
        for point in self.points:
            if point.get_distance(Point(pos[0], pos[1], "")) < RADIUS:
                point.selected = not point.selected

   # Алгоритм Дейкстры
    def dijkstra(self, start, end):
        # Инициализация
        queue = []  # Очередь для хранения точек с их расстояниями
        distances = {point: float('inf') for point in self.points}  # Словарь для хранения минимальных расстояний до каждой точки (по умолчанию - inf)
        previous_points = {point: None for point in self.points}  # Словарь для хранения предыдущих точек на пути
        distances[start] = 0  # Расстояние до стартовой точки равно 0
        heapq.heappush(queue, (0, start.label))  # Добавляем стартовую точку в очередь с расстоянием 0

        # Пока в очереди содержатся точки
        while queue:
            current_distance, current_label = heapq.heappop(queue)  # Извлекаем точку с наименьшим расстоянием
            current_point = next(point for point in self.points if point.label == current_label)  # Находим соответствующую точку

            if current_distance > distances[current_point]:
                continue  # Пропускаем итерацию, если расстояние не минимально

            for neighbor, weight in self.edges[current_point]:  # Проходим по всем соседям текущей точки
                distance = current_distance + weight  # Вычисляем новое расстояние до соседа

                # Если новое расстояние меньше известного, обновляем значения
                if distance < distances[neighbor]:  # Если найдено более короткое расстояние
                    distances[neighbor] = distance  # Обновляем минимальное расстояние до соседа
                    previous_points[neighbor] = current_point  # Запоминаем текущую точку как предыдущую для соседа
                    heapq.heappush(queue, (distance, neighbor.label))  # Добавляем соседа в очередь с обновленным расстоянием

        path = []  # Список для хранения найденного пути
        current = end  # Начинаем с конечной точки
        while current is not None:  # Пока есть предыдущая точка
            path.append(current)  # Добавляем текущую точку в путь
            current = previous_points[current]  # Переходим к предыдущей точке
        path.reverse()  # Разворачиваем путь, чтобы получить его от начала до конца

        self.shortest_path_length = distances[end]  # Сохраняем длину кратчайшего пути
        return path  # Возвращаем найденный путь

    def reset_selection(self):
        for point in self.points:
            point.selected = False
        self.shortest_path = []
        self.shortest_path_length = 0
