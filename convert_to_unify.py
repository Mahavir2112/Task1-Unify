import json
import uuid
from datetime import datetime

def create_empty_container(display_name):
    return {
        "component": {
            "componentType": "Stack",
            "appearance": {
                "alignItems": "stretch",
                "reverseOrder": False,
                "styles": {
                    "padding": {
                        "all": "p-xl"
                    },
                    "flexWrap": "flex-nowrap",
                    "gap": {
                        "all": "gap-md"
                    },
                    "width": "w-full"
                },
                "theme": "inherit",
                "justifyContent": "flex-start",
                "direction": "row"
            },
            "content": {
                "blockIds": ["__PLACEHOLDER__"]
            }
        },
        "dpOn": [],
        "visibility": {
            "value": False
        },
        "displayName": display_name,
        "additional": {
            "isRootBlock": True
        },
        "dataSourceIds": [],
        "id": str(uuid.uuid4())
    }

def convert_figma_to_ecomponent(figma_data):
    e_component = {
        "cursor": {
            "previous": "eyJmaWx0ZXIiOnsiZmllbGQiOiJwcm9wZXJ0aWVzLm5hbWUiLCJvcCI6IkxUIiwidmFsdWVzIjpbIkhvbWVwYWdlIl19LCJyZXZlcnNlIjp0cnVlfQ=="
        },
        "hasMore": False,
        "objects": [
            {
                "createdTime": int(datetime.now().timestamp() * 1000),
                "deleted": False,
                "entityType": "e_component",
                "id": f"e_{uuid.uuid4().hex}",
                "lastModifiedBy": 522,
                "modifiedTime": int(datetime.now().timestamp() * 1000),
                "ownerUserId": 522,
                "properties": {
                    "layout": {
                        "footer": "footer_id",
                        "header": "header_id",
                        "body": "root_id"
                    },
                    "interfaceType": "application",
                    "componentType": "PAGE",
                    "metadata": {
                        "_blockCounter": {
                            "TextInput": len(figma_data)
                        }
                    },
                    "blocks": {},
                    "name": "Homepage",
                    "flags": {
                        "shouldUseBuiltDependencies": True
                    },
                    "interfaceId": "joey-temp",
                    "dataSources": {},
                    "slug": "homepage",
                    "pageVariables": {}
                },
                "standard": False,
                "version": 3
            }
        ],
        "type": "HITS"
    }

    blocks = e_component["objects"][0]["properties"]["blocks"]
    root_block_ids = []

    # Convert each input field
    for i, input_data in enumerate(figma_data, start=1):
        block_id = f"b_{uuid.uuid4().hex[:6]}"
        root_block_ids.append(block_id)

        style = input_data.get("style", {})
        width = f"{int(style.get('width', 200))}px"
        height = f"{int(style.get('height', 40))}px"

        blocks[block_id] = {
    "component": {
        "componentType": "TextInput",
        "appearance": {
            "size": "md",
            "variant": "outlined",
            "styles": {
                "width": {"custom": width},     # ✅ custom wrapped
                "height": {"custom": height}    # ✅ custom wrapped
            },
            "placeholder": {
                "align": "left"
            },
            "value": {}
        },
        "content": {
            "addOns": {
                "label": {
                    "appearance": {
                        "color": "text-secondary",
                        "variant": "text-sm",
                        "weight": "medium"
                    },
                    "value": input_data.get("label", "")
                }
            },
            "placeholder": input_data.get("placeholder", "")
        }
    },
    "visibility": {"value": True},
    "dpOn": [],
    "displayName": f"TextInput_{i}",
    "dataSourceIds": [],
    "id": block_id,
    "parentId": "root_id"
}


    # Root Stack container block
    blocks["root_id"] = {
        "component": {
            "componentType": "Stack",
            "appearance": {
                "alignItems": "stretch",
                "reverseOrder": False,
                "styles": {
                    "padding": {"all": "p-xl"},
                    "backgroundColor": "bg-workspace",
                    "borderColor": "border-transparent",
                    "flexWrap": "flex-nowrap",
                    "gap": {"all": "gap-md"},
                    "rotation": {"custom": "0deg"},
                    "width": {"custom": "300px"},
                    "height": {"custom": "20%"}
                },
                "theme": "inherit",
                "wrapContent": False,
                "justifyContent": "flex-start",
                "direction": "column"
            },
            "content": {
                "blockIds": root_block_ids + ["__PLACEHOLDER__"]
            }
        },
        "dpOn": [],
        "visibility": {"value": True},
        "displayName": "Body",
        "additional": {"isRootBlock": True},
        "dataSourceIds": [],
        "id": "root_id"
    }

    # Header & Footer placeholder blocks
    blocks["header_id"] = create_empty_container("Header")
    blocks["footer_id"] = create_empty_container("Footer")

    return e_component


# Load figma-extracted input data
with open('text_inputs.json', 'r') as file:
    figma_data = json.load(file)

# Convert and save

converted_data = convert_figma_to_ecomponent(figma_data)
with open('e_component.json', 'w') as file:
    json.dump(converted_data, file, indent=2)

print("✅ Conversion complete. Output saved to e_component.json")
