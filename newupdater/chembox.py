import wikitextparser as wtp
from pathlib import Path

Dir = Path(__file__).parent

from newupdater.lists.chem_params import rename_chem_params


class fix_Chembox:
    def __init__(self, text):
        self.text = text
        self.new_text = text

        self.all_params = {}
        self.oldchembox = ""
        self.newchembox = "{{drugbox"

    def run(self):
        self.get_params()
        # ---
        if not self.all_params:
            return self.new_text
        # ---
        # create self.newchembox
        self.new_temp()
        # ---
        if self.oldchembox != "" and self.newchembox != "":
            self.new_text = self.new_text.replace(self.oldchembox, self.newchembox)
        # ---
        return self.new_text

    def get_params(self):
        # ---
        parsed = wtp.parse(self.text)
        # ---
        for template in parsed.templates:
            # ---
            if not template:
                continue
            # ---
            name = str(template.normal_name()).strip()
            # ---
            boxes = [
                "chembox",
                "chembox identifiers",
                "chembox properties",
                "chembox hazards",
                "chembox thermochemistry",
                "chembox explosive",
                "chembox pharmacology",
                "chembox related",
                "chembox structure",
                "chembox supplement",
            ]
            # ---
            if name.lower() == "chembox":
                self.oldchembox = template.string
            # ---
            # if name.lower().startswith("chembox"):
            elif name.lower() not in boxes:
                continue
            # ---
            params = {str(param.name).strip(): str(param.value) for param in template.arguments}
            # ---
            for x, v in params.items():
                if not v.strip():
                    continue
                # ---
                if x.lower().startswith("section"):
                    continue
                # ---
                self.all_params[x] = v

    def new_temp(self):
        # ---
        for p, value in self.all_params.items():
            # ---
            p = rename_chem_params.get(p, "") if rename_chem_params.get(p, "") != "" else p
            # ---
            p_v = f"\n| {p}= {value}"
            # ---
            self.newchembox += p_v
            # ---
        # ---
        self.newchembox += "\n}}"


if __name__ == "__main__":
    import pywikibot

    text = {}

    # ---

    with open(f"{Dir}/texts/chembox.txt", "r", encoding="utf-8") as f:
        text = f.read(f)
    bot = fix_Chembox(text)
    newtext = bot.run()
    pywikibot.showDiff(text, newtext)
