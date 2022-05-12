import datetime
from DataModel import sanction_web
from DataModel.CH.sanction_CH_generic_attribute import SanctionCHGenericAttribute

# XML class: target
from DataModel.CH.sanction_CH_program import SanctionCHProgram


class SanctionCH:

    def __init__(self, ssid=0, sanctions_set_id=0, foreign_identifier='',
                 generic_attribute=None, modification=None, sex='', object_type='', identity=None, justification=None,
                 relation=None, other_information=None, sanction_set: SanctionCHProgram = None):
        self.sanction_set = sanction_set
        self.object_type = object_type
        if other_information is None:
            other_information = []
        if relation is None:
            relation = []
        if justification is None:
            justification = []
        if identity is None:
            identity = []
        self.other_information = other_information
        self.relation = relation
        self.justification = justification
        self.identity = identity
        self.sex = sex
        if generic_attribute is None:
            generic_attribute = []
        if modification is None:
            modification = []
        self.generic_attribute = generic_attribute
        self.foreign_identifier = foreign_identifier
        self.sanctions_set_id = sanctions_set_id
        self.ssid = ssid
        self.modification = modification
        self.search_fields = []
        for iden in self.identity:
            for name in iden.name:
                main_name = ''
                names = []
                for i in range(0, len(name.name_part)):
                    part = name.name_part[i]
                    if main_name:
                        main_name = main_name + ' ' + part.value
                    else:
                        main_name = part.value
                    for j in range(0, len(part.spelling_variant)):
                        if len(names) == j:
                            names.append(part.spelling_variant[j])
                        else:
                            names[j] = names[j] + ' ' + part.spelling_variant[j]
                self.search_fields.append(main_name)
                self.search_fields.extend(names)


    def webify(self):
        main_name = self.search_fields[0]

        names = ''
        for i in range(1, len(self.search_fields)):
            if names:
                names = names + '\n' + self.search_fields[i]
            else:
                names = self.search_fields[i]

        program = ''
        p = self.sanction_set
        if program:
            program = program + ';\n' + p.program_name
        else:
            program = p.program_name
        program = program + '\n' + p.sanctions_set

        nationality = ''
        for iden in self.identity:
            for nation in iden.nationality:
                if nationality:
                    nationality = nationality + ';\n' + nation
                else:
                    nationality = nation

        address = ''
        for iden in self.identity:
            for addr in iden.address:
                if addr.c_o:
                    address = address + 'c.o. ' + addr.c_o + ', '
                if addr.address_details:
                    address = address + addr.address_details + ', '
                if addr.p_o_box:
                    address = address + 'p.o. ' + addr.p_o_box + ', '
                if addr.zip_code:
                    address = address + 'zip ' + addr.zip_code + ', '
                place = addr.place
                if place.location:
                    address = address + place.location + ', '
                if place.area:
                    address = address + place.area + ', '
                if place.country:
                    address = address + place.country + ', '
                if addr.remark:
                    address = address + addr.remark
                if address:
                    address = address + '\n'

        personal_details = ''
        if self.sex:
            personal_details = 'Gender: ' + self.sex + '\n'
        if self.object_type:
            personal_details = 'Type: ' + self.object_type + '\n'

        additional_info = ''
        for text in self.justification:
            if additional_info:
                additional_info = additional_info + ';\n' + text
            else:
                additional_info = text
        for rel in self.relation:
            text = rel.relation_type + ' ' + rel.target_name
            if rel.remark:
                text = text + '; ' + rel.remark
            if additional_info:
                additional_info = additional_info + ';\n' + text
            else:
                additional_info = text
        for text in self.other_information:
            if additional_info:
                additional_info = additional_info + ';\n' + text
            else:
                additional_info = text

        sanction = sanction_web.SanctionWeb(main_name=main_name, names=names, sanctioned_by='ch',
                                            program=program, nationality=nationality, address=address,
                                            personal_details=personal_details, additional_info=additional_info,
                                            id=self.ssid)
        return sanction

