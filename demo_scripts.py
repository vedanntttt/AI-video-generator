"""
Demo Scripts for AI Video Generator
Contains sample scripts that users can use to test the application
"""

DEMO_SCRIPTS = {
    "Space Adventure": {
        "script": """A brave astronaut discovers a mysterious planet.
The planet is covered in glowing purple crystals.
Strange alien creatures emerge from crystal caves.
The astronaut makes peaceful contact with the aliens.
They share knowledge about the universe together.
The astronaut returns to Earth with new wisdom.""",
        "description": "A short space adventure story perfect for testing the video generator"
    },
    
    "Ocean Discovery": {
        "script": """A marine biologist dives into the deep ocean.
Colorful coral reefs stretch as far as the eye can see.
Schools of tropical fish swim in perfect harmony.
A giant whale appears majestically in the distance.
The biologist discovers a new species of seahorse.
The underwater world reveals its hidden treasures.""",
        "description": "An underwater exploration story with beautiful ocean scenes"
    },
    
    "Forest Magic": {
        "script": """A young explorer enters an enchanted forest.
Ancient trees tower high into the misty sky.
Magical fireflies dance between the branches.
A wise old owl shares secrets of the forest.
Hidden fairy houses appear among the mushrooms.
The explorer leaves with a heart full of wonder.""",
        "description": "A magical forest adventure with mystical elements"
    },
    
    "City Innovation": {
        "script": """A brilliant inventor works in their laboratory.
Futuristic gadgets and robots fill the workspace.
The inventor creates a device to clean the oceans.
The invention is tested in polluted waters.
Marine life returns to the cleaned areas.
The world celebrates this environmental breakthrough.""",
        "description": "A futuristic story about innovation and environmental protection"
    },
    
    "Mountain Journey": {
        "script": """A hiker begins climbing a majestic mountain.
Snow-capped peaks stretch across the horizon.
The hiker encounters friendly mountain animals.
A beautiful sunrise illuminates the summit.
The view from the top is breathtakingly spectacular.
The hiker descends with renewed appreciation for nature.""",
        "description": "An inspiring mountain climbing adventure"
    }
}

def get_demo_script(title: str) -> str:
    """Get a demo script by title"""
    if title in DEMO_SCRIPTS:
        return DEMO_SCRIPTS[title]["script"]
    return ""

def get_all_demo_titles() -> list:
    """Get all demo script titles"""
    return list(DEMO_SCRIPTS.keys())

def get_demo_description(title: str) -> str:
    """Get demo script description"""
    if title in DEMO_SCRIPTS:
        return DEMO_SCRIPTS[title]["description"]
    return ""