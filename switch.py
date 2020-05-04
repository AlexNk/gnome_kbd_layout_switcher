#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
import time

import dbus
from json import loads as json_loads

def list_layouts():
    try:
        bus = dbus.SessionBus()
        proxy = bus.get_object("org.gnome.Shell", "/org/gnome/Shell")
        method = proxy.get_dbus_method("Eval", "org.gnome.Shell")
        success, res = method("imports.ui.status.keyboard.getInputSourceManager().inputSources")
        if not success:
            raise Exception(res)
        res = json_loads(res);
        return [(l["id"], l["index"]) for l in res.values()]
    finally:
        bus.close()

def get_active_layout():
    try:
        bus = dbus.SessionBus()
        proxy = bus.get_object("org.gnome.Shell", "/org/gnome/Shell")
        method = proxy.get_dbus_method("Eval", "org.gnome.Shell")
        success, res = method("imports.ui.status.keyboard.getInputSourceManager().currentSource.index")
        if not success:
            raise Exception(res)
        return int(res)
    finally:
        bus.close()

def set_layout(index):
    try:
        bus = dbus.SessionBus()
        proxy = bus.get_object("org.gnome.Shell", "/org/gnome/Shell")
        method = proxy.get_dbus_method("Eval", "org.gnome.Shell")
        success, res = method(f"imports.ui.status.keyboard.getInputSourceManager().inputSources[{index}].activate()")
        if not success:
            raise Exception(res)
    finally:
        bus.close()

def switch_layout():
    js_remote_code = """
const mgr = imports.ui.status.keyboard.getInputSourceManager();
const keys = Object.keys(mgr.inputSources);
const current = (mgr.currentSource.index + 1) % keys.length;
mgr.inputSources[current].activate(); current"""
    try:
        bus = dbus.SessionBus()
        proxy = bus.get_object("org.gnome.Shell", "/org/gnome/Shell")
        method = proxy.get_dbus_method("Eval", "org.gnome.Shell")
        success, res = method(js_remote_code)
        if not success:
            raise Exception(res)
    finally:
        bus.close()

