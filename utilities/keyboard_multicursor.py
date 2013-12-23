import sublime
import sublime_plugin


class MultiCursorCommand(sublime_plugin.TextCommand):
    def run(self, edit, action="add"):
        self.key = "multi_cursor"
        cursors = self.view.sel()
        saved_cursors = self.view.get_regions(self.key)
        if action == "add":
            self.view.add_regions(self.key, list(cursors) + saved_cursors, "keyword", "", sublime.DRAW_EMPTY)
        elif action == "show":
            cursors.add_all(saved_cursors)
            self.view.add_regions(self.key, [])
        elif action == "show_begin":
            saved_cursors += list(cursors)
            cursors.clear()
            cursors.add_all([c.begin() for c in saved_cursors])
            self.view.add_regions(self.key, [])
        elif action == "show_end":
            saved_cursors += list(cursors)
            cursors.clear()
            cursors.add_all([c.end() for c in saved_cursors])
            self.view.add_regions(self.key, [])
        elif action == "show_visible":
            pass
        elif action == "clear":
            self.view.add_regions(self.key, [])
        elif action == "remove":
            for cursor in cursors:
                if cursor in saved_cursors:
                    saved_cursors.remove(cursor)
            self.view.add_regions(self.key, saved_cursors, "keyword", "", sublime.DRAW_EMPTY)


class RemoveCursorCommand(sublime_plugin.TextCommand):
    def is_enabled(self):
        return len(self.view.sel()) > 1

    def run(self, edit, forward=True):
        self.view.sel().subtract(self.view.sel()[0 if forward else -1])
