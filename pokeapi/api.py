import pokebase


class Pokemon:
    def __init__(self, name):
        self.pokemon = pokebase.pokemon(name)
        self.name = name if len(name) > 0 else "Unidentified Pokemon"
        self.is_fakemon = False
        if self.pokemon.id_ is None:
            self.is_fakemon = True

    def get_types(self):
        types = []
        if not self.is_fakemon:
            for type_metadata in self.pokemon.types:
                types.append(type_metadata.type.name)
        else:
            types = ["ghost", "psychic"]
        return types

    def get_damage_relations(self):
        type_relations = {}
        for type_name in self.get_types():
            type_metadata = pokebase.type_(type_name)
            damage_relations = type_metadata.damage_relations
            damage_multiplier_table = [
                (damage_relations.double_damage_from, 2),
                (damage_relations.half_damage_from, 0.5),
                (damage_relations.no_damage_from, 0)
            ]
            for related_types_metadata, multiplier in damage_multiplier_table:
                for related_type in related_types_metadata:
                    if related_type.name in type_relations:
                        type_relations[related_type.name] *= multiplier
                    else:
                        type_relations[related_type.name] = multiplier
        return type_relations

    def get_formatted_damage_relations(self):
        multiplier_descriptions = {
            4: "Super Weak To",
            2: "Weak To",
            0.5: "Resists",
            0.25: "Super Resists",
            0: "Immune To"
        }
        type_relations = self.get_damage_relations()
        multiplier_dict = {mult: [] for mult in multiplier_descriptions.keys()}

        for type_name in type_relations:
            multiplier_value = type_relations[type_name]
            if multiplier_value != 1:
                multiplier_dict[multiplier_value].append(type_name)

        base_string = "\t--Incoming Damage Matchups--"
        output = base_string
        for multiplier_value, types in multiplier_dict.items():
            if len(types) > 0:
                output += f"\n\t{multiplier_descriptions[multiplier_value]}:"
                for type_name in types:
                    output += f" {type_name.title()},"
                output = output.strip(',')

        if output == base_string:
            output = "\tTyping is True Neutral"

        return output

    def __str__(self):
        output = f"{self.name}:"
        output += f"\n\ttypes: {self.get_types()}"
        output += "\n" + self.get_formatted_damage_relations()
        return output




