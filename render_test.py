import zlib
import base64
import string
import urllib.request
import os

def plantuml_encode(plantuml_text):
    utf8_text = plantuml_text.encode('utf-8')
    zlibbed = zlib.compress(utf8_text)
    compressed = zlibbed[2:-4]
    
    plantuml_alphabet = string.digits + string.ascii_uppercase + string.ascii_lowercase + '-_'
    base64_alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'
    
    b64_to_plantuml = bytes.maketrans(base64_alphabet.encode('utf-8'), plantuml_alphabet.encode('utf-8'))
    return base64.b64encode(compressed).translate(b64_to_plantuml).decode('utf-8')

test_diagram = """@startuml
Alice -> Bob: Test Connection
@enduml"""

try:
    encoded = plantuml_encode(test_diagram)
    url = f"http://www.plantuml.com/plantuml/png/{encoded}"
    print(f"Requesting URL: {url}")
    
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    with urllib.request.urlopen(req) as response:
        content = response.read()
        with open("test_render.png", "wb") as f:
            f.write(content)
    print("Success! test_render.png created successfully. Size:", len(content), "bytes")
except Exception as e:
    print("Failed with exception:", str(e))
