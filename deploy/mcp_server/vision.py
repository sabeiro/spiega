"""
YOLO-based scene description for the camera. Lightweight alternative to LLaVA on Jetson.
"""
from __future__ import annotations

import json
from collections import Counter
from typing import Union

import cv2
import numpy as np

_YOLO_MODEL = None


def _get_model():
    global _YOLO_MODEL
    if _YOLO_MODEL is None:
        from ultralytics import YOLO
        _YOLO_MODEL = YOLO("yolov8n.pt")  # nano, runs on CPU
    return _YOLO_MODEL


def describe_scene_yolo(image: Union[bytes, np.ndarray]) -> str:
    """
    Run YOLO object detection on an image and return a short text description.
    image: JPEG bytes or BGR numpy array (H, W, 3).
    """
    if isinstance(image, bytes):
        arr = np.frombuffer(image, dtype=np.uint8)
        frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if frame is None:
            return json.dumps({"error": "Could not decode image"})
    else:
        frame = image
    try:
        model = _get_model()
        results = model.predict(frame, verbose=False)
    except Exception as e:
        return json.dumps({"error": f"YOLO inference failed: {e}"})
    if not results:
        return "Detected: nothing."
    r = results[0]
    if r.boxes is None or len(r.boxes.cls) == 0:
        return "Detected: nothing."
    names = r.names or {}
    classes = [names.get(int(c), "?") for c in r.boxes.cls]
    counts = Counter(classes)
    parts = [f"{name} ({n})" if n > 1 else name for name, n in sorted(counts.items())]
    return "Detected: " + ", ".join(parts) + "."


def detect_yolo(image: Union[bytes, np.ndarray]) -> list[dict]:
    """
    Run YOLO object detection and return list of detections with bbox and label.
    image: JPEG bytes or BGR numpy array (H, W, 3).
    Returns list of {"label": str, "bbox": [x1, y1, x2, y2], "confidence": float}.
    """
    if isinstance(image, bytes):
        arr = np.frombuffer(image, dtype=np.uint8)
        frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if frame is None:
            return []
    else:
        frame = image
    try:
        model = _get_model()
        results = model.predict(frame, verbose=False)
    except Exception:
        return []
    if not results:
        return []
    r = results[0]
    if r.boxes is None or len(r.boxes.cls) == 0:
        return []
    names = r.names or {}
    out = []
    for i in range(len(r.boxes.cls)):
        cls_id = int(r.boxes.cls[i])
        label = names.get(cls_id, "?")
        # xyxy: [x1, y1, x2, y2] in pixel coords (tensor or ndarray)
        xyxy = r.boxes.xyxy[i]
        if hasattr(xyxy, "tolist"):
            bbox = xyxy.tolist()
        else:
            bbox = [float(xyxy[0]), float(xyxy[1]), float(xyxy[2]), float(xyxy[3])]
        conf = float(r.boxes.conf[i]) if r.boxes.conf is not None else None
        out.append({
            "label": label,
            "bbox": bbox,
            "confidence": conf,
        })
    return out


def plot_yolo(image: Union[bytes, np.ndarray]) -> bytes | None:
    """
    Run YOLO and return the image with bounding boxes and labels drawn (standard YOLO visual).
    image: JPEG bytes or BGR numpy array (H, W, 3).
    Returns JPEG bytes, or None on failure.
    """
    if isinstance(image, bytes):
        arr = np.frombuffer(image, dtype=np.uint8)
        frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if frame is None:
            return None
    else:
        frame = image.copy()
    try:
        model = _get_model()
        results = model.predict(frame, verbose=False)
    except Exception:
        return None
    if not results:
        return None
    r = results[0]
    # plot() returns BGR numpy array with boxes and labels drawn
    plotted = r.plot()
    if plotted is None:
        return None
    _, jpeg = cv2.imencode(".jpg", plotted)
    return jpeg.tobytes()
