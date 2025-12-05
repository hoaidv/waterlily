#!/usr/bin/env python3
"""
Generate product definitions, product_def_attributes, and bind categories to product_defs.
Inserts data directly to MySQL instead of generating CSV files.
"""

import csv
import json
import mysql.connector
import os
import random
import argparse

# Load MySQL config
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, '..', 'mysql-config.json')
with open(config_path, 'r') as f:
    mysql_config = json.load(f)

def connect_to_mysql():
    """Connect to MySQL database"""
    return mysql.connector.connect(
        host=mysql_config['host'],
        port=mysql_config['port'],
        user=mysql_config['user'],
        password=mysql_config['password'],
        database=mysql_config['database'],
        charset=mysql_config['charset']
    )

def generate_random_6digit_id(existing_ids):
    """Generate a random 6-digit ID in range [100000, 999999] that doesn't conflict."""
    while True:
        new_id = random.randint(100000, 999999)
        if new_id not in existing_ids:
            return new_id

# Define product definitions with their keywords and attributes
# IDs are hardcoded as random 6-digit numbers
PRODUCT_DEFS = [
    {
        'id': 123456,
        'name': 'Computers and Laptops',
        'keywords': ['computer', 'laptop', 'desktop', 'chromebook', 'macbook', 'netbook', 'tablet', 'ipad', 'all-in-one', 'computing'],
        'attributes': [
            ('brand', 'Brand', 'STRING', 234567),
            ('model', 'Model', 'STRING', 234568),
            ('cpu', 'CPU', 'STRING', 234569),
            ('ram', 'RAM', 'STRING', 234570),
            ('storage', 'Storage', 'STRING', 234571),  # 2G, 1T, 512GB, etc.
            ('storage_type', 'Storage Type', 'STRING', 234572),
            ('screen_size', 'Screen Size', 'NUMBER', 234573),
            ('resolution', 'Resolution', 'STRING', 234574),
            ('operating_system', 'Operating System', 'STRING', 234575),
            ('year', 'Year of Release', 'NUMBER', 234576),
            ('color', 'Color', 'STRING', 234577),
            ('graphics', 'Graphics Card', 'STRING', 234578),
        ]
    },
    {
        'id': 123457,
        'name': 'Phones and Mobile Devices',
        'keywords': ['phone', 'smartphone', 'iphone', 'android', 'mobile device', 'feature phone'],
        'attributes': [
            ('brand', 'Brand', 'STRING', 234579),
            ('model', 'Model', 'STRING', 234580),
            ('color', 'Color', 'STRING', 234581),
            ('storage', 'Storage', 'STRING', 234582),  # 2G, 1T, 512GB, etc.
            ('screen_size', 'Screen Size', 'NUMBER', 234583),
            ('camera', 'Camera', 'STRING', 234584),
            ('battery', 'Battery Capacity', 'NUMBER', 234585),
            ('year', 'Year of Release', 'NUMBER', 234586),
            ('operating_system', 'Operating System', 'STRING', 234587),
            ('network', 'Network', 'STRING', 234588),
        ]
    },
    {
        'id': 123458,
        'name': 'Books and Media',
        'keywords': ['book', 'magazine', 'novel', 'fiction', 'textbook', 'comic', 'manga', 'dvd', 'blu-ray', 'movie', 'tv series', 'music download', 'vinyl', 'cd'],
        'attributes': [
            ('publisher', 'Publisher', 'STRING', 234589),
            ('isbn', 'ISBN', 'STRING', 234590),
            ('author', 'Author', 'STRING', 234591),
            ('format', 'Format', 'STRING', 234592),
            ('language', 'Language', 'STRING', 234593),
            ('pages', 'Pages', 'NUMBER', 234594),
            ('year', 'Year of Release', 'NUMBER', 234595),
            ('genre', 'Genre', 'STRING', 234596),
            ('rating', 'Rating', 'STRING', 234597),
        ],
        'conditional_attributes': [
            {
                'condition': lambda combined: 'magazine' in combined,
                'attributes': [
                    ('issue', 'Issue Number', 'STRING', 234598),
                    ('publication_date', 'Publication Date', 'DATE', 234599),
                ]
            },
            {
                'condition': lambda combined: any(word in combined for word in ['dvd', 'blu-ray', 'movie', 'tv series']),
                'attributes': [
                    ('director', 'Director', 'STRING', 234600),
                    ('runtime', 'Runtime', 'NUMBER', 234601),
                    ('studio', 'Studio', 'STRING', 234602),
                ]
            }
        ]
    },
    {
        'id': 104834,
        'name': 'Clothing and Apparel',
        'keywords': ['shirt', 'pants', 'dress', 'jacket', 'coat', 'shoes', 'sneakers', 'boots', 'sandals', 'heels', 'flats', 'socks', 'underwear', 'lingerie', 'bra', 'panty', 'thong', 'brief', 'boxer', 'jeans', 'shorts', 'skirt', 'top', 'blouse', 'sweater', 'cardigan', 'hoodie', 'vest', 'suit', 'tuxedo', 'swimwear', 'bikini', 'swimsuit', 'activewear', 'yoga', 'leggings', 'tights', 'pantyhose', 'stockings', 'romper', 'jumpsuit', 'bodysuit', 'camisole', 'tunic', 'jegging', 'khaki', 'chino', 'cargo', 'henley', 'polo', 'peacoat', 'bomber', 'trench', 'parka', 'puffer', 'windbreaker', 'board short', 'robe', 'kimono', 'caftan', 'gloves', 'mitten', 'scarf', 'hat', 'cap', 'belt', 'tie', 'bow tie', 'cufflink', 'anklet', 'shapewear', 'maternity', 'clothing'],
        'attributes': [
            ('brand', 'Brand', 'STRING', 101583),
            ('color', 'Color', 'STRING', 103178),
            ('size', 'Size', 'STRING', 103835),
            ('material', 'Material', 'STRING', 103860),
            ('style', 'Style', 'STRING', 104904),
            ('gender', 'Gender', 'STRING', 105235),
        ],
        'conditional_attributes': [
            {
                'condition': lambda combined: any(word in combined for word in ['shoes', 'sneakers', 'boots', 'sandals', 'heels', 'flats']),
                'attributes': [
                    ('width', 'Width', 'STRING', 110427),
                    ('heel_height', 'Heel Height', 'NUMBER', 110820),
                ]
            },
            {
                'condition': lambda combined: any(word in combined for word in ['bra', 'sports bra']),
                'attributes': [
                    ('cup_size', 'Cup Size', 'STRING', 111396),
                    ('band_size', 'Band Size', 'STRING', 114261),
                ]
            },
            {
                'condition': lambda combined: 'suit' in combined or 'tuxedo' in combined,
                'attributes': [
                    ('suit_type', 'Suit Type', 'STRING', 114825),
                    ('fit', 'Fit', 'STRING', 115637),
                ]
            }
        ]
    },
    {
        'id': 130570,
        'name': 'TVs and Displays',
        'keywords': ['tv', 'television', 'monitor', 'display', 'smart tv', 'led tv', 'oled tv', '4k tv', 'ultrawide'],
        'attributes': [
            ('brand', 'Brand', 'STRING', 117511),
            ('model', 'Model', 'STRING', 117815),
            ('screen_size', 'Screen Size', 'NUMBER', 118928),
            ('resolution', 'Resolution', 'STRING', 121224),
            ('refresh_rate', 'Refresh Rate', 'NUMBER', 122007),
            ('smart_features', 'Smart Features', 'BOOLEAN', 124722),
            ('year', 'Year of Release', 'NUMBER', 130173),
            ('connectivity', 'Connectivity', 'STRING', 132790),
        ]
    },
    {
        'id': 193492,
        'name': 'Audio Equipment',
        'keywords': ['headphone', 'earbud', 'speaker', 'soundbar', 'amplifier', 'receiver', 'subwoofer', 'microphone', 'audio interface', 'headphone amp'],
        'attributes': [
            ('brand', 'Brand', 'STRING', 136608),
            ('model', 'Model', 'STRING', 137596),
            ('connectivity', 'Connectivity', 'STRING', 141606),
            ('frequency_response', 'Frequency Response', 'STRING', 142772),
            ('impedance', 'Impedance', 'NUMBER', 147895),
            ('sensitivity', 'Sensitivity', 'NUMBER', 149778),
            ('color', 'Color', 'STRING', 151630),
        ],
        'conditional_attributes': [
            {
                'condition': lambda combined: 'wireless' in combined or 'bluetooth' in combined,
                'attributes': [
                    ('battery_life', 'Battery Life', 'NUMBER', 156784),
                ]
            }
        ]
    },
    {
        'id': 264734,
        'name': 'Cameras',
        'keywords': ['camera', 'lens', 'dslr', 'mirrorless', 'digital camera', 'action camera', 'instant camera', 'film camera', 'point & shoot'],
        'attributes': [
            ('brand', 'Brand', 'STRING', 159999),
            ('model', 'Model', 'STRING', 160926),
            ('megapixels', 'Megapixels', 'NUMBER', 166871),
            ('sensor_size', 'Sensor Size', 'STRING', 169224),
            ('lens_mount', 'Lens Mount', 'STRING', 171658),
            ('video_resolution', 'Video Resolution', 'STRING', 174074),
            ('iso_range', 'ISO Range', 'STRING', 177470),
            ('year', 'Year of Release', 'NUMBER', 183157),
        ]
    },
    {
        'id': 306313,
        'name': 'Gaming Equipment',
        'keywords': ['gaming', 'console', 'xbox', 'playstation', 'nintendo', 'switch', 'controller', 'gaming pc', 'gaming laptop', 'gaming monitor', 'gaming chair', 'gaming headset', 'gaming mouse', 'gaming keyboard', 'racing wheel', 'flight stick', 'vr headset'],
        'attributes': [
            ('brand', 'Brand', 'STRING', 183244),
            ('model', 'Model', 'STRING', 186952),
            ('platform', 'Platform', 'STRING', 190823),
            ('year', 'Year of Release', 'NUMBER', 193118),
        ],
        'conditional_attributes': [
            {
                'condition': lambda combined: 'pc' in combined or 'laptop' in combined,
                'attributes': [
                    ('cpu', 'CPU', 'STRING', 199480),
                    ('gpu', 'GPU', 'STRING', 203337),
                    ('ram', 'RAM', 'STRING', 209200),
                    ('storage', 'Storage', 'STRING', 211874),
                ]
            }
        ]
    },
    {
        'id': 323929,
        'name': 'Storage Devices',
        'keywords': ['hard drive', 'ssd', 'external', 'usb flash', 'memory card', 'sd card', 'microsd', 'nas', 'portable ssd'],
        'attributes': [
            ('brand', 'Brand', 'STRING', 214921),
            ('model', 'Model', 'STRING', 218179),
            ('capacity', 'Capacity', 'NUMBER', 220467),
            ('interface', 'Interface', 'STRING', 221546),
            ('speed', 'Speed', 'NUMBER', 222446),
            ('form_factor', 'Form Factor', 'STRING', 222916),
        ]
    },
    {
        'id': 343967,
        'name': 'Computer Components',
        'keywords': ['cpu', 'processor', 'ram', 'memory', 'motherboard', 'graphics card', 'gpu', 'power supply', 'cooling', 'case', 'chassis'],
        'attributes': [
            ('brand', 'Brand', 'STRING', 223648),
            ('model', 'Model', 'STRING', 224569),
            ('specification', 'Specification', 'STRING', 225049),
            ('compatibility', 'Compatibility', 'JSON', 225309),
            ('form_factor', 'Form Factor', 'STRING', 225310),
        ]
    },
    {
        'id': 355552,
        'name': 'Cables and Adapters',
        'keywords': ['cable', 'adapter', 'charger', 'dongle', 'hub', 'lightning', 'usb-c', 'usb', 'hdmi', 'displayport', 'ethernet', 'audio cable'],
        'attributes': [
            ('brand', 'Brand', 'STRING', 227455),
            ('length', 'Length', 'NUMBER', 229671),
            ('connector_type', 'Connector Type', 'STRING', 233089),
            ('compatibility', 'Compatibility', 'JSON', 233652),
        ]
    },
    {
        'id': 378404,
        'name': 'Smart Home Devices',
        'keywords': ['smart', 'smart home', 'smart lock', 'smart doorbell', 'smart speaker', 'smart display', 'smart bulb', 'smart light', 'smart plug', 'smart thermostat', 'smart sensor', 'smart security', 'smart smoke', 'smart carbon monoxide', 'home hub', 'router', 'modem', 'mesh', 'range extender', 'network switch', 'network adapter'],
        'attributes': [
            ('brand', 'Brand', 'STRING', 235252),
            ('model', 'Model', 'STRING', 240514),
            ('connectivity', 'Connectivity', 'STRING', 242438),
            ('compatibility', 'Compatibility', 'JSON', 243365),
            ('features', 'Features', 'JSON', 246122),
        ]
    },
    {
        'id': 393561,
        'name': 'Wearables',
        'keywords': ['smartwatch', 'fitness tracker', 'wearable', 'smart ring', 'smart glasses'],
        'attributes': [
            ('brand', 'Brand', 'STRING', 253224),
            ('model', 'Model', 'STRING', 253240),
            ('color', 'Color', 'STRING', 254916),
            ('size', 'Size', 'STRING', 255024),
            ('battery_life', 'Battery Life', 'NUMBER', 258328),
            ('compatibility', 'Compatibility', 'JSON', 264860),
            ('features', 'Features', 'JSON', 264968),
        ]
    },
    {
        'id': 410474,
        'name': 'General Electronics',
        'keywords': ['electronic', 'device', 'gadget'],
        'attributes': [
            ('brand', 'Brand', 'STRING', 265812),
            ('model', 'Model', 'STRING', 266848),
            ('color', 'Color', 'STRING', 267175),
            ('year', 'Year of Release', 'NUMBER', 269965),
            ('specifications', 'Specifications', 'JSON', 270226),
        ]
    },
    {
        'id': 433406,
        'name': 'Furniture',
        'keywords': ['furniture', 'chair', 'table', 'desk', 'sofa', 'couch', 'loveseat', 'bed', 'mattress', 'dresser', 'nightstand', 'bookshelf', 'bookcase', 'wardrobe', 'armoire', 'buffet', 'sideboard', 'vanity', 'ottoman', 'recliner', 'accent chair', 'bar stool', 'dining chair', 'dining table', 'coffee table', 'tv stand', 'entertainment center', 'china cabinet', 'chandelier', 'pendant light', 'ceiling light', 'floor lamp', 'table lamp', 'desk lamp', 'wall sconce', 'night light'],
        'attributes': [
            ('brand', 'Brand', 'STRING', 271999),
            ('material', 'Material', 'STRING', 272725),
            ('color', 'Color', 'STRING', 272837),
            ('style', 'Style', 'STRING', 273877),
            ('dimensions', 'Dimensions', 'STRING', 277580),
            ('weight_capacity', 'Weight Capacity', 'NUMBER', 281643),
            ('assembly_required', 'Assembly Required', 'BOOLEAN', 288856),
        ],
        'conditional_attributes': [
            {
                'condition': lambda combined: any(word in combined for word in ['mattress', 'bed']),
                'attributes': [
                    ('size', 'Size', 'STRING', 289406),
                    ('firmness', 'Firmness', 'STRING', 292855),
                    ('type', 'Type', 'STRING', 293950),
                ]
            }
        ]
    },
    {
        'id': 558515,
        'name': 'Kitchen and Dining',
        'keywords': ['kitchen', 'dining', 'cookware', 'pot', 'pan', 'knife', 'utensil', 'appliance', 'coffee maker', 'espresso', 'kettle', 'toaster', 'microwave', 'blender', 'food processor', 'mixer', 'air fryer', 'pressure cooker', 'slow cooker', 'crock pot', 'juicer', 'grill', 'cutting board', 'colander', 'strainer', 'spatula', 'whisk', 'ladle', 'tongs', 'peeler', 'grater', 'zester', 'rolling pin', 'mixing bowl', 'measuring cup', 'scale', 'thermometer', 'timer', 'can opener', 'bottle opener', 'corkscrew', 'pizza cutter', 'cookie cutter', 'cake pan', 'loaf pan', 'muffin tin', 'pie dish', 'bakeware', 'baking sheet', 'cooling rack', 'serving dish', 'bowl', 'plate', 'dinnerware', 'flatware', 'silverware', 'cutlery', 'glassware', 'wine glass', 'champagne flute', 'cocktail glass', 'shot glass', 'beer glass', 'mug', 'cup', 'pitcher', 'carafe', 'teapot', 'sugar bowl', 'butter dish', 'salt pepper', 'napkin ring', 'trivet', 'hot pad', 'oven mitt', 'pot holder', 'apron', 'dish towel', 'dish brush', 'sponge', 'dish soap', 'dish rack', 'sink organizer', 'kitchen storage', 'kitchen gadget', 'kitchen timer', 'french press', 'pour over', 'moka pot', 'cake stand', 'chip dip', 'gravy boat', 'salad spinner', 'ice cream scoop', 'pastry brush', 'piping bag'],
        'attributes': [
            ('brand', 'Brand', 'STRING', 295897),
            ('material', 'Material', 'STRING', 297711),
            ('color', 'Color', 'STRING', 300229),
            ('capacity', 'Capacity', 'NUMBER', 300901),
            ('dimensions', 'Dimensions', 'STRING', 301794),
        ],
        'conditional_attributes': [
            {
                'condition': lambda combined: any(word in combined for word in ['appliance', 'coffee maker', 'espresso', 'kettle', 'toaster', 'microwave', 'blender', 'food processor', 'mixer', 'air fryer', 'pressure cooker', 'slow cooker']),
                'attributes': [
                    ('power', 'Power', 'NUMBER', 303141),
                    ('voltage', 'Voltage', 'NUMBER', 304861),
                    ('features', 'Features', 'JSON', 306100),
                ]
            }
        ]
    },
    {
        'id': 566081,
        'name': 'Bedding and Linens',
        'keywords': ['bedding', 'bed sheet', 'pillow', 'pillowcase', 'comforter', 'duvet', 'blanket', 'throw blanket', 'mattress pad', 'topper', 'bed skirt', 'dust ruffle'],
        'attributes': [
            ('brand', 'Brand', 'STRING', 311609),
            ('material', 'Material', 'STRING', 314229),
            ('color', 'Color', 'STRING', 314406),
            ('size', 'Size', 'STRING', 316722),
            ('thread_count', 'Thread Count', 'NUMBER', 318103),
            ('care_instructions', 'Care Instructions', 'STRING', 320190),
        ]
    },
    {
        'id': 574642,
        'name': 'Bath and Personal Care',
        'keywords': ['bath', 'bathroom', 'towel', 'hand towel', 'washcloth', 'bath mat', 'shower curtain', 'bathroom storage', 'bath accessory', 'soap', 'body wash', 'shampoo', 'conditioner', 'lotion', 'moisturizer', 'face mask', 'serum', 'cleanser', 'toner', 'anti-aging', 'acne treatment', 'sunscreen', 'makeup', 'foundation', 'concealer', 'powder', 'blush', 'bronzer', 'eyeshadow', 'eyeliner', 'mascara', 'lipstick', 'lip gloss', 'makeup brush', 'razor', 'shaving cream', 'shaving', 'deodorant', 'toothpaste', 'toothbrush', 'mouthwash', 'oral care', 'hair care', 'hair color', 'hair styling', 'hair tool', 'hair treatment', 'fragrance', 'perfume', 'cologne', 'body spray', 'personal care', 'beauty', 'skincare'],
        'attributes': [
            ('brand', 'Brand', 'STRING', 936874),
            ('size', 'Size', 'STRING', 547091),
            ('color', 'Color', 'STRING', 198057),
            ('scent', 'Scent', 'STRING', 624042),
            ('skin_type', 'Skin Type', 'STRING', 174522),
        ],
        'conditional_attributes': [
            {
                'condition': lambda combined: any(word in combined for word in ['towel', 'bath mat', 'shower curtain']),
                'attributes': [
                    ('material', 'Material', 'STRING', 370605),
                    ('dimensions', 'Dimensions', 'STRING', 221106),
                ]
            }
        ]
    },
    {
        'id': 585025,
        'name': 'Baby and Kids',
        'keywords': ['baby', 'infant', 'toddler', 'crib', 'stroller', 'car seat', 'high chair', 'changing table', 'playpen', 'play yard', 'activity center', 'baby monitor', 'baby carrier', 'wrap', 'bottle', 'pacifier', 'teether', 'diaper', 'wipe', 'bath', 'sleepwear', 'sleep sack', 'pajama', 'outerwear', 'bodysuit', 'onesie', 'rattle', 'toy', 'kids', 'children', 'girls', 'boys'],
        'attributes': [
            ('brand', 'Brand', 'STRING', 565034),
            ('age_range', 'Age Range', 'STRING', 971707),
            ('color', 'Color', 'STRING', 949201),
            ('size', 'Size', 'STRING', 550602),
            ('safety_features', 'Safety Features', 'STRING', 564346),
        ],
        'conditional_attributes': [
            {
                'condition': lambda combined: any(word in combined for word in ['car seat', 'stroller', 'crib', 'high chair']),
                'attributes': [
                    ('weight_limit', 'Weight Limit', 'NUMBER', 765257),
                    ('dimensions', 'Dimensions', 'STRING', 692077),
                ]
            }
        ]
    },
    {
        'id': 633162,
        'name': 'Sports and Outdoors',
        'keywords': ['sport', 'outdoor', 'fitness', 'exercise', 'gym', 'hiking', 'camping', 'cycling', 'bike', 'bicycle', 'soccer', 'football', 'basketball', 'baseball', 'volleyball', 'tennis', 'golf', 'swimming', 'diving', 'surfing', 'snowboarding', 'skiing', 'ice skating', 'fishing', 'kayaking', 'water sport', 'winter sport', 'team sport', 'equipment', 'treadmill', 'elliptical', 'exercise bike', 'stationary bike', 'yoga mat', 'foam roller', 'resistance band', 'weight', 'dumbbell', 'fitness tracker', 'backpack', 'backpacking', 'tent', 'sleeping bag', 'camping chair', 'hammock', 'hiking boot'],
        'attributes': [
            ('brand', 'Brand', 'STRING', 146440),
            ('sport_type', 'Sport Type', 'STRING', 837542),
            ('size', 'Size', 'STRING', 452422),
            ('color', 'Color', 'STRING', 832109),
            ('material', 'Material', 'STRING', 898794),
        ],
        'conditional_attributes': [
            {
                'condition': lambda combined: any(word in combined for word in ['bike', 'bicycle', 'helmet']),
                'attributes': [
                    ('size', 'Size', 'STRING', 108416),
                    ('age_range', 'Age Range', 'STRING', 230575),
                ]
            }
        ]
    },
    {
        'id': 644299,
        'name': 'Toys and Games',
        'keywords': ['toy', 'game', 'board game', 'card game', 'puzzle', 'doll', 'action figure', 'building set', 'lego', 'die-cast', 'model kit', 'remote control', 'rc', 'pretend play', 'play kitchen', 'role-play', 'stuffed animal', 'plush', 'educational toy', 'musical instrument toy', 'trading card', 'chess', 'poker', 'dart board', 'billiard', 'pool'],
        'attributes': [
            ('brand', 'Brand', 'STRING', 257961),
            ('age_range', 'Age Range', 'STRING', 876382),
            ('number_of_players', 'Number of Players', 'NUMBER', 538838),
            ('material', 'Material', 'STRING', 280858),
        ]
    },
    {
        'id': 662556,
        'name': 'Musical Instruments',
        'keywords': ['guitar', 'bass', 'piano', 'keyboard', 'drum', 'violin', 'viola', 'cello', 'ukulele', 'mandolin', 'banjo', 'harmonica', 'saxophone', 'trumpet', 'trombone', 'tuba', 'flute', 'piccolo', 'clarinet', 'oboe', 'french horn', 'bagpipe', 'organ', 'synthesizer', 'cymbal', 'gong', 'maraca', 'tambourine', 'xylophone', 'glockenspiel', 'bongo', 'conga', 'recorder', 'musical instrument', 'instrument', 'capo', 'tuner', 'metronome', 'music stand', 'guitar stand', 'guitar case', 'gig bag', 'guitar pick', 'guitar string', 'guitar pedal', 'effect pedal', 'amplifier', 'drum stick', 'drum accessory', 'microphone', 'mic stand', 'audio interface', 'midi controller', 'studio monitor', 'pa system', 'turntable', 'vinyl'],
        'attributes': [
            ('brand', 'Brand', 'STRING', 621240),
            ('model', 'Model', 'STRING', 156401),
            ('type', 'Type', 'STRING', 944187),
            ('color', 'Color', 'STRING', 880944),
            ('material', 'Material', 'STRING', 289473),
        ],
        'conditional_attributes': [
            {
                'condition': lambda combined: any(word in combined for word in ['guitar', 'bass', 'violin', 'viola', 'cello']),
                'attributes': [
                    ('size', 'Size', 'STRING', 145166),
                    ('strings', 'Number of Strings', 'NUMBER', 590587),
                ]
            }
        ]
    },
    {
        'id': 666224,
        'name': 'Jewelry',
        'keywords': ['jewelry', 'jewellery', 'ring', 'necklace', 'bracelet', 'earring', 'anklet', 'brooch', 'pin', 'engagement ring', 'wedding band', 'diamond', 'gold', 'silver', 'pearl', 'gemstone', 'fashion jewelry', 'costume jewelry', 'fine jewelry', 'body jewelry', 'piercing', 'jewelry box', 'jewelry set', 'cufflink', 'tie accessory'],
        'attributes': [
            ('brand', 'Brand', 'STRING', 999194),
            ('material', 'Material', 'STRING', 208359),
            ('metal_type', 'Metal Type', 'STRING', 735214),
            ('stone_type', 'Stone Type', 'STRING', 229706),
            ('size', 'Size', 'STRING', 971162),
            ('color', 'Color', 'STRING', 965031),
        ]
    },
    {
        'id': 681972,
        'name': 'Watches and Timepieces',
        'keywords': ['watch', 'timepiece'],
        'attributes': [
            ('brand', 'Brand', 'STRING', 619698),
            ('model', 'Model', 'STRING', 215045),
            ('case_material', 'Case Material', 'STRING', 263967),
            ('band_material', 'Band Material', 'STRING', 958773),
            ('color', 'Color', 'STRING', 956119),
            ('water_resistance', 'Water Resistance', 'STRING', 894126),
            ('movement', 'Movement Type', 'STRING', 387282),
        ]
    },
    {
        'id': 710157,
        'name': 'Bags and Luggage',
        'keywords': ['bag', 'backpack', 'luggage', 'suitcase', 'handbag', 'purse', 'wallet', 'briefcase', 'messenger', 'tote', 'duffel', 'laptop sleeve', 'tablet case', 'camera bag'],
        'attributes': [
            ('brand', 'Brand', 'STRING', 819514),
            ('material', 'Material', 'STRING', 248109),
            ('color', 'Color', 'STRING', 568215),
            ('size', 'Size', 'STRING', 402699),
            ('capacity', 'Capacity', 'NUMBER', 195558),
            ('dimensions', 'Dimensions', 'STRING', 261257),
        ]
    },
    {
        'id': 741425,
        'name': 'Automotive',
        'keywords': ['car', 'automotive', 'auto', 'tire', 'wheel', 'tire pressure', 'car seat', 'car cover', 'car charger', 'car audio', 'car stereo', 'car vacuum', 'car wash', 'car wax', 'car care', 'car accessory', 'car organizer', 'floor mat', 'sun shade', 'dash cam', 'jump starter', 'phone mount', 'hub cap', 'wheel cover', 'motor oil', 'engine oil', 'lubricant', 'car jack', 'tool', 'equipment'],
        'attributes': [
            ('brand', 'Brand', 'STRING', 179917),
            ('compatibility', 'Compatibility', 'JSON', 870256),
            ('material', 'Material', 'STRING', 314480),
            ('color', 'Color', 'STRING', 156094),
        ],
        'conditional_attributes': [
            {
                'condition': lambda combined: 'tire' in combined,
                'attributes': [
                    ('size', 'Size', 'STRING', 984788),
                    ('load_index', 'Load Index', 'NUMBER', 436602),
                    ('speed_rating', 'Speed Rating', 'STRING', 551266),
                ]
            }
        ]
    },
    {
        'id': 761103,
        'name': 'Home and Garden',
        'keywords': ['home', 'garden', 'outdoor', 'patio', 'lawn', 'plant', 'seed', 'bulb', 'pot', 'planter', 'garden hose', 'watering', 'fertilizer', 'garden tool', 'garden statue', 'outdoor furniture', 'patio set', 'outdoor chair', 'outdoor table', 'patio umbrella', 'hammock', 'lounger', 'chaise', 'grill', 'bbq', 'outdoor cooking', 'outdoor decor', 'outdoor play', 'lawn mower', 'storage', 'organization', 'closet organizer', 'drawer organizer', 'desk organizer', 'mail organizer', 'garage storage', 'shelving', 'shelf', 'storage bin', 'container', 'plastic container', 'glass container', 'food storage', 'lunch box', 'lunch container', 'thermos', 'water bottle', 'travel mug', 'cooler', 'ice chest', 'trash can', 'waste bin', 'wastebasket', 'door mat', 'umbrella stand', 'coat rack', 'key holder', 'shoe rack', 'ladder'],
        'attributes': [
            ('brand', 'Brand', 'STRING', 289841),
            ('material', 'Material', 'STRING', 607051),
            ('color', 'Color', 'STRING', 261257),
            ('dimensions', 'Dimensions', 'STRING', 179917),
        ]
    },
    {
        'id': 766907,
        'name': 'Home Decor',
        'keywords': ['decor', 'decoration', 'wall art', 'painting', 'picture frame', 'photo frame', 'mirror', 'vase', 'candle', 'string light', 'led strip', 'led bulb', 'light', 'lamp', 'lighting', 'rug', 'carpet', 'curtain', 'drape', 'blind', 'shade', 'throw pillow', 'blanket', 'throw blanket', 'artificial plant', 'faux plant', 'flower', 'decorative object', 'sculpture', 'clock', 'chandelier'],
        'attributes': [
            ('brand', 'Brand', 'STRING', 870256),
            ('material', 'Material', 'STRING', 314480),
            ('color', 'Color', 'STRING', 156094),
            ('style', 'Style', 'STRING', 984788),
            ('dimensions', 'Dimensions', 'STRING', 436602),
        ]
    },
    {
        'id': 777846,
        'name': 'Office and School Supplies',
        'keywords': ['office', 'school', 'supply', 'pen', 'pencil', 'marker', 'highlighter', 'notebook', 'journal', 'legal pad', 'binder', 'folder', 'stapler', 'staple', 'paper clip', 'tape', 'dispenser', 'scissors', 'calculator', 'ruler', 'eraser', 'sticky note', 'post-it', 'whiteboard', 'bulletin board', 'filing cabinet', 'desk', 'office chair', 'desk lamp', 'book light', 'reading light', 'magazine rack', 'bookshelf', 'bookcase'],
        'attributes': [
            ('brand', 'Brand', 'STRING', 551266),
            ('color', 'Color', 'STRING', 289841),
            ('quantity', 'Quantity', 'NUMBER', 607051),
        ],
        'conditional_attributes': [
            {
                'condition': lambda combined: any(word in combined for word in ['paper', 'notebook', 'binder']),
                'attributes': [
                    ('size', 'Size', 'STRING', 261257),
                    ('pages', 'Number of Pages', 'NUMBER', 179917),
                ]
            }
        ]
    },
    {
        'id': 802547,
        'name': 'Arts and Crafts',
        'keywords': ['art', 'craft', 'paint', 'brush', 'canvas', 'yarn', 'fabric', 'textile', 'sewing', 'knitting', 'crochet', 'needle', 'hook', 'embroidery', 'kit', 'supply'],
        'attributes': [
            ('brand', 'Brand', 'STRING', 870256),
            ('color', 'Color', 'STRING', 314480),
            ('material', 'Material', 'STRING', 156094),
            ('quantity', 'Quantity', 'NUMBER', 984788),
        ]
    },
    {
        'id': 813681,
        'name': 'Pet Supplies',
        'keywords': ['pet', 'dog', 'cat', 'bird', 'fish', 'aquatic', 'small animal', 'hamster', 'collar', 'leash', 'harness', 'bed', 'food', 'treat', 'toy', 'litter', 'box', 'cage', 'aquarium', 'tank', 'filter', 'decor', 'feeder', 'grooming', 'training'],
        'attributes': [
            ('brand', 'Brand', 'STRING', 436602),
            ('pet_type', 'Pet Type', 'STRING', 551266),
            ('size', 'Size', 'STRING', 289841),
            ('age_range', 'Age Range', 'STRING', 607051),
        ],
        'conditional_attributes': [
            {
                'condition': lambda combined: any(word in combined for word in ['food', 'treat']),
                'attributes': [
                    ('flavor', 'Flavor', 'STRING', 261257),
                    ('weight', 'Weight', 'NUMBER', 179917),
                ]
            }
        ]
    },
    {
        'id': 817215,
        'name': 'Health and Wellness',
        'keywords': ['health', 'wellness', 'vitamin', 'supplement', 'multivitamin', 'omega', 'probiotic', 'protein powder', 'weight management', 'pain relief', 'stress relief', 'sleep aid', 'first aid', 'bandage', 'wound care', 'thermometer', 'blood pressure', 'monitor', 'health monitor', 'fitness', 'exercise', 'yoga'],
        'attributes': [
            ('brand', 'Brand', 'STRING', 870256),
            ('quantity', 'Quantity', 'NUMBER', 314480),
            ('dosage', 'Dosage', 'NUMBER', 156094),
            ('form', 'Form', 'STRING', 984788),
        ]
    },
    {
        'id': 845953,
        'name': 'Food and Beverages',
        'keywords': ['food', 'beverage', 'drink', 'coffee', 'tea', 'juice', 'water', 'soda', 'soft drink', 'energy drink', 'sports drink', 'snack', 'candy', 'chocolate', 'cookie', 'cracker', 'chip', 'popcorn', 'nut', 'trail mix', 'granola', 'cereal', 'oatmeal', 'breakfast bar', 'pasta', 'rice', 'grain', 'canned', 'sauce', 'condiment', 'oil', 'vinegar', 'spice', 'seasoning', 'pantry staple', 'breakfast food'],
        'attributes': [
            ('brand', 'Brand', 'STRING', 436602),
            ('flavor', 'Flavor', 'STRING', 551266),
            ('size', 'Size', 'STRING', 289841),
            ('weight', 'Weight', 'NUMBER', 607051),
            ('expiration_date', 'Expiration Date', 'DATE', 261257),
        ]
    },
    {
        'id': 856118,
        'name': 'Cleaning Supplies',
        'keywords': ['cleaning', 'cleaner', 'detergent', 'soap', 'sponge', 'mop', 'broom', 'dustpan', 'vacuum', 'trash', 'waste', 'laundry', 'basket', 'hamper'],
        'attributes': [
            ('brand', 'Brand', 'STRING', 179917),
            ('type', 'Type', 'STRING', 870256),
            ('size', 'Size', 'STRING', 314480),
            ('scent', 'Scent', 'STRING', 156094),
        ]
    },
    {
        'id': 871346,
        'name': 'Tools and Hardware',
        'keywords': ['tool', 'hardware', 'screw', 'nail', 'power tool', 'hand tool', 'tool set', 'kit', 'ladder', 'plumbing', 'electrical', 'paint', 'supply'],
        'attributes': [
            ('brand', 'Brand', 'STRING', 984788),
            ('type', 'Type', 'STRING', 436602),
            ('size', 'Size', 'STRING', 551266),
            ('material', 'Material', 'STRING', 289841),
        ]
    },
    {
        'id': 877848,
        'name': 'Batteries and Power',
        'keywords': ['battery', 'charger', 'power bank', 'rechargeable', 'aa', 'aaa'],
        'attributes': [
            ('brand', 'Brand', 'STRING', 607051),
            ('type', 'Type', 'STRING', 261257),
            ('capacity', 'Capacity', 'NUMBER', 179917),
            ('voltage', 'Voltage', 'NUMBER', 870256),
            ('quantity', 'Quantity', 'NUMBER', 314480),
        ]
    },
    {
        'id': 891476,
        'name': 'Default Product Definition',
        'keywords': [],  # This will match categories that don't match any other product_def
        'attributes': [
            ('brand', 'Brand', 'STRING', 156094),
            ('model', 'Model', 'STRING', 984788),
            ('color', 'Color', 'STRING', 436602),
            ('size', 'Size', 'NUMBER', 551266),
            ('material', 'Material', 'STRING', 289841),
        ]
    }
]


def match_category_to_product_def(category_name, category_description):
    """Match a category to a product_def based on keywords."""
    name_lower = category_name.lower()
    desc_lower = (category_description or '').lower()
    combined = f"{name_lower} {desc_lower}"
    
    # Try to match with product_defs (excluding the default one)
    for product_def in PRODUCT_DEFS[:-1]:  # Exclude default
        keywords = product_def['keywords']
        # Check if any keyword matches in the category name (prioritize name over description)
        if any(keyword in name_lower for keyword in keywords):
            return product_def
        # Check if any keyword matches in the combined name+description
        if any(keyword in combined for keyword in keywords):
            return product_def
    
    # Return default product_def if no match found
    return PRODUCT_DEFS[-1]


def get_attributes_for_product_def(product_def, category_name, category_description):
    """Get all attributes for a product_def, including conditional ones."""
    name_lower = category_name.lower()
    desc_lower = (category_description or '').lower()
    combined = f"{name_lower} {desc_lower}"
    
    attributes = list(product_def['attributes'])
    
    # Add conditional attributes
    if 'conditional_attributes' in product_def:
        for cond_attr in product_def['conditional_attributes']:
            if cond_attr['condition'](combined):
                attributes.extend(cond_attr['attributes'])
    
    # Ensure we have at least 2 and at most 20 attributes
    attributes = attributes[:20]
    if len(attributes) < 2:
        # Generate IDs for default attributes if needed (shouldn't happen with hardcoded IDs)
        attributes.extend([
            ('brand', 'Brand', 'STRING', 999991),
            ('model', 'Model', 'STRING', 999992),
        ])
        attributes = attributes[:20]
    
    return attributes


def assign_random_ids_to_product_defs():
    """IDs are now hardcoded in PRODUCT_DEFS, so this function just validates they exist."""
    for product_def in PRODUCT_DEFS:
        if 'id' not in product_def:
            raise ValueError(f"Product def '{product_def.get('name', 'unknown')}' is missing an 'id' field")
    return set(pd['id'] for pd in PRODUCT_DEFS)

def insert_product_defs(conn):
    """Insert/update product_defs to MySQL using upsert."""
    print("\n=== Inserting/Updating product_defs ===")
    
    cursor = conn.cursor()
    inserted_count = 0
    updated_count = 0
    skipped_count = 0
    
    for product_def in PRODUCT_DEFS:
        product_def_id = product_def['id']
        name = product_def['name']
        
        # Upsert with explicit ID
        insert_sql = "INSERT INTO product_defs (id, name) VALUES (%s, %s) ON DUPLICATE KEY UPDATE name = VALUES(name)"
        
        try:
            cursor.execute(insert_sql, (product_def_id, name))
            if cursor.rowcount == 1:
                inserted_count += 1
                print(f"  Inserted: {name} (ID: {product_def_id})")
            elif cursor.rowcount == 2:
                updated_count += 1
                print(f"  Updated: {name} (ID: {product_def_id})")
        except mysql.connector.Error as e:
            print(f"  Warning: Error upserting {name} (ID: {product_def_id}): {e}")
            skipped_count += 1
    
    conn.commit()
    cursor.close()
    
    print(f"✓ Inserted {inserted_count} product_defs, updated {updated_count} product_defs")
    if skipped_count > 0:
        print(f"  (Skipped {skipped_count} due to errors)")

def insert_product_def_attributes(conn):
    """Insert/update product_def_attributes to MySQL using upsert."""
    print("\n=== Inserting/Updating product_def_attributes ===")
    
    cursor = conn.cursor()
    inserted_count = 0
    updated_count = 0
    skipped_count = 0
    
    for product_def in PRODUCT_DEFS:
        product_def_id = product_def['id']
        
        # Collect all unique attributes with their IDs (base + conditional)
        all_attributes = {}
        
        # Add base attributes
        for attr_tuple in product_def['attributes']:
            if len(attr_tuple) == 4:
                attr_name, attr_display, attr_datatype, attr_id = attr_tuple
            else:
                # Fallback for old format (shouldn't happen with hardcoded IDs)
                attr_name, attr_display, attr_datatype = attr_tuple
                attr_id = None
            all_attributes[attr_name] = (attr_display, attr_datatype, attr_id)
        
        # Add conditional attributes (avoid duplicates)
        if 'conditional_attributes' in product_def:
            for cond_attr in product_def['conditional_attributes']:
                for attr_tuple in cond_attr['attributes']:
                    if len(attr_tuple) == 4:
                        attr_name, attr_display, attr_datatype, attr_id = attr_tuple
                    else:
                        # Fallback for old format
                        attr_name, attr_display, attr_datatype = attr_tuple
                        attr_id = None
                    if attr_name not in all_attributes:
                        all_attributes[attr_name] = (attr_display, attr_datatype, attr_id)
        
        # Insert/update all unique attributes
        for attr_name, (attr_display, attr_datatype, attr_id) in all_attributes.items():
            if attr_id is None:
                # Shouldn't happen with hardcoded IDs, but handle gracefully
                print(f"  Warning: Attribute {attr_name} for product_def_id {product_def_id} has no ID, skipping")
                skipped_count += 1
                continue
                
            insert_sql = """
                INSERT INTO product_def_attributes 
                (id, product_def_id, name, datatype, display_name, default_value, validation_rules)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    product_def_id = VALUES(product_def_id),
                    datatype = VALUES(datatype),
                    display_name = VALUES(display_name),
                    default_value = VALUES(default_value),
                    validation_rules = VALUES(validation_rules)
            """
            
            try:
                cursor.execute(insert_sql, (
                    attr_id,
                    product_def_id,
                    attr_name,
                    attr_datatype,
                    attr_display,
                    None,  # default_value
                    '{}'   # validation_rules
                ))
                if cursor.rowcount == 1:
                    inserted_count += 1
                elif cursor.rowcount == 2:
                    updated_count += 1
            except mysql.connector.Error as e:
                print(f"  Warning: Error upserting {attr_name} (ID: {attr_id}) for product_def_id {product_def_id}: {e}")
                skipped_count += 1
    
    conn.commit()
    cursor.close()
    
    print(f"✓ Inserted {inserted_count} product_def_attributes, updated {updated_count} product_def_attributes")
    if skipped_count > 0:
        print(f"  (Skipped {skipped_count} due to errors)")

def link_categories(conn):
    """Link categories to product_defs by updating product_def_id in categories table."""
    print("\n=== Linking categories to product_defs ===")
    
    cursor = conn.cursor()
    
    # Read categories from database
    cursor.execute("SELECT id, name, description FROM categories")
    categories = cursor.fetchall()
    
    updated_count = 0
    not_found_count = 0
    
    for category_id, category_name, category_description in categories:
        # Match category to product_def
        product_def = match_category_to_product_def(category_name, category_description or '')
        product_def_id = product_def['id']
        
        # Update category
        update_sql = "UPDATE categories SET product_def_id = %s WHERE id = %s"
        cursor.execute(update_sql, (product_def_id, category_id))
        
        if cursor.rowcount > 0:
            updated_count += 1
    
    conn.commit()
    cursor.close()
    
    print(f"✓ Updated {updated_count} categories with product_def_id")
    if not_found_count > 0:
        print(f"  (Could not find {not_found_count} categories)")

def generate_product_defs(flags):
    """Generate and insert product_defs, product_def_attributes, and link categories."""
    
    # Assign random IDs to product_defs
    print("Assigning random IDs to product_defs...")
    assign_random_ids_to_product_defs()
    
    # Print assigned IDs
    print("\nAssigned Product Def IDs:")
    for product_def in PRODUCT_DEFS:
        print(f"  {product_def['id']}: {product_def['name']}")
    
    try:
        conn = connect_to_mysql()
        print("\n✓ Connected to MySQL database")
        
        # Step 1: Insert product_defs
        if 'product_defs' in flags:
            insert_product_defs(conn)
        
        # Step 2: Insert product_def_attributes
        if 'product_def_attributes' in flags:
            insert_product_def_attributes(conn)
        
        # Step 3: Link categories
        if 'link_categories' in flags:
            link_categories(conn)
        
        conn.close()
        
        # Print summary
        print("\n=== SUMMARY ===")
        print(f"Total product_defs: {len(PRODUCT_DEFS)}")
        
        # Count categories per product_def
        if 'link_categories' in flags:
            conn = connect_to_mysql()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT pd.id, pd.name, COUNT(c.id) as category_count
                FROM product_defs pd
                LEFT JOIN categories c ON pd.id = c.product_def_id
                GROUP BY pd.id, pd.name
                ORDER BY category_count DESC
            """)
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            
            print("\nProduct Def Distribution:")
            for row in results:
                print(f"  {row['name']} (ID: {row['id']}): {row['category_count']} categories")
        
        print("\n✓ All operations completed successfully!")
        
    except mysql.connector.Error as e:
        print(f"\n✗ MySQL Error: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate and insert product definitions to MySQL')
    parser.add_argument(
        '--flags',
        type=str,
        default='product_defs,product_def_attributes,link_categories',
        help='Comma-separated list of operations to perform: product_defs, product_def_attributes, link_categories'
    )
    
    args = parser.parse_args()
    
    # Parse flags
    flags = [flag.strip() for flag in args.flags.split(',') if flag.strip()]
    
    if not flags:
        print("Error: No flags specified. Use --flags to specify operations.")
        print("Available flags: product_defs, product_def_attributes, link_categories")
        exit(1)
    
    print(f"Operations to perform: {', '.join(flags)}")
    
    exit(generate_product_defs(flags))

