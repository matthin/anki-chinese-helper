import anki.stdmodels

def add_chinese_model(col):
    mm = col.models
    m = mm.new("Chinese (alt)")

    fm = mm.newField("Hanzi")
    mm.addField(m, fm)

    fm = mm.newField("Meaning")
    mm.addField(m, fm)

    fm = mm.newField("Pinyin")
    mm.addField(m, fm)

    t = mm.newTemplate("Recognition")
    t["qfmt"] = "<div>{{ Hanzi }}</div>"
    t["afmt"] = """
    <div class="meaning">{{ Meaning }}</div>
    <div>{{ Pinyin }}</div>
    <div>{{ Hanzi }}</div>
    """
    mm.addTemplate(m, t)

    m["css"] += """
    .meaning {
        margin-bottom: 2em;
    }
    """

    mm.add(m)
    return m

anki.stdmodels.models.append(("Chinese (alt)", add_chinese_model))
