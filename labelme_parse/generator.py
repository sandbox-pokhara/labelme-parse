from argparse import ArgumentParser
from collections import Counter
from pathlib import Path
from typing import Optional

from labelme_parse.labels import get_labels_as_list
from labelme_parse.labels import get_rect_from_points

LABEL_TEMPLATE = """{var} = {cls}(
    name="{name}",
    file_name="{file_name}",
    type="{type}",
    points={points},
    value={value},
)
"""

RECTANGLES_TEMPLATE = """RECTANGLES: dict[str, tuple[int, int, int, int]] = {{
{lines}}}
"""
POINTS_TEMPLATE = """POINTS: dict[str, tuple[int, int]] = {{
{lines}}}
"""
LINES_TEMPLATE = """LINES: dict[str, tuple[tuple[int, int], tuple[int, int]]] = {{
{lines}}}
"""


def generate_python_code(
    dir_path: Path,
    width: Optional[int] = None,
    height: Optional[int] = None,
):
    labels = get_labels_as_list(dir_path, width, height)
    name_counter = Counter[str]()
    output = ""
    rect_map = ""
    point_map = ""
    line_map = ""
    for l in labels:
        name, _, points, typ = l
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
            var = name + "_" + str(name_counter[name])
        else:
            var = name
        output += f"{var.upper()} = {value}\n"
        if typ == "rectangle":
            rect_map += f'    "{var}": {var.upper()},\n'
        if typ == "point":
            point_map += f'    "{var}": {var.upper()},\n'
        if typ == "line":
            line_map += f'    "{var}": {var.upper()},\n'
        name_counter.update([name])
    output += RECTANGLES_TEMPLATE.format(lines=rect_map)
    output += POINTS_TEMPLATE.format(lines=point_map)
    output += LINES_TEMPLATE.format(lines=line_map)
    return output


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
