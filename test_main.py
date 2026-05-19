import main
import flet as ft
class DummyControl:
    def __init__(self, data):
        self.data = data
class DummyEvent:
    def __init__(self, data):
        self.control = DummyControl(data)
class DummyPage:
    def __init__(self):
        self.overlay = []
    def update(self): pass
    def add(self, *args): pass

page = DummyPage()
# main.main(page) would fail because page doesn't mock everything.
