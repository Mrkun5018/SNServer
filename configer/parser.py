from configparser import ConfigParser
from .config import SERVER, MYSQL, JWT, LOCAL

config_object_table = {
    "server": SERVER,
    "mysql": MYSQL,
    "local": LOCAL,
    "jwt": JWT
}


def mapping_config_object(cnf_name):

    parser = ConfigParser()
    parser.read(cnf_name)

    config_section_table = {}
    for name, section in parser.items():
        if name not in config_object_table.keys():
            continue
        config_section_table[name] = section

    for name, section in config_section_table.items():
        for field in section.keys():
            field_upper = field.upper()

            if field_upper in ('DEBUG', ):
                cnf_value = section.getboolean(field, fallback=None)
            elif field_upper in ('PORT', ):
                cnf_value = section.getint(field, fallback=None)
            else:
                cnf_value = section.get(field, fallback=None)

            if cnf_value is None:
                continue

            print(f" - load configer {name}.{field}={cnf_value}")
            cnf_object = config_object_table[name]
            setattr(cnf_object, field_upper, cnf_value)


if __name__ == '__main__':
    mapping_config_object('../server.ini')
    print(JWT.KEY)
