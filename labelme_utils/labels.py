import json
from functools import lru_cache
from pathlib import Path
from typing import List
from typing import Optional
from typing import Tuple


def get_rect_from_points(points: List[List[float]]):
    x, y = points[0]
    x1, y1 = points[1]
    big_x, big_y = max(x1, x), max(y1, y)
    small_x, small_y = min(x1, x), min(y1, y)
    w, h = big_x - small_x, big_y - small_y
    return int(small_x), int(small_y), int(w + 1), int(h + 1)


@lru_cache
def get_labels(
    dir_path: Path, width: Optional[int] = None, height: Optional[int] = None
):
    """
    :param width: width of the screen
    :param height: height of the screen
    """
    output: dict[Tuple[str, str], Tuple[Path, List[List[float]], str]] = {}
    for file_path in dir_path.glob("*.json"):
        with open(file_path) as fp:
            data = json.load(fp)
            if (not height or data["imageHeight"] == height) and (
                not width or data["imageWidth"] == width
            ):
                for shape in data["shapes"]:
                    points: List[List[float]] = shape["points"]
                    label: str = shape["label"]
                    output[(shape["shape_type"], label)] = (
                        file_path,
                        points,
                        shape["shape_type"],
                    )
    return output


def get_point(
    dir_path: Path,
    label: str,
    width: Optional[int] = None,
    height: Optional[int] = None,
):
    _, p, _ = get_labels(dir_path, width, height)["point", label]
    return int(p[0][0]), int(p[0][1])


def get_rect(
    dir_path: Path,
    label: str,
    width: Optional[int] = None,
    height: Optional[int] = None,
):
    _, points, _ = get_labels(dir_path, width, height)["rectangle", label]
    return get_rect_from_points(points)


def get_rect_relative(
    dir_path: Path,
    label: str,
    parent: str,
    width: Optional[int] = None,
    height: Optional[int] = None,
):
    """
    Parses the rectangle of a label relative to parent rectangle

    For example, if rectangle C is inside rectangle P
    this function returns the rectangle P related to rectangle C
    """
    _, points, _ = get_labels(dir_path, width, height)["rectangle", parent]
    x0, y0, _, _ = get_rect_from_points(points)
    _, points, _ = get_labels(dir_path, width, height)["rectangle", label]
    x, y, w, h = get_rect_from_points(points)
    return x - x0, y - y0, w, h


def get_poly(dir_path: Path, label: str):
    _, points, _ = get_labels(dir_path)["polygon", label]
    p = [(int(p[0]), int(p[1])) for p in points]
    return p


def get_point_names(dir_path: Path):
    return [
        k[1]
        for k, v in get_labels(dir_path).items()
        if v[0].stem.startswith("floor") and v[2] == "point"
    ]


def get_rect_names(dir_path: Path):
    return [
        k[1]
        for k, v in get_labels(dir_path).items()
        if v[0].stem.startswith("floor") and v[2] == "rectangle"
    ]


def get_poly_names(dir_path: Path):
    return [
        k[1]
        for k, v in get_labels(dir_path).items()
        if v[0].stem.startswith("floor") and v[2] == "polygon"
    ]
