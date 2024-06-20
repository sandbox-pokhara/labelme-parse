from argparse import ArgumentParser
from collections import Counter
from pathlib import Path
from typing import Optional

from labelme_parse.labels import get_labels_as_list
from labelme_parse.labels import get_rect_from_points

CLASSES = """from dataclasses import dataclass


@dataclass
class Label:
    name: str
    file_name: str
    type: str
    points: list[tuple[int, int]]


@dataclass
class Rectangle(Label):
    value: tuple[int, int, int, int]


@dataclass
class Point(Label):
    value: tuple[int, int]


@dataclass
class Line(Label):
    value: tuple[tuple[int, int], tuple[int, int]]


"""

LABEL_TEMPLATE = """{var} = {cls}(
    name="{name}",
    file_name="{file_name}",
    type="{type}",
    points={points},
    value={value},
)
"""

ALL_LABELS_TEMPLATE = """ALL_LABELS = [
{lines}]
"""


def generate_python_code(
    dir_path: Path, width: Optional[int] = None, height: Optional[int] = None
):
    labels = get_labels_as_list(dir_path, width, height)
    name_counter = Counter[str]()
    output = CLASSES
    all_labels_lines = ""
    for l in labels:
        name, path, points, typ = l
        var = name.upper()
        if typ == "rectangle":
            value = get_rect_from_points(points)
        elif typ == "point":
            value = int(points[0][0]), int(points[0][1])
        elif typ == "line":
            value = (int(points[0][0]), int(points[0][1])), (
                int(points[1][0]),
                int(points[1][1]),
            )
        else:
            raise NotImplementedError(f"Label type {typ} is not implemented.")
        if name_counter[name] > 0:
            var += "_" + str(name_counter[name])

        output += LABEL_TEMPLATE.format(
            var=var,
            cls=typ.title(),
            name=name,
            file_name=path.name,
            type=typ,
            points=[(int(p[0]), int(p[1])) for p in points],
            value=value,
        )
        all_labels_lines += "    " + var + "," + "\n"
        name_counter.update([name])
    return output + ALL_LABELS_TEMPLATE.format(lines=all_labels_lines)


def main():
    parser = ArgumentParser()
    parser.add_argument("labels_dir")
    parser.add_argument("-o", default="labels.py")
    args = parser.parse_args()

    data = generate_python_code(Path(args.labels_dir))
    with open(args.o, "w") as fp:
        fp.write(data)


if __name__ == "__main__":
    main()
