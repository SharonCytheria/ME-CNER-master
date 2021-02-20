from process_character.constants import Dataset
from process_character.load_drink_indexes import \
    load_character_indexes, \
    load_phrase_indexes, \
    load_label_indexes

character_dict = {}
phrase_dict = {}
label_dict = {}

if not character_dict:
    character_dict = load_character_indexes()

if not phrase_dict:
    phrase_dict = load_phrase_indexes()

if not label_dict:
    label_dict = load_label_indexes()
