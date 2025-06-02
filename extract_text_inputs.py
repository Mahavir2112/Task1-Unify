import json
from typing import Dict, List, Optional

def extract_text_inputs(figma_json: Dict) -> List[Dict]:
    text_inputs = []
    nodes = figma_json.get('Result', {}).get('nodes', {})
    
    for node_id, node_data in nodes.items():
        if 'document' in node_data:
            inputs = _traverse_node(node_data['document'])
            text_inputs.extend(inputs)
    
    return text_inputs

def _traverse_node(node: Dict) -> List[Dict]:
    inputs = []
    if _is_text_input(node):
        input_data = _extract_input_properties(node)
        if input_data:
            inputs.append(input_data)

    for child in node.get('children', []):
        inputs.extend(_traverse_node(child))
    
    return inputs

def _is_text_input(node: Dict) -> bool:
    name = node.get('name', '').lower()
    component_id = node.get('componentId', '')
    return (
        'input' in name and 'field' in name or 
        'textarea' in name or
        component_id in ['1:8266', '146:7190', '146:6293']
    )

def _extract_input_properties(node: Dict) -> Optional[Dict]:
    input_props = {
        'name': node.get('name', ''),
        'type': node.get('type', ''),
        'component_id': node.get('componentId', ''),
        'label': '',
        'placeholder': '',
        'hint': '',
        'value': '',
        'properties': node.get('componentProperties', {}),
        'style': {}
    }

    # Try to get bounding box (for width & height)
    bbox = node.get('absoluteBoundingBox', {})
    if bbox:
        input_props['style'] = {
            'width': bbox.get('width', 0),
            'height': bbox.get('height', 0)
        }

    # Look through children for text content
    for child in node.get('children', []):
        name = child.get('name', '').lower()
        characters = child.get('characters', '')

        if 'label' in name and child.get('type') == 'TEXT':
            input_props['label'] = characters
        elif ('placeholder' in name or 'text' in name) and 'hint' not in name and child.get('type') == 'TEXT':
            input_props['placeholder'] = characters
        elif ('hint' in name or 'supporting' in name) and child.get('type') == 'TEXT':
            input_props['hint'] = characters
        elif 'children' in child:
            for grandchild in child['children']:
                gname = grandchild.get('name', '').lower()
                gtext = grandchild.get('characters', '')

                if 'label' in gname and grandchild.get('type') == 'TEXT':
                    input_props['label'] = gtext
                elif ('placeholder' in gname or 'text' in gname) and 'hint' not in gname and grandchild.get('type') == 'TEXT':
                    input_props['placeholder'] = gtext
                elif ('hint' in gname or 'supporting' in gname) and grandchild.get('type') == 'TEXT':
                    input_props['hint'] = gtext
    
    return input_props

def main():
    with open('figma_response.json', 'r', encoding='utf-8') as f:
        figma_data = json.load(f)

    text_inputs = extract_text_inputs(figma_data)

    with open('text_inputs.json', 'w', encoding='utf-8') as f:
        json.dump(text_inputs, f, indent=2)

    print(f"Extracted {len(text_inputs)} text inputs with styling.")
    if text_inputs:
        print("Sample:", json.dumps(text_inputs[0], indent=2))

if __name__ == '__main__':
    main()
