# PORTRAIT MASTER
# Modifié et traduit en français par Light-x02
# Created by AI Wiz Art (Stefano Flore)
# Version: 3.2.2
# https://stefanoflore.it
# https://ai-wiz.art

import os
import random
import json

script_dir = os.path.dirname(__file__)

########################################################
# Dictionnaire global pour stocker la correspondance
# name -> prompt, par catégorie
########################################################

PROMPTS_MAP = {}

########################################################
# Fonctions de lecture de JSON + extraction
########################################################

def read_json_file(file_path):
    """
    Lit le fichier JSON et retourne son contenu sous forme
    d'objet Python (liste ou dictionnaire).
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            return json_data
    except Exception as e:
        print(f"Une erreur est survenue lors de la lecture du fichier '{file_path}': {str(e)}")
        return []

########################################################
# Fonction utilitaire pour gérer les poids
########################################################

def applyWeight(text, weight):
    """
    Applique un "poids" à un texte selon la syntaxe (monTexte:poids).
    Si le poids est 1, on renvoie simplement le texte sans parenthèses.
    """
    if weight == 1:
        return text
    else:
        return f"({text}:{round(weight,2)})"

########################################################
# Lecture des listes depuis des fichiers JSON
# On crée deux structures :
#   1) lists[name] : liste de STR (les 'name') pour ComfyUI
#   2) PROMPTS_MAP[name][one_name] = correspondance vers 'prompt'
########################################################

rand_opt = 'random 🎲'

def load_lists():
    global PROMPTS_MAP
    lists = {}
    
    # Ajuster ci-dessous la liste de toutes les "catégories" à charger
    list_names = [
        "shot", "gender", "face_shape", "face_expression", "nationality",
        "hair_style", "light_type", "light_direction", "eyes_color",
        "eyes_shape", "beard_color", "hair_color", "hair_length",
        "body_type", "beard", "model_pose", "style", "lips_shape",
        "lips_color", "makeup", "clothes", "age", "makeup_color",
        "female_lingerie"
    ]
    
    for name in list_names:
        list_path = os.path.join(script_dir, f"lists/{name}_list.json")
        data = read_json_file(list_path)
        
        display_names = []
        PROMPTS_MAP[name] = {}
        
        if isinstance(data, list):
            for item in data:
                # item est censé être un dict {"name": "...", "prompt": "..."}
                if isinstance(item, dict) and "name" in item and "prompt" in item:
                    n = item["name"]
                    p = item["prompt"]
                    display_names.append(n)
                    PROMPTS_MAP[name][n] = p
            
            # Tri par ordre alphabétique
            display_names.sort()
        
        lists[name] = display_names
    
    return lists

lists = load_lists()

########################################################
# 1) Portrait Master Base Character
########################################################

class PortraitMasterBaseCharacter:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        max_float_value = 2
        return {
            "optional": {
                "text_in": ("STRING", {"forceInput": True}),
                "seed": ("INT", {"forceInput": True}),
            },
            "required": {
                "prise_de_vue": (['-'] + [rand_opt] + lists['shot'], {
                    "default": '-',
                }),
                "poids_prise_de_vue": ("FLOAT", {
                    "default": 1,
                    "step": 0.05,
                    "min": 0,
                    "max": max_float_value,
                    "display": "slider",
                }),
                "genre": (['-'] + [rand_opt] + lists['gender'], {
                    "default": '-',
                }),
                "androgynie": ("FLOAT", {
                    "default": 0,
                    "min": 0,
                    "max": max_float_value,
                    "step": 0.05,
                    "display": "slider",
                }),
                "laid": ("FLOAT", {
                    "default": 0,
                    "min": 0,
                    "max": max_float_value,
                    "step": 0.05,
                    "display": "slider",
                }),
                "visage_ordinaire": ("FLOAT", {
                    "default": 0,
                    "min": 0,
                    "max": max_float_value,
                    "step": 0.05,
                    "display": "slider",
                }),
                "âge": (['-'] + [rand_opt] + lists['age'], {
                    "default": '-',
                }),
                "nationalite_1": (['-'] + [rand_opt] + lists['nationality'], {
                    "default": '-',
                }),
                "nationalite_2": (['-'] + [rand_opt] + lists['nationality'], {
                    "default": '-',
                }),
                "nationalite_mix": ("FLOAT", {
                    "default": 0.5,
                    "min": 0,
                    "max": 1,
                    "step": 0.05,
                    "display": "slider",
                }),
                "type_corps": (['-'] + [rand_opt] + lists['body_type'], {
                    "default": '-',
                }),
                "poids_type_corps": ("FLOAT", {
                    "default": 1,
                    "step": 0.05,
                    "min": 0,
                    "max": max_float_value,
                    "display": "slider",
                }),
                "couleur_yeux": (['-'] + [rand_opt] + lists['eyes_color'], {
                    "default": '-',
                }),
                "forme_yeux": (['-'] + [rand_opt] + lists['eyes_shape'], {
                    "default": '-',
                }),
                "couleur_lèvres": (['-'] + [rand_opt] + lists['lips_color'], {
                    "default": '-',
                }),
                "forme_lèvres": (['-'] + [rand_opt] + lists['lips_shape'], {
                    "default": '-',
                }),
                "expression_faciale": (['-'] + [rand_opt] + lists['face_expression'], {
                    "default": '-',
                }),
                "poids_expression_faciale": ("FLOAT", {
                    "default": 1,
                    "step": 0.05,
                    "min": 0,
                    "max": max_float_value,
                    "display": "slider",
                }),
                "forme_visage": (['-'] + [rand_opt] + lists['face_shape'], {
                    "default": '-',
                }),
                "poids_forme_visage": ("FLOAT", {
                    "default": 1,
                    "step": 0.05,
                    "min": 0,
                    "max": max_float_value,
                    "display": "slider",
                }),
                "asymetrie_faciale": ("FLOAT", {
                    "default": 0,
                    "min": 0,
                    "max": max_float_value,
                    "step": 0.05,
                    "display": "slider",
                }),
                "style_cheveux": (['-'] + [rand_opt] + lists['hair_style'], {
                    "default": '-',
                }),
                "couleur_cheveux": (['-'] + [rand_opt] + lists['hair_color'], {
                    "default": '-',
                }),
                "longueur_cheveux": (['-'] + [rand_opt] + lists['hair_length'], {
                    "default": '-',
                }),
                "ebouriffe": ("FLOAT", {
                    "default": 0,
                    "min": 0,
                    "max": max_float_value,
                    "step": 0.05,
                    "display": "slider",
                }),
                "barbe": (['-'] + [rand_opt] + lists['beard'], {
                    "default": '-',
                }),
                "couleur_barbe": (['-'] + [rand_opt] + lists['beard_color'], {
                    "default": '-',
                }),
                "active": ("BOOLEAN", {"default": True}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text_out",)

    FUNCTION = "pmbc"

    CATEGORY = "AI WizArt/Portrait Master"

    def pmbc(
            self,
            text_in='',
            seed=0,
            prise_de_vue='-',
            poids_prise_de_vue=1,
            genre='-',
            androgynie=0,
            laid=0,
            visage_ordinaire=0,
            âge='-',
            nationalite_1='-',
            nationalite_2='-',
            nationalite_mix=0.5,
            type_corps='-',
            poids_type_corps=1,
            couleur_yeux='-',
            forme_yeux='-',
            couleur_lèvres='-',
            forme_lèvres='-',
            expression_faciale='-',
            poids_expression_faciale=1,
            forme_visage='-',
            poids_forme_visage=1,
            asymetrie_faciale=0,
            style_cheveux='-',
            couleur_cheveux='-',
            longueur_cheveux='-',
            ebouriffe=0,
            barbe='-',
            couleur_barbe='-',
            active=True
        ):

        # Pour simplifier, on « mappe » nos variables FR vers des variables
        # internes en anglais, afin de réutiliser la logique ci-dessous.
        shot = prise_de_vue
        shot_weight = poids_prise_de_vue
        gender = genre
        androgynous = androgynie
        ugly = laid
        ordinary_face = visage_ordinaire
        age = âge
        body_type = type_corps
        body_type_weight = poids_type_corps
        eyes_color = couleur_yeux
        eyes_shape = forme_yeux
        lips_color = couleur_lèvres
        lips_shape = forme_lèvres
        facial_expression = expression_faciale
        facial_expression_weight = poids_expression_faciale
        face_shape = forme_visage
        face_shape_weight = poids_forme_visage
        facial_asymmetry = asymetrie_faciale
        hair_style = style_cheveux
        hair_color = couleur_cheveux
        hair_length = longueur_cheveux
        disheveled = ebouriffe
        beard = barbe
        beard_color = couleur_barbe

        prompt = []

        # Raccourci pour récupérer le prompt correspondant à un "name"
        def name_to_prompt(category, name_value):
            """
            Retourne le 'prompt' associé au 'name_value' 
            dans la catégorie correspondante, si trouvé.
            Sinon, renvoie le name_value lui-même.
            """
            return PROMPTS_MAP.get(category, {}).get(name_value, name_value)

        if text_in != '':
            prompt.append(text_in)

        if active:

            # Prise de vue (anciennement 'shot')
            if shot_weight > 0:
                if shot == rand_opt:
                    chosen_shot = random.choice(lists['shot'])
                    shot_prompt = name_to_prompt('shot', chosen_shot)
                    prompt.append(applyWeight(shot_prompt, shot_weight))
                elif shot != '-':
                    shot_prompt = name_to_prompt('shot', shot)
                    prompt.append(applyWeight(shot_prompt, shot_weight))

            # Genre
            if gender == rand_opt:
                chosen_gender = random.choice(lists['gender'])
                gender_opt = name_to_prompt('gender', chosen_gender)
            elif gender != '-':
                gender_opt = name_to_prompt('gender', gender)
            else:
                gender_opt = ''

            # Âge
            if age == rand_opt:
                chosen_age = random.choice(lists['age'])
                age_opt = ' ' + name_to_prompt('age', chosen_age) + '-years-old'
            elif age != '-' and age != '':
                # on suppose que la liste 'age' contient des valeurs "30", "40", etc.
                age_opt = ' ' + name_to_prompt('age', str(age)) + '-years-old'
            else:
                age_opt = ''

            # Androgynie
            if androgynous > 0:
                androgynous_opt = applyWeight('androgynous', androgynous) + ' '
            else:
                androgynous_opt = ''

            # Laid
            if ugly > 0:
                ugly_opt = applyWeight('ugly', ugly) + ' '
            else:
                ugly_opt = ''

            # Nationalité(s)
            nationality = ''
            if nationalite_1 != '-' or nationalite_2 != '-':
                if nationalite_1 == rand_opt:
                    chosen_nat1 = random.choice(lists['nationality'])
                    nat1_prompt = name_to_prompt('nationality', chosen_nat1)
                else:
                    nat1_prompt = name_to_prompt('nationality', nationalite_1) if nationalite_1 != '-' else ''

                if nationalite_2 == rand_opt:
                    chosen_nat2 = random.choice(lists['nationality'])
                    nat2_prompt = name_to_prompt('nationality', chosen_nat2)
                else:
                    nat2_prompt = name_to_prompt('nationality', nationalite_2) if nationalite_2 != '-' else ''

                if nat1_prompt and nat2_prompt:
                    mix_val = str(round(nationalite_mix, 2))
                    nationality = f'[{nat1_prompt}:{nat2_prompt}:{mix_val}] '
                else:
                    # si l’une des deux est vide, on prend juste l’autre
                    nationality = (nat1_prompt + ' ') if nat1_prompt else (nat2_prompt + ' ' if nat2_prompt else '')

            # Regroupement (androgynous + ugly + nationality + gender + age)
            combo = androgynous_opt + ugly_opt + nationality + gender_opt + age_opt
            if combo.strip():
                # pour donner un « petit poids » global
                t = f'({combo}:1.15)'
                prompt.append(t.strip())
            
            # Visage ordinaire
            if ordinary_face > 0:
                prompt.append(applyWeight('ordinary face', ordinary_face))

            # Type de corps
            if body_type_weight > 0:
                if body_type == rand_opt:
                    chosen_body = random.choice(lists['body_type'])
                    body_prompt = name_to_prompt('body_type', chosen_body)
                    prompt.append(applyWeight(body_prompt + ' body', body_type_weight))
                elif body_type != '-':
                    body_prompt = name_to_prompt('body_type', body_type)
                    prompt.append(applyWeight(body_prompt + ' body', body_type_weight))

            # Couleur des yeux
            if eyes_color == rand_opt:
                chosen_eyes_color = random.choice(lists['eyes_color'])
                eyes_color_prompt = name_to_prompt('eyes_color', chosen_eyes_color)
                prompt.append("(%s eyes:1.05)" % eyes_color_prompt)
            elif eyes_color != '-':
                eyes_color_prompt = name_to_prompt('eyes_color', eyes_color)
                prompt.append("(%s eyes:1.05)" % eyes_color_prompt)

            # Forme des yeux
            if eyes_shape == rand_opt:
                chosen_eyes_shape = random.choice(lists['eyes_shape'])
                eyes_shape_prompt = name_to_prompt('eyes_shape', chosen_eyes_shape)
                prompt.append(f"({eyes_shape_prompt}:1.05)")
            elif eyes_shape != '-':
                eyes_shape_prompt = name_to_prompt('eyes_shape', eyes_shape)
                prompt.append(f"({eyes_shape_prompt}:1.05)")

            # Couleur des lèvres
            if lips_color == rand_opt:
                chosen_lips_color = random.choice(lists['lips_color'])
                lips_color_prompt = name_to_prompt('lips_color', chosen_lips_color)
                prompt.append(f"({lips_color_prompt}:1.05)")
            elif lips_color != '-':
                lips_color_prompt = name_to_prompt('lips_color', lips_color)
                prompt.append(f"({lips_color_prompt}:1.05)")

            # Forme des lèvres
            if lips_shape == rand_opt:
                chosen_lips_shape = random.choice(lists['lips_shape'])
                lips_shape_prompt = name_to_prompt('lips_shape', chosen_lips_shape)
                prompt.append(f"({lips_shape_prompt}:1.05)")
            elif lips_shape != '-':
                lips_shape_prompt = name_to_prompt('lips_shape', lips_shape)
                prompt.append(f"({lips_shape_prompt}:1.05)")

            # Expression faciale
            if facial_expression_weight > 0:
                if facial_expression == rand_opt:
                    chosen_expr = random.choice(lists['face_expression'])
                    expr_prompt = name_to_prompt('face_expression', chosen_expr)
                    prompt.append(applyWeight(expr_prompt, facial_expression_weight))
                elif facial_expression != '-':
                    expr_prompt = name_to_prompt('face_expression', facial_expression)
                    prompt.append(applyWeight(expr_prompt, facial_expression_weight))

            # Forme du visage
            if face_shape_weight > 0:
                if face_shape == rand_opt:
                    chosen_face_shape = random.choice(lists['face_shape'])
                    face_shape_prompt = name_to_prompt('face_shape', chosen_face_shape)
                    prompt.append(applyWeight(face_shape_prompt + ' face-shape', face_shape_weight))
                elif face_shape != '-':
                    face_shape_prompt = name_to_prompt('face_shape', face_shape)
                    prompt.append(applyWeight(face_shape_prompt + ' face-shape', face_shape_weight))

            # Asymétrie faciale
            if facial_asymmetry > 0:
                prompt.append(applyWeight('facial asymmetry, face asymmetry', facial_asymmetry))

            # Coiffure (style, couleur, longueur)
            if hair_style == rand_opt:
                chosen_hair_style = random.choice(lists['hair_style'])
                hair_style_prompt = name_to_prompt('hair_style', chosen_hair_style)
                prompt.append(f"({hair_style_prompt} hair style:1.05)")
            elif hair_style != '-':
                hair_style_prompt = name_to_prompt('hair_style', hair_style)
                prompt.append(f"({hair_style_prompt} hair style:1.05)")

            if hair_color == rand_opt:
                chosen_hair_color = random.choice(lists['hair_color'])
                hair_color_prompt = name_to_prompt('hair_color', chosen_hair_color)
                prompt.append(f"({hair_color_prompt} hair color:1.05)")
            elif hair_color != '-':
                hair_color_prompt = name_to_prompt('hair_color', hair_color)
                prompt.append(f"({hair_color_prompt} hair color:1.05)")

            if hair_length == rand_opt:
                chosen_hair_length = random.choice(lists['hair_length'])
                hair_length_prompt = name_to_prompt('hair_length', chosen_hair_length)
                prompt.append(f"({hair_length_prompt} hair length:1.05)")
            elif hair_length != '-':
                hair_length_prompt = name_to_prompt('hair_length', hair_length)
                prompt.append(f"({hair_length_prompt} hair length:1.05)")

            if disheveled > 0:
                prompt.append(applyWeight('disheveled', disheveled))

            # Barbe
            if beard == rand_opt:
                chosen_beard = random.choice(lists['beard'])
                beard_prompt = name_to_prompt('beard', chosen_beard)
                prompt.append(f"({beard_prompt}:1.05)")
            elif beard != '-':
                beard_prompt = name_to_prompt('beard', beard)
                prompt.append(f"({beard_prompt}:1.05)")

            if beard_color == rand_opt:
                chosen_beard_color = random.choice(lists['beard_color'])
                beard_color_prompt = name_to_prompt('beard_color', chosen_beard_color)
                prompt.append(f"({beard_color_prompt} beard color:1.05)")
            elif beard_color != '-':
                beard_color_prompt = name_to_prompt('beard_color', beard_color)
                prompt.append(f"({beard_color_prompt} beard color:1.05)")

        if len(prompt) > 0:
            prompt = ', '.join(prompt)
            prompt = prompt.lower()
            return (prompt,)
        else:
            return ('',)

########################################################
# 2) Portrait Master Skin Details
########################################################

class PortraitMasterSkinDetails:

    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        max_float_value = 2
        return {
            "optional": {
                "text_in": ("STRING", {"forceInput": True}),
                "seed": ("INT", {"forceInput": True}),
            },
            "required": {
                "peau_naturelle": ("FLOAT", {
                    "default": 0,
                    "min": 0,
                    "max": max_float_value,
                    "step": 0.05,
                    "display": "slider",
                }),
                "visage_nu": ("FLOAT", {
                    "default": 0,
                    "min": 0,
                    "max": max_float_value,
                    "step": 0.05,
                    "display": "slider",
                }),
                "visage_lave": ("FLOAT", {
                    "default": 0,
                    "min": 0,
                    "max": max_float_value,
                    "step": 0.05,
                    "display": "slider",
                }),
                "visage_seche": ("FLOAT", {
                    "default": 0,
                    "min": 0,
                    "max": max_float_value,
                    "step": 0.05,
                    "display": "slider",
                }),
                "details_peau": ("FLOAT", {
                    "default": 0,
                    "min": 0,
                    "max": max_float_value,
                    "step": 0.05,
                    "display": "slider",
                }),
                "pores_peau": ("FLOAT", {
                    "default": 0,
                    "min": 0,
                    "max": max_float_value,
                    "step": 0.05,
                    "display": "slider",
                }),
                "fossettes": ("FLOAT", {
                    "default": 0,
                    "min": 0,
                    "max": max_float_value,
                    "step": 0.05,
                    "display": "slider",
                }),
                "rides": ("FLOAT", {
                    "default": 0,
                    "min": 0,
                    "max": max_float_value,
                    "step": 0.05,
                    "display": "slider",
                }),
                "taches_rousseur": ("FLOAT", {
                    "default": 0,
                    "min": 0,
                    "max": max_float_value,
                    "step": 0.05,
                    "display": "slider",
                }),
                "grains_de_beaute": ("FLOAT", {
                    "default": 0,
                    "min": 0,
                    "max": max_float_value,
                    "step": 0.05,
                    "display": "slider",
                }),
                "imperfections_peau": ("FLOAT", {
                    "default": 0,
                    "min": 0,
                    "max": max_float_value,
                    "step": 0.05,
                    "display": "slider",
                }),
                "acne_peau": ("FLOAT", {
                    "default": 0,
                    "min": 0,
                    "max": max_float_value,
                    "step": 0.05,
                    "display": "slider",
                }),
                "peau_bronzee": ("FLOAT", {
                    "default": 0,
                    "min": 0,
                    "max": max_float_value,
                    "step": 0.05,
                    "display": "slider",
                }),
                "details_yeux": ("FLOAT", {
                    "default": 0,
                    "min": 0,
                    "max": max_float_value,
                    "step": 0.05,
                    "display": "slider",
                }),
                "details_iris": ("FLOAT", {
                    "default": 0,
                    "min": 0,
                    "max": max_float_value,
                    "step": 0.05,
                    "display": "slider",
                }),
                "iris_circulaire": ("FLOAT", {
                    "default": 0,
                    "min": 0,
                    "max": max_float_value,
                    "step": 0.05,
                    "display": "slider",
                }),
                "pupille_circulaire": ("FLOAT", {
                    "default": 0,
                    "min": 0,
                    "max": max_float_value,
                    "step": 0.05,
                    "display": "slider",
                }),
                "active": ("BOOLEAN", {"default": True}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text_out",)

    FUNCTION = "pmsd"

    CATEGORY = "AI WizArt/Portrait Master"

    def pmsd(
            self,
            text_in='',
            seed=0,
            peau_naturelle=0,
            visage_nu=0,
            visage_lave=0,
            visage_seche=0,
            details_peau=0,
            pores_peau=0,
            fossettes=0,
            rides=0,
            taches_rousseur=0,
            grains_de_beaute=0,
            imperfections_peau=0,
            acne_peau=0,
            peau_bronzee=0,
            details_yeux=0,
            details_iris=0,
            iris_circulaire=0,
            pupille_circulaire=0,
            active=True
    ):
        # Mapping interne
        natural_skin = peau_naturelle
        bare_face = visage_nu
        washed_face = visage_lave
        dried_face = visage_seche
        skin_details = details_peau
        skin_pores = pores_peau
        dimples = fossettes
        wrinkles = rides
        freckles = taches_rousseur
        moles = grains_de_beaute
        skin_imperfections = imperfections_peau
        skin_acne = acne_peau
        tanned_skin = peau_bronzee
        eyes_details = details_yeux
        iris_details = details_iris
        circular_iris = iris_circulaire
        circular_pupil = pupille_circulaire

        prompt = []

        if text_in != '':
            prompt.append(text_in)

        if active:

            if natural_skin > 0:
                prompt.append(applyWeight('natural skin', natural_skin))

            if bare_face > 0:
                prompt.append(applyWeight('bare face', bare_face))

            if washed_face > 0:
                prompt.append(applyWeight('washed-face', washed_face))

            if dried_face > 0:
                prompt.append(applyWeight('dried-face', dried_face))

            if skin_details > 0:
                prompt.append(applyWeight('detailed skin', skin_details))

            if skin_pores > 0:
                prompt.append(applyWeight('skin pores', skin_pores))

            if skin_imperfections > 0:
                prompt.append(applyWeight('skin imperfections', skin_imperfections))

            if skin_acne > 0:
                prompt.append(applyWeight('acne, skin with acne', skin_acne))

            if wrinkles > 0:
                prompt.append(applyWeight('wrinkles', wrinkles))

            if tanned_skin > 0:
                prompt.append(applyWeight('tanned skin', tanned_skin))

            if dimples > 0:
                prompt.append(applyWeight('dimples', dimples))

            if freckles > 0:
                prompt.append(applyWeight('freckles', freckles))

            if moles > 0:
                prompt.append(applyWeight('moles', moles))

            if eyes_details > 0:
                prompt.append(applyWeight('eyes details', eyes_details))

            if iris_details > 0:
                prompt.append(applyWeight('iris details', iris_details))

            if circular_iris > 0:
                prompt.append(applyWeight('circular details', circular_iris))

            if circular_pupil > 0:
                prompt.append(applyWeight('circular pupil', circular_pupil))

        if len(prompt) > 0:
            prompt = ', '.join(prompt)
            prompt = prompt.lower()
            return (prompt,)
        else:
            return ('',)

########################################################
# 3) Portrait Master Style & Pose
########################################################

class PortraitMasterStylePose:

    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        max_float_value = 2
        return {
            "optional": {
                "text_in": ("STRING", {"forceInput": True}),
                "seed": ("INT", {"forceInput": True}),
            },
            "required": {
                "pose_modele": (['-'] + [rand_opt] + lists['model_pose'], {
                    "default": '-',
                }),
                "vetements": (['-'] + [rand_opt] + lists['clothes'], {
                    "default": '-',
                }),
                "lingerie_feminine": (['-'] + [rand_opt] + lists['female_lingerie'], {
                    "default": '-',
                }),
                "maquillage": (['-'] + [rand_opt] + lists['makeup'], {
                    "default": '-',
                }),
                "type_lumiere": (['-'] + [rand_opt] + lists['light_type'], {
                    "default": '-',
                }),
                "direction_lumiere": (['-'] + [rand_opt] + lists['light_direction'], {
                    "default": '-',
                }),
                "poids_lumiere": ("FLOAT", {
                    "default": 1,
                    "min": 0,
                    "max": max_float_value,
                    "step": 0.05,
                    "display": "slider",
                }),
                "style_1": (['-'] + [rand_opt] + lists['style'], {
                    "default": '-',
                }),
                "poids_style_1": ("FLOAT", {
                    "default": 1,
                    "min": 0,
                    "max": max_float_value,
                    "step": 0.05,
                    "display": "slider",
                }),
                "style_2": (['-'] + [rand_opt] + lists['style'], {
                    "default": '-',
                }),
                "poids_style_2": ("FLOAT", {
                    "default": 1,
                    "min": 0,
                    "max": max_float_value,
                    "step": 0.05,
                    "display": "slider",
                }),
                "amelioration_photorealisme": ("BOOLEAN", {"default": True}),
                "active": ("BOOLEAN", {"default": True}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text_out",)

    FUNCTION = "pmsp"

    CATEGORY = "AI WizArt/Portrait Master"

    def pmsp(
            self,
            text_in='',
            seed=0,
            pose_modele='-',
            vetements='-',
            lingerie_feminine='-',
            maquillage='-',
            type_lumiere='-',
            direction_lumiere='-',
            poids_lumiere=1,
            style_1='-',
            poids_style_1=1,
            style_2='-',
            poids_style_2=1,
            amelioration_photorealisme=True,
            active=True
    ):
        # Mapping interne
        model_pose = pose_modele
        clothes = vetements
        female_lingerie = lingerie_feminine
        makeup = maquillage
        light_type = type_lumiere
        light_direction = direction_lumiere
        light_weight = poids_lumiere
        style_1_weight = poids_style_1
        style_2_weight = poids_style_2
        photorealism_improvement = amelioration_photorealisme

        prompt = []

        def name_to_prompt(category, name_value):
            return PROMPTS_MAP.get(category, {}).get(name_value, name_value)

        if text_in != '':
            prompt.append(text_in)

        if active:

            # Maquillage
            if makeup == rand_opt:
                chosen_makeup = random.choice(lists['makeup'])
                mk_prompt = name_to_prompt('makeup', chosen_makeup)
                prompt.append(f"({mk_prompt}:1.05)")
            elif makeup != '-':
                mk_prompt = name_to_prompt('makeup', makeup)
                prompt.append(f"({mk_prompt}:1.05)")

            # Pose du modèle
            if model_pose == rand_opt:
                chosen_pose = random.choice(lists['model_pose'])
                pose_prompt = name_to_prompt('model_pose', chosen_pose)
                prompt.append(f"({pose_prompt}:1.25)")
            elif model_pose != '-':
                pose_prompt = name_to_prompt('model_pose', model_pose)
                prompt.append(f"({pose_prompt}:1.25)")

            # Vêtements
            if clothes == rand_opt:
                chosen_clothes = random.choice(lists['clothes'])
                clothes_prompt = name_to_prompt('clothes', chosen_clothes)
                prompt.append(f"({clothes_prompt}:1.25)")
            elif clothes != '-':
                clothes_prompt = name_to_prompt('clothes', clothes)
                prompt.append(f"({clothes_prompt}:1.25)")

            # Lingerie féminine
            if female_lingerie == rand_opt:
                chosen_lingerie = random.choice(lists['female_lingerie'])
                lingerie_prompt = name_to_prompt('female_lingerie', chosen_lingerie)
                prompt.append(f"({lingerie_prompt}:1.25)")
            elif female_lingerie != '-':
                lingerie_prompt = name_to_prompt('female_lingerie', female_lingerie)
                prompt.append(f"({lingerie_prompt}:1.25)")

            # Lumière
            if light_weight > 0:
                if light_type == rand_opt:
                    chosen_light_type = random.choice(lists['light_type'])
                    light_type_prompt = name_to_prompt('light_type', chosen_light_type)
                    prompt.append(applyWeight(light_type_prompt, light_weight))
                elif light_type != '-':
                    light_type_prompt = name_to_prompt('light_type', light_type)
                    prompt.append(applyWeight(light_type_prompt, light_weight))

                if light_direction == rand_opt:
                    chosen_light_dir = random.choice(lists['light_direction'])
                    light_dir_prompt = name_to_prompt('light_direction', chosen_light_dir)
                    prompt.append(applyWeight(light_dir_prompt, light_weight))
                elif light_direction != '-':
                    light_dir_prompt = name_to_prompt('light_direction', light_direction)
                    prompt.append(applyWeight(light_dir_prompt, light_weight))

            # Styles 1 et 2
            if style_1_weight > 0:
                if style_1 == rand_opt:
                    chosen_style_1 = random.choice(lists['style'])
                    style_1_prompt = name_to_prompt('style', chosen_style_1)
                    prompt.append(applyWeight(style_1_prompt, style_1_weight))
                elif style_1 != '-':
                    style_1_prompt = name_to_prompt('style', style_1)
                    prompt.append(applyWeight(style_1_prompt, style_1_weight))

            if style_2_weight > 0:
                if style_2 == rand_opt:
                    chosen_style_2 = random.choice(lists['style'])
                    style_2_prompt = name_to_prompt('style', chosen_style_2)
                    prompt.append(applyWeight(style_2_prompt, style_2_weight))
                elif style_2 != '-':
                    style_2_prompt = name_to_prompt('style', style_2)
                    prompt.append(applyWeight(style_2_prompt, style_2_weight))

            # Amélioration photoréaliste
            if photorealism_improvement:
                prompt.append('(professional photo, balanced photo, balanced exposure:1.2)')

        if len(prompt) > 0:
            prompt = ', '.join(prompt)
            prompt = prompt.lower()
            return (prompt,)
        else:
            return ('',)

########################################################
# 4) Portrait Master Makeup
########################################################

class PortraitMasterMakeup:

    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        max_float_value = 2
        return {
            "optional": {
                "text_in": ("STRING", {"forceInput": True}),
                "seed": ("INT", {"forceInput": True}),
            },
            "required": {
                "style_maquillage": (['-'] + [rand_opt] + lists['makeup'], {
                    "default": '-',
                }),
                "couleur_maquillage": (['-'] + [rand_opt] + lists['makeup_color'], {
                    "default": '-',
                }),
                "fard_a_paupieres": ("BOOLEAN", {"default": False}),
                "eyeliner": ("BOOLEAN", {"default": False}),
                "mascara": ("BOOLEAN", {"default": False}),
                "blush": ("BOOLEAN", {"default": False}),
                "rouge_a_levres": ("BOOLEAN", {"default": False}),
                "gloss_levres": ("BOOLEAN", {"default": False}),
                "active": ("BOOLEAN", {"default": True}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text_out",)

    FUNCTION = "pmmk"

    CATEGORY = "AI WizArt/Portrait Master"

    def pmmk(
            self,
            text_in='',
            seed=0,
            style_maquillage='-',
            couleur_maquillage='-',
            fard_a_paupieres=False,
            eyeliner=False,
            mascara=False,
            blush=False,
            rouge_a_levres=False,
            gloss_levres=False,
            active=True
    ):
        # Mapping interne
        makeup_style = style_maquillage
        makeup_color = couleur_maquillage
        eyeshadow = fard_a_paupieres
        lipstick = rouge_a_levres
        lip_gloss = gloss_levres

        prompt = []

        def name_to_prompt(category, name_value):
            return PROMPTS_MAP.get(category, {}).get(name_value, name_value)

        if text_in != '':
            prompt.append(text_in)

        if active:

            # Style de maquillage
            if makeup_style == rand_opt:
                chosen_style = random.choice(lists['makeup'])
                style_prompt = name_to_prompt('makeup', chosen_style)
                prompt.append(f"({style_prompt}:1.05)")
            elif makeup_style != '-':
                style_prompt = name_to_prompt('makeup', makeup_style)
                prompt.append(f"({style_prompt}:1.05)")

            # Couleur de maquillage
            if makeup_color == rand_opt:
                chosen_color = random.choice(lists['makeup_color'])
                color_prompt = name_to_prompt('makeup_color', chosen_color)
                prompt.append(f"({color_prompt} make-up color:1.05)")
            elif makeup_color != '-':
                color_prompt = name_to_prompt('makeup_color', makeup_color)
                prompt.append(f"({color_prompt} make-up color:1.05)")

            # Éléments de maquillage
            if eyeshadow:
                prompt.append("(eyeshadow make-up:1.05)")
            if eyeliner:
                prompt.append("(eyeliner make-up:1.05)")
            if mascara:
                prompt.append("(mascara make-up:1.05)")
            if blush:
                prompt.append("(blush make-up:1.05)")
            if lipstick:
                prompt.append("(lipstick make-up:1.05)")
            if lip_gloss:
                prompt.append("(lip gloss make-up:1.05)")

        if len(prompt) > 0:
            prompt = ', '.join(prompt)
            prompt = prompt.lower()
            return (prompt,)
        else:
            return ('',)


NODE_CLASS_MAPPINGS = {
    "PortraitMasterBaseCharacter": PortraitMasterBaseCharacter,
    "PortraitMasterSkinDetails": PortraitMasterSkinDetails,
    "PortraitMasterStylePose": PortraitMasterStylePose,
    "PortraitMasterMakeup": PortraitMasterMakeup
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PortraitMasterBaseCharacter": "Portrait Master : Personnage de base",
    "PortraitMasterSkinDetails": "Portrait Master : Détails de la peau",
    "PortraitMasterStylePose": "Portrait Master : Style & Pose",
    "PortraitMasterMakeup": "Portrait Master : Maquillage"
}
