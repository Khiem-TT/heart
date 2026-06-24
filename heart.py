# -*- coding: utf-8 -*-
"""
Trái tim particle đập - tkinter (kiểu "爱心表白代码" trên Bilibili/TikTok).
Chạy: python heart.py   (chỉ cần Python, tkinter có sẵn)
"""
import random
import math
import tkinter as tk

CANVAS_W = 640
CANVAS_H = 640
CENTER_X = CANVAS_W / 2
CENTER_Y = CANVAS_H / 2

IMAGE_ENLARGE = 11
HEART_COLOR = "#ff2d6b"


def heart_function(t, shrink_ratio=IMAGE_ENLARGE):
    """Phương trình đường cong trái tim."""
    x = 16 * (math.sin(t) ** 3)
    y = -(13 * math.cos(t) - 5 * math.cos(2 * t)
          - 2 * math.cos(3 * t) - math.cos(4 * t))
    x *= shrink_ratio
    y *= shrink_ratio
    x += CENTER_X
    y += CENTER_Y
    return int(x), int(y)


def scatter_inside(x, y, beta=0.15):
    """Đẩy điểm vào trong tim để lấp đầy."""
    ratio_x = -beta * math.log(random.random())
    ratio_y = -beta * math.log(random.random())
    dx = ratio_x * (x - CENTER_X)
    dy = ratio_y * (y - CENTER_Y)
    return x - dx, y - dy


def shrink(x, y, ratio):
    """Co/giãn tạo viền lung linh."""
    force = -1 / (((x - CENTER_X) ** 2 + (y - CENTER_Y) ** 2) ** 0.6)
    dx = ratio * force * (x - CENTER_X)
    dy = ratio * force * (y - CENTER_Y)
    return x - dx, y - dy


def curve(p):
    """Hàm nhịp đập (mượt)."""
    return 2 * (2 * math.sin(4 * p)) / (2 * math.pi)


class Heart:
    def __init__(self, generate_frame=20):
        self._points = set()          # điểm viền gốc
        self._edge_diffusion_points = set()
        self._center_diffusion_points = set()
        self.all_points = {}          # các frame dựng sẵn
        self.build(2000)
        self.random_halo = 1000
        self.generate_frame = generate_frame
        for frame in range(generate_frame):
            self.calc(frame)

    def build(self, number):
        # viền tim
        for _ in range(number):
            t = random.uniform(0, 2 * math.pi)
            x, y = heart_function(t)
            self._points.add((x, y))
        # khuếch tán từ viền ra ngoài
        for _x, _y in list(self._points):
            for _ in range(3):
                x, y = scatter_inside(_x, _y, 0.05)
                self._edge_diffusion_points.add((x, y))
        # lấp đầy bên trong
        point_list = list(self._points)
        for _ in range(4000):
            x, y = random.choice(point_list)
            x, y = scatter_inside(x, y, 0.17)
            self._center_diffusion_points.add((x, y))

    @staticmethod
    def calc_position(x, y, ratio):
        force = 1 / (((x - CENTER_X) ** 2 + (y - CENTER_Y) ** 2) ** 0.520)
        dx = ratio * force * (x - CENTER_X) + random.randint(-1, 1)
        dy = ratio * force * (y - CENTER_Y) + random.randint(-1, 1)
        return x - dx, y - dy

    def calc(self, generate_frame):
        ratio = 10 * curve(generate_frame / 10 * math.pi)
        halo_radius = int(4 + 6 * (1 + curve(generate_frame / 10 * math.pi)))
        halo_number = int(3000 + 4000 * abs(curve(generate_frame / 10 * math.pi) ** 2))

        all_points = []

        # hào quang
        heart_halo_point = set()
        for _ in range(halo_number):
            t = random.uniform(0, 2 * math.pi)
            x, y = heart_function(t, shrink_ratio=11.6)
            x, y = shrink(x, y, halo_radius)
            if (x, y) not in heart_halo_point:
                heart_halo_point.add((x, y))
                x += random.randint(-14, 14)
                y += random.randint(-14, 14)
                size = random.choice((1, 2, 2))
                all_points.append((x, y, size))

        # viền tim
        for x, y in self._points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 3)
            all_points.append((x, y, size))

        # khuếch tán
        for x, y in self._edge_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))
        for x, y in self._center_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))

        self.all_points[generate_frame] = all_points

    def render(self, render_canvas, render_frame):
        for x, y, size in self.all_points[render_frame % self.generate_frame]:
            render_canvas.create_rectangle(
                x, y, x + size, y + size, width=0, fill=HEART_COLOR)


def draw(main, render_canvas, render_heart, frame=0):
    render_canvas.delete("all")
    render_heart.render(render_canvas, frame)
    main.after(160, draw, main, render_canvas, render_heart, frame + 1)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("I Love You")
    canvas = tk.Canvas(root, bg="black", height=CANVAS_H, width=CANVAS_W)
    canvas.pack()
    heart = Heart()
    draw(root, canvas, heart)
    root.mainloop()
