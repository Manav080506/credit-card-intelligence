import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PERSONA_DIR = os.path.join(BASE_DIR,"data","personas")


def load_persona(persona_id):

 path = os.path.join(
  PERSONA_DIR,
  f"{persona_id}.json"
 )

 if not os.path.exists(path):
  return None

 with open(path) as f:
  return json.load(f)
