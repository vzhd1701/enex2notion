import contextlib
import re
from functools import partial
from math import sqrt
from types import MappingProxyType

from tinycss2 import parse_declaration_list
from tinycss2.color3 import parse_color

HEX_BASE = 16

base16 = partial(int, base=HEX_BASE)

EVERNOTE_STANDARD_FG = MappingProxyType(
    {
        (51, 51, 51): "black",
        (90, 90, 90): "gray",
        (140, 140, 140): "gray",
        (191, 191, 191): "gray",
        (255, 255, 255): "white",
        (87, 36, 194): "purple",
        (182, 41, 212): "purple",
        (252, 18, 51): "red",
        (251, 95, 44): "orange",
        (229, 158, 37): "yellow",
        # green
        (24, 168, 65): "teal",
        (26, 169, 178): "blue",
        (24, 133, 226): "blue",
        (13, 58, 153): "blue",
    }
)

EVERNOTE_STANDARD_BG = MappingProxyType(
    {
        (255, 209, 176): "orange_background",
        (255, 239, 158): "yellow_background",
        # old yellowish highlight
        (255, 250, 165): "yellow_background",
        # green
        (183, 247, 209): "teal_background",
        (173, 236, 244): "blue_background",
        (203, 202, 255): "purple_background",
        (254, 193, 208): "red_background",
    }
)

COLORS_FG = MappingProxyType(
    {
        "black": (0, 0, 0),
        "white": (255, 255, 255),
        "gray": (140, 140, 140),
        "brown": (159, 107, 83),
        "orange": (251, 95, 33),
        "yellow": (229, 158, 37),
        # green
        "teal": (24, 168, 65),
        "blue": (24, 133, 226),
        "purple": (182, 41, 212),
        "pink": (193, 76, 138),
        "red": (252, 18, 51),
    }
)

COLORS_BG = MappingProxyType(
    {
        "black_background": (0, 0, 0),
        "white_background": (255, 255, 255),
        "gray_background": (241, 241, 239),
        "brown_background": (244, 238, 238),
        "orange_background": (255, 209, 176),
        "yellow_background": (255, 239, 158),
        # green
        "teal_background": (183, 247, 209),
        "blue_background": (173, 236, 244),
        "purple_background": (203, 202, 255),
        "pink_background": (249, 238, 243),
        "red_background": (254, 193, 208),
    }
)


def extract_color(style):  # noqa: WPS210
    color_map = {
        ".*en-highlight$": _extract_background_text,
        "^background-color$": _extract_background_rgb,
        "^color$": _extract_foreground_rgb,
    }

    for s_name, s_value in _parse_style(style).items():
        for regex, color_extract_func in color_map.items():
            if re.match(regex, s_name):
                color = color_extract_func(s_value)
                if color:
                    return color

    return None


def _parse_style(style):
    result_styles = {}

    declarations = (
        d
        for d in parse_declaration_list(style, skip_comments=True, skip_whitespace=True)
        if d.type == "declaration"
    )

    for dec in declarations:
        with contextlib.suppress(StopIteration):
            result_styles[dec.lower_name] = next(
                v for v in dec.value if v.type not in {"whitespace", "comment"}
            )

    return result_styles


def _parse_css_color(color_token):
    rgba = parse_color(color_token)

    if rgba is None or rgba == "currentColor":
        return None

    float_to_int_rgb = 255

    return tuple(int(c * float_to_int_rgb) for c in (rgba[:3]))


def _extract_background_text(color_token):
    color = f"{color_token.value}_background"

    if color == "green_background":
        color = "teal_background"

    if color in COLORS_BG:
        return color

    return None


def _extract_background_rgb(color_token):
    rbg_bg = _parse_css_color(color_token)

    if rbg_bg is None:
        return None

    if EVERNOTE_STANDARD_BG.get(rbg_bg):
        return EVERNOTE_STANDARD_BG[rbg_bg]
    else:
        color = _closest_color(COLORS_BG, rbg_bg)

    if color not in {"black_background", "white_background"}:
        return color

    return None


def _extract_foreground_rgb(color_token):
    rbg_fg = _parse_css_color(color_token)

    if rbg_fg is None:
        return None

    if EVERNOTE_STANDARD_FG.get(rbg_fg):
        color = EVERNOTE_STANDARD_FG[rbg_fg]
    else:
        color = _closest_color(COLORS_FG, rbg_fg)

    if color not in {"black", "white"}:
        return color

    return None


def _closest_color(colors, rgb):  # noqa: WPS210
    r, g, b = rgb
    color_diffs = []
    for color_name, color in colors.items():
        cr, cg, cb = color
        color_diff = sqrt(
            abs(r - cr) ** 2 + abs(g - cg) ** 2 + abs(b - cb) ** 2,  # noqa: WPS221
        )
        color_diffs.append((color_diff, color_name))
    return min(color_diffs)[1]
