# labelme-parse

Utility functions to parse json file generated by labelme

## Installation

You can install the package via pip:

```bash
pip install labelme-parse
```

## Usage

```python
from pathlib import Path

from labelme_parse import get_point
from labelme_parse import get_point_names
from labelme_parse import get_poly
from labelme_parse import get_poly_names
from labelme_parse import get_rect
from labelme_parse import get_rect_names

d = Path("path/to/dir")


print(get_point_names(d))
# ["dp_7_to_dp_0"]
print(get_rect_names(d))
# ["dp_0"]
print(get_poly_names(d))
# ["dp_8"]
print(get_point(d, "dp_7_to_dp_0"))
# (329, 919)
print(get_rect(d, "dp_0"))
# (301, 897, 38, 38)
print(get_poly(d, "dp_8"))
# [(317, 909), (309, 909), (309, 914), (313, 914), (313, 920), (327, 920), (327, 914), (331, 914), (331, 909), (322, 909), (322, 907), (317, 907)]
```

## License

This project is licensed under the terms of the MIT license.
