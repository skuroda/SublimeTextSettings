import sublime
import sublime_plugin

class ChangeViewCommand(sublime_plugin.WindowCommand):
    def run(self, reverse=False):
        window = self.window
        group, view_index = window.get_view_index(window.active_view())

        if view_index >= 0:
            views = window.views_in_group(group)
            if reverse:
                if view_index == 0:
                    view_index = len(views)

            if reverse:
                new_index = view_index - 1
            else:
                new_index = (view_index + 1) % len(views)
            window.focus_view(views[new_index])
