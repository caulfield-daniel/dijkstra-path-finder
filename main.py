import pygame
from graph import Graph
from settings import *


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Алгоритм Дейкстры")
    clock = pygame.time.Clock()

    graph = Graph()
    graph.generate_points()
    running = True

    while running:
        screen.fill(WHITE)

        graph.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:  # ПКМ
                    x, y = event.pos
                    graph.add_point(x, y)
                elif event.button == 1:  # Левый клик мыши
                    x, y = event.pos
                    graph.select_point((x, y))

                    selected_points = [
                        point for point in graph.points if point.selected
                    ]
                    if len(selected_points) == 2:
                        start, end = selected_points
                        path = graph.dijkstra(start, end)
                        graph.shortest_path = path
                        print(
                            f"Кратчайший путь от {start.label} до {end.label}: {[point.label for point in path]} с расстоянием {graph.shortest_path_length}"
                        )

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:  # Генерация нового графа
                    graph.generate_points()
                    graph.reset_selection()
                elif event.key == pygame.K_r:  # Сброс выбранных точек
                    graph.reset_selection()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
