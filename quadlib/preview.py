#!/usr/bin/env python
# -*- coding: utf-8 -*-

def init(camera, resolution, overlay_render):
    _camera = camera
    _camera.resolution = resolution
    _overlay_render = overlay_render

def start():
    _camera.start_preview()
        
def render(img)
    if not overlay_renderer:
            """
            If overlay layer is not created yet, get a new one. Layer
            parameter must have 3 or higher number because the original
            preview layer has a # of 2 and a layer with smaller number will
            be obscured.
            """
            overlay_renderer = camera.add_overlay(img.tobytes(),
                                                    layer=3,
                                                    size=img.size,
                                                    alpha=128);
        else:
            overlay_renderer.update(img.tobytes())