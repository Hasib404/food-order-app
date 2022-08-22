import lxml.etree
import xmltodict


def xml_validator(xml, schema):
    xml_file = lxml.etree.parse(xml)
    xml_validator = lxml.etree.XMLSchema(file=schema)
    is_valid = xml_validator.validate(xml_file)
    return is_valid


def convert_xml_to_dict(xml):
    with open(xml) as xml_file:
        data_dict = xmltodict.parse(xml_file.read())
    return data_dict


def pascal_to_snake(string):
    snake_case = "".join(
        ["_" + char.lower() if char.isupper() else char for char in string]
    ).lstrip("_")

    return snake_case
