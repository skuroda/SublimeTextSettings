import sublime_plugin
import sublime

class MoveInterceptCommand(sublime_plugin.TextCommand):
    def run(self, edit, by, forward, extend=False):
        move_cursor_to_visible(self.view)
        self.view.run_command("move", {"by": by, "forward": forward, "extend": extend})

class MoveToInterceptCommand(sublime_plugin.TextCommand):
    def run(self, edit, to, extend=False):
        move_cursor_to_visible(self.view)
        self.view.run_command("move_to", {"to": to, "extend": extend})

class MoveInterceptEventListener(sublime_plugin.EventListener):
    def on_text_command(self, view, command_name, args):
        move_by_list = ["characters", "lines", "words", "word_ends", "subwords", "subword_ends", "pages"]
        move_to_list = ["bol", "eol"]

        if command_name == "move":
            if "by" in args and args["by"] in move_by_list:
                return ("move_intercept", args)
        elif command_name == "move_to":
            if "to" in args and args["to"] in move_to_list:
                return ("move_to_intercept", args)

def move_cursor_to_visible(view):
    vis_region = view.visible_region()
    cursors = view.sel()
    move_cursor_top = False
    move_cursor_bottom = False

    if len(cursors) > 0:
        return

    for cursor in cursors:
        if cursor.b < vis_region.begin():
            move_cursor_top = True
            break
        if cursor.b > vis_region.end():
            move_cursor_bottom = True
            break
    if move_cursor_top:
        cursors.clear()
        cursors.add(sublime.Region(vis_region.begin(), vis_region.begin()))
    elif move_cursor_bottom:
        cursors.clear()
        line = view.line(vis_region.end())
        cursors.add(sublime.Region(line.begin(), line.begin()))
