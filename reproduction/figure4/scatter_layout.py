"""Enlarge six comparable axes within their existing outer rectangle."""
import numpy as np


def compact_rectangles(rectangles, figure_width_pt, figure_height_pt,
                       horizontal_gap_pt=24., vertical_gap_pt=40.):
    boxes = np.asarray(rectangles, dtype=float)
    if boxes.shape != (6, 4) or not np.isfinite(boxes).all():
        raise ValueError('Six finite x/y/width/height axes rectangles are required')
    if np.any(boxes[:, 2:] <= 0) or min(figure_width_pt, figure_height_pt) <= 0:
        raise ValueError('Figure and axes dimensions must be positive')
    left, bottom = boxes[:, :2].min(axis=0)
    right = np.max(boxes[:, 0] + boxes[:, 2])
    top = np.max(boxes[:, 1] + boxes[:, 3])
    gap_x, gap_y = horizontal_gap_pt / figure_width_pt, vertical_gap_pt / figure_height_pt
    width, height = (right - left - 2 * gap_x) / 3, (top - bottom - gap_y) / 2
    if min(width, height) <= 0 or min(gap_x, gap_y) < 0:
        raise ValueError('Gaps leave no positive plotting area')
    return np.array([[left + col * (width + gap_x),
                      bottom + (1 - row) * (height + gap_y), width, height]
                     for row in range(2) for col in range(3)])
