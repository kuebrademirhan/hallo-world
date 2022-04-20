from lxml import etree as xml_helper


def check_xml(schema, file):
    try:
        xml_file = xml_helper.parse(file)
        xml_validator = xml_helper.XMLSchema(file=schema)
        return xml_validator.validate(xml_file)

    except Exception as err:
        print("error!")
        print(err)
        return False


def read_xml(file):
    tree = xml_helper.parse(file)
    #rough_string = xml_helper.tostring(tree)
    #print(rough_string)
    #result = xml_helper.fromstring(rough_string)
    #print(result)
    root = tree.getroot()
    buchungen = []
    for child in root:
        print(child.tag)
        temp = myDBhelper.Buchung()
        for b in child:
            if b.tag == "pzn":
                temp.pzn = b.text
            elif b.tag == "quantity":
                temp.quantity = b.text
            elif b.tag == "type":
                temp.type = b.text
            elif b.tag == "time":
                temp.time = b.text

            #print(b.tag, end=";")
            #print(b.text)

        buchungen.append(temp)
    return buchungen


def check_xml(schema, file):
    try:
        xml_file = xml_helper.parse(file)
        xml_validator = xml_helper.XMLSchema(file=schema)
        return xml_validator.validate(xml_file)

    except Exception as err:
        print("error!")
        print(err)
        return False


def main():
    file = "../xml/firstxml.xml"
    schema = "xml/firstxsd.xsd"

    print("checking...", end="")
    print(check_xml(schema, file))

    print("reading...")
    read_xml(file)


if __name__ == "__main__":
    main()