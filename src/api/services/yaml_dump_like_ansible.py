from io import StringIO
import re
import yaml

def yaml_dump_like_ansible(data, indent_size=2):
    stream = StringIO(yaml.dump(data, explicit_start=True, default_flow_style=False, indent=indent_size))
    out = StringIO()
    pat = re.compile('(\s*)([^:]*)(:*)')
    last = None

    prefix = 0
    for s in stream:
        indent, key, colon = pat.match(s).groups()
        if indent == "" and key[0] != '-':
            prefix = 0
        if last:
            if len(last[0]) == len(indent) and last[2] == ':':
                if all([
                        not last[1].startswith('-'),
                        s.strip().startswith('-')
                        ]):
                    prefix += indent_size
        out.write(" "*prefix+s)
        last = indent, key, colon
    return out.getvalue()
