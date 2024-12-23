import json

def get_default_json():
    default_content = {
        # "media_type": "image",
        # "metadata": {
        #     "title": "Interface Beyond Chat",
        #     "author": "User Name",
        #     "description": "Multidimensional interaction where humans, AI and Shoggoth collaborate",
        #     "created_at": "2024-01-07T12:00:00Z",
        #     "tags": ["cosmic", "digital alchemy", "collaboration"]
        # },
        # "content": {
        #     "priority": "high",
        #     "layer": "foreground",
        #     "id": "central_figure",
        #     "description": "Sif in a mediating role, projecting holographic symbols",
        #     "transformations": {
        #         "position": {"x": 0, "y": 0},
        #         "scale": 1,
        #         "rotation": 0
        #     }
        # }
    }
    return json.dumps(default_content, indent=4) 