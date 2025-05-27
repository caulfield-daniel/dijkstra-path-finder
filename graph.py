import pygame
import random
import string
import heapq
from point import Point
from settings import *


class Graph:
    """
    Класс, представляющий граф, состоящий из точек и ребер.
    """

    def __init__(self):
        """
        Инициализация графа.
        """
        self.points = []
        self.edges = {}
        self.shortest_path = []
        self.shortest_path_length = 0

    def generate_points(self):
        """
        Генерация случайных точек на графе.
        """
        self.points = []
        letters = list(string.ascii_uppercase)
        for i in range(NUM_POINTS):
            new_point = Point(
                random.randint(50, WIDTH - 50),
                random.randint(50, HEIGHT - 100),
                letters[i],
            )
            if self.is_valid_point(new_point):
                self.points.append(new_point)
        self.generate_edges()
        self.print_graph()

    def is_valid_point(self, point):
        """
        Проверка, является ли точка допустимой для добавления на граф.
        """
        for p in self.points:
            if p.get_distance(point) < RADIUS * 2:
                return False
        return True

    def generate_edges(self):
        """
        Генерация случайных ребер между точками на графе.
        """
        self.edges = {point: [] for point in self.points}
        for i in range(len(self.points)):
            for j in range(i + 1, len(self.points)):
                if random.random() < EDGE_PROB:
                    weight = random.randint(1, 10)
                    self.edges[self.points[i]].append((self.points[j], weight))
                    self.edges[self.points[j]].append((self.points[i], weight))

    def print_graph(self):
        """
        Вывод графа в виде словаря.
        """
        graph_representation = {}
        for point, neighbors in self.edges.items():
            graph_representation[point.label] = [
                (neighbor.label, weight) for neighbor, weight in neighbors
            ]
        print("Граф в виде словаря:")
        for point, connections in graph_representation.items():
            print(f"{point}: {connections}")

    def draw(self, screen):
        """
        Рисование графа на экране.
        """
        if self.shortest_path:
            for i in range(len(self.shortest_path) - 1):
                pygame.draw.line(
                    screen,
                    GREEN,
                    (self.shortest_path[i].x, self.shortest_path[i].y),
                    (self.shortest_path[i + 1].x, self.shortest_path[i + 1].y),
                    4,
                )

        for point, neighbors in self.edges.items():
            for neighbor, weight in neighbors:
                pygame.draw.line(
                    screen, GRAY, (point.x, point.y), (neighbor.x, neighbor.y), 2
                )
                mid_x = (point.x + neighbor.x) // 2
                mid_y = (point.y + neighbor.y) // 2
                font = pygame.font.Font(None, 24)
                text = font.render(f"{weight}", True, RED)
                text_rect = text.get_rect(center=(mid_x, mid_y))
                screen.blit(text, text_rect)

        if self.shortest_path:
            font = pygame.font.Font(None, 36)
            path_labels = " -> ".join(point.label for point in self.shortest_path)
            text = font.render(
                f"Кратчайший путь: {path_labels} (Длина: {self.shortest_path_length})",
                True,
                BLACK,
            )
            screen.blit(text, (20, 20))

        for point in self.points:
            point.draw(screen)

    def add_point(self, x, y):
        """
        Добавление новой точки на граф.
        """
        letters = list(string.ascii_uppercase)
        new_label = letters[len(self.points) % len(letters)]
        new_point = Point(x, y, new_label)
        if self.is_valid_point(new_point):
            self.points.append(new_point)
            self.generate_edges()
            self.print_graph()

    def select_point(self, pos):
        """
        Выбор точки на графе по позиции.
        """
        for point in self.points:
            if point.get_distance(Point(pos[0], pos[1], "")) < RADIUS:
                point.selected = not point.selected

    def dijkstra(self, start, end):
        """
        Алгоритм Дейкстры для поиска кратчайшего пути между двумя точками на графе.
        """
        queue = []
        distances = {point: float("inf") for point in self.points}
        previous_points = {point: None for point in self.points}
        distances[start] = 0
        heapq.heappush(queue, (0, start.label))

        while queue:
            current_distance, current_label = heapq.heappop(queue)
            current_point = next(
                point for point in self.points if point.label == current_label
            )

            if current_distance > distances[current_point]:
                continue

            for neighbor, weight in self.edges[current_point]:
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_points[neighbor] = current_point
                    heapq.heappush(queue, (distance, neighbor.label))

        path = []
        current = end
        while current is not None:
            path.append(current)
            current = previous_points[current]
        path.reverse()

        self.shortest_path_length = distances[end]
        return path

    def reset_selection(self):
        """
        Сброс выделения точек и кратчайшего пути.
        """
        for point in self.points:
            point.selected = False
        self.shortest_path = []
        self.shortest_path_length = 0
