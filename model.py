import anki.stdmodels


def add_chinese_model(col):
    """ Creates a general chinese model used for notes """

    models = col.models
    model = models.new("Chinese (alt)")

    models.addField(model, models.newField("Hanzi"))
    models.addField(model, models.newField("Meaning"))
    models.addField(model, models.newField("Pinyin"))

    template = models.newTemplate("Recognition")
    template["qfmt"] = "<div>{{ Hanzi }}</div>"
    template["afmt"] = """
    <div class="meaning">{{ Meaning }}</div>
    <div>{{ Pinyin }}</div>
    <div>{{ Hanzi }}</div>
    """
    models.addTemplate(model, template)

    model["css"] += """
    .meaning {
        margin-bottom: 2em;
    }
    """

    models.add(model)
    return model


anki.stdmodels.models.append(("Chinese (alt)", add_chinese_model))
