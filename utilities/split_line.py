import sublime
import sublime_plugin
import re


class SplitLineCommand(sublime_plugin.TextCommand):
    def run(self, edit, split_pattern=" "):
        view = self.view
        cursors = view.sel()
        if len(cursors) == 1:
            cursor = cursors[0]
            begin_offset = 0
            end_offset = 0
            if cursor.empty():
                region = view.line(cursor)
                content = view.substr(region)
                new_content = re.sub(split_pattern, "\n", content)

                view.replace(edit, region, new_content)
            else:
                region = cursor
                content = view.substr(region)
                new_content = ""
                if view.line(region).begin() != region.begin():
                    new_content = "\n"
                    begin_offset = 1
                new_content += re.sub(split_pattern, "\n", content)

                if view.line(region).end() != region.end():
                    new_content += "\n"
                    end_offset = - 1

            view.replace(edit, region, new_content)
            cursors.clear()
            cursors.add(sublime.Region(region.begin() + begin_offset, region.begin() + len(new_content) + end_offset))
            view.run_command("split_selection_into_lines")


class SplitLineEventListener(sublime_plugin.EventListener):
    def on_text_command(self, view, command, args):
        if command == "split_selection_into_lines":
            if len(view.sel()) == 1:
                cursor = view.sel()[0]
                if view.line(cursor.begin()) == view.line(cursor.end()):
                    return "split_line", {"split_pattern": r"\s+"}
