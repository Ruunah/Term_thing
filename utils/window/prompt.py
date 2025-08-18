#import tomllib

#with open("prompt.toml", "rb") as f:
#    config = tomllib.load(f)

def load(self, bg_color, style=""):
    try:
        match style:
            case "transient":
                if self.vfs.cwd == self.vfs.root:
                    cwd = "<b>root<b>"

                elif self.vfs.cwd == self.vfs.home:
                    cwd = " "

                else:
                    cwd = str(self.vfs.cwd.relative_to(self.vfs.root)).replace("\\", "/").split("/")[-1]
                
                prompt=f"""<span style='color:#61AFEF; background-color:{bg_color}'></span><span style='color:#011627; background-color:#61AFEF'>{cwd}</span><span style='color:#61AFEF; background-color:{bg_color}'></span>"""

                return prompt

            case "normal":
                if self.vfs.cwd == self.vfs.root:
                    cwd = "<b>root <b>"

                elif self.vfs.cwd == self.vfs.home:
                    cwd = " "

                elif self.vfs.cwd.is_relative_to(self.vfs.home):
                    cwd = f" ❯<b>{str(self.vfs.cwd.relative_to(self.vfs.home))}<b>"

                else:
                    cwd = self.vfs.cwd.relative_to(self.vfs.root)
                
                cwd = "❯".join(str(cwd).split("/"))+"❯ "
                
                prompt=f"""<span style='color:#ffffff; background-color:{bg_color}'>╭─</span><span style='color:#61AFEF; background-color:{bg_color}'></span><span style='color:#011627; background-color:#61AFEF'> </span><span style='color:#61AFEF; background-color:#ffafd2'></span><span style='color:#011627; background-color:#ffafd2'> {cwd}</span><span style='color:#ffafd2; background-color:{bg_color}'><br></span><span style='color:#ffffff; background-color:{bg_color}'>╰─</span>"""

                return prompt

            case _:
                raise(ValueError)

    except(ValueError):
        print("style can only be normal or transient")
