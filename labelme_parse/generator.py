from argparse import ArgumentParser
from collections import Counter
from pathlib import Path
from typing import Optional

from labelme_parse.labels import get_labels_as_list
from labelme_parse.labels import get_rect_from_points

IMPORTS = """from typing import Literal

"""
RECTANGLES_LITERALS_TEMPLATE = """Rectangles = Literal[
{lines}]
"""
POINTS_LITERALS_TEMPLATE = """Points = Literal[
{lines}]
"""
LINES_LITERALS_TEMPLATE = """Lines = Literal[
{lines}]
"""
RECTANGLES_TEMPLATE = """RECTANGLES: dict[Rectangles, tuple[int, int, int, int]] = {{
{lines}}}
"""
POINTS_TEMPLATE = """POINTS: dict[Points, tuple[int, int]] = {{
{lines}}}
"""
LINES_TEMPLATE = """LINES: dict[Lines, tuple[tuple[int, int], tuple[int, int]]] = {{
{lines}}}
"""


def generate_python_code(
    dir_path: Path,
    width: Optional[int] = None,
    height: Optional[int] = None,
):
    labels = get_labels_as_list(dir_path, width, height)
    name_counter = Counter[str]()
    output = IMPORTS
    rect_vars: list[tuple[str, str]] = []
    point_vars: list[tuple[str, str]] = []
    line_vars: list[tuple[str, str]] = []
    for l in labels:
        name, _, points, typ = l
        if name_counter[name] > 0:
            var = name + "_" + str(name_counter[name])
        else:
            var = name
        if typ == "rectangle":
            value = get_rect_from_points(points)
            rect_vars.append((var, str(value)))
        elif typ == "point":
            value = int(points[0][0]), int(points[0][1])
            point_vars.append((var, str(value)))
        elif typ == "line":
            value = (int(points[0][0]), int(points[0][1])), (
                int(points[1][0]),
                int(points[1][1]),
            )
            line_vars.append((var, str(value)))
        else:
            raise NotImplementedError(f"Label type {typ} is not implemented.")
        # output += f"{var.upper()} = {value}\n"
        name_counter.update([name])
    lines = "".join([f'    "{var}",\n' for var, _ in rect_vars])
    output += RECTANGLES_LITERALS_TEMPLATE.format(lines=lines)
    lines = "".join([f'    "{var}",\n' for var, _ in point_vars])
    output += POINTS_LITERALS_TEMPLATE.format(lines=lines)
    lines = "".join([f'    "{var}",\n' for var, _ in line_vars])
    output += LINES_LITERALS_TEMPLATE.format(lines=lines)

    lines = "".join([f'    "{var}": {value},\n' for var, value in rect_vars])
    output += RECTANGLES_TEMPLATE.format(lines=lines)
    lines = "".join([f'    "{var}": {value},\n' for var, value in point_vars])
    output += POINTS_TEMPLATE.format(lines=lines)
    lines = "".join([f'    "{var}": {value},\n' for var, value in line_vars])
    output += LINES_TEMPLATE.format(lines=lines)
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
