import lxml.etree
import json
import xmltodict


def xml_validator(xml):
    xml_file = lxml.etree.parse(xml)
    xml_validator = lxml.etree.XMLSchema(file="schema.xsd")
    is_valid = xml_validator.validate(xml_file)
    return is_valid


def convert_xml_to_dict(xml):
    with open(xml) as xml_file:
        data_dict = xmltodict.parse(xml_file.read())
        json_data = json.dumps(data_dict)
    return json_data
