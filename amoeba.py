import random
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numpy import arange, array


# nosocheklubitchelovechka #nosokichelovek #lubov #podnosoktozhenosok

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __abs__(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, Vector):
            return self.x * other.y - self.y * other.x
        else:
            return Vector(self.x * other, self.y * other)

    def __repr__(self):
        return f'({self.x}, {self.y})'


def func(v):
    x = v.x
    y = v.y
    try:
        return -math.sqrt(1 - (x - 1.5) ** 2 - (y - 1.5) ** 2) + 2
    except ValueError:
        return 2


class Amoeba:
    def __init__(self, f, x_range, y_range, eps=0.0001):
        self.f = f
        self.eps = eps
        self.x_range = x_range
        self.y_range = y_range
        self.vertexes = [
            Vector(random.uniform(x_range[0], x_range[1]), random.uniform(y_range[0], y_range[1])),
            Vector(random.uniform(x_range[0], x_range[1]), random.uniform(y_range[0], y_range[1])),
            Vector(random.uniform(x_range[0], x_range[1]), random.uniform(y_range[0], y_range[1]))
        ]

        self.sort()

    def next(self):
        self.sort()
        f = self.f

        h, h_, k = self.vertexes
        m = (k + h_) * 0.5
        n = m + (m - h)

        if f(n) < f(h_):
            n_ = m + (m - h) * 2
            if f(n_) < f(h_):
                h = n_
            else:
                h = n
        elif f(n) > f(h_):
            n__ = m - (m - h) * 0.5
            if f(n__) < f(h_):
                h = n__
            else:
                h = k + (h - k) * 0.5
                h_ = k + (h_ - k) * 0.5
        plot_2d(self.x_range, self.y_range, points=[h, h_, k])
        self.vertexes = [h, h_, k]

    def find_min(self):
        while self.area() > self.eps:
            self.next()
        return self.vertexes[-1]

    def sort(self):
        self.vertexes = sorted(self.vertexes, key=self.f, reverse=True)

    def area(self):
        return abs((self.vertexes[1] - self.vertexes[0]) * (self.vertexes[2] - self.vertexes[0])) * 0.5


def plot_2d(x_range, y_range, points=None):
    xs = [p.x for p in points]
    ys = [p.y for p in points]

    plt.scatter(xs, ys)
    plt.axis([x_range[0], x_range[1], y_range[0], y_range[1]])
    plt.grid(True)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()


def plot_3d(f, x_range, y_range, points=None):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    xs_ = arange(x_range[0], x_range[1], 0.1)
    ys_ = arange(y_range[0], y_range[1], 0.1)

    xs, ys, zs = [], [], []
    for x in xs_:
        for y in ys_:
            xs.append(x)
            ys.append(y)
            zs.append(f(Vector(x, y)))

    ax.scatter(xs, ys, zs)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

    if points:
        for p in points:
            ax.scatter(p.x, p.y, f(p), c='r', marker='o')

    plt.show()


if __name__ == '__main__':
    eps = 0.0001
    am = Amoeba(func, [0, 2], [0, 2], eps=eps)
    minimum = am.find_min()
    print(minimum)
    plot_3d(func, [0, 2], [0, 2], points=[minimum])
