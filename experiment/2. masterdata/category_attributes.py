"""
Category attributes mapping
Generated automatically from categories.csv
Each category has been analyzed individually to generate specific, relevant attributes.
"""

CATEGORY_ATTRIBUTES = [
  {
    # Hangers
    'id': 100953,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('quantity', 'NUMBER', 'Quantity in pack'),
      ('type', 'STRING', 'Type (Plastic, Wood, Velvet)'),
    ]
  },
  {
    # AA Batteries
    'id': 102105,
    'attributes': [
      ('voltage', 'STRING', 'Voltage per cell (typically 1.5V)'),
      ('chemistry', 'STRING', 'Battery chemistry (Alkaline, Lithium, etc.)'),
      ('quantity', 'NUMBER', 'Number of batteries in pack'),
      ('rechargeable', 'BOOLEAN', 'Rechargeable'),
      ('brand', 'STRING', 'Brand name'),
      ('expiration_date', 'STRING', 'Expiration date'),
    ]
  },
  {
    # Sugar Bowls
    'id': 102964,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material (Ceramic, Glass, Silver)'),
      ('capacity', 'STRING', 'Capacity'),
      ('color', 'STRING', 'Color'),
      ('dishwasher_safe', 'BOOLEAN', 'Dishwasher safe'),
      ('quantity', 'NUMBER', 'Quantity in set'),
    ]
  },
  {
    # Embroidery Kits
    'id': 104221,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('design', 'STRING', 'Design/Pattern'),
      ('difficulty_level', 'STRING', 'Difficulty level'),
      ('includes', 'STRING', 'What\'s included'),
      ('finished_size', 'STRING', 'Finished size'),
    ]
  },
  {
    # Baby Bottles
    'id': 104302,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Bottle size (oz)'),
      ('material', 'STRING', 'Material (Glass, Plastic, Silicone)'),
      ('nipple_type', 'STRING', 'Nipple type'),
      ('age_range', 'STRING', 'Age range'),
      ('bpa_free', 'BOOLEAN', 'BPA-free'),
      ('dishwasher_safe', 'BOOLEAN', 'Dishwasher safe'),
    ]
  },
  {
    # External Hard Drives
    'id': 105562,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('capacity', 'STRING', 'Storage capacity'),
      ('type', 'STRING', 'Type (HDD, SSD, NVMe)'),
      ('interface', 'STRING', 'Interface (USB 3.0, USB-C, Thunderbolt)'),
      ('form_factor', 'STRING', 'Form factor'),
      ('speed', 'STRING', 'Read/Write speed'),
    ]
  },
  {
    # Educational Toys
    'id': 105841,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('age_range', 'STRING', 'Age range'),
      ('type', 'STRING', 'Type'),
    ]
  },
  {
    # Women's Lingerie
    'id': 106741,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Mesh Wi-Fi Systems
    'id': 107613,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('wifi_standard', 'STRING', 'Wi-Fi standard'),
      ('coverage_area', 'STRING', 'Coverage area (sq ft)'),
      ('number_of_nodes', 'NUMBER', 'Number of nodes'),
      ('speed', 'STRING', 'Speed (Mbps)'),
    ]
  },
  {
    # Bike Accessories
    'id': 108820,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('type', 'STRING', 'Type (Mountain, Road, Hybrid, etc.)'),
      ('frame_size', 'STRING', 'Frame size'),
      ('wheel_size', 'STRING', 'Wheel size'),
      ('number_of_speeds', 'NUMBER', 'Number of speeds'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Men's Khakis
    'id': 109173,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('waist_size', 'STRING', 'Waist size'),
      ('inseam', 'STRING', 'Inseam length'),
      ('fit', 'STRING', 'Fit type'),
      ('rise', 'STRING', 'Rise'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
    ]
  },
  {
    # Women's Sneakers
    'id': 111131,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size (US)'),
      ('width', 'STRING', 'Width'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('style', 'STRING', 'Style'),
      ('closure', 'STRING', 'Closure type'),
      ('heel_height', 'STRING', 'Heel height'),
    ]
  },
  {
    # Books
    'id': 112551,
    'attributes': [
      ('title', 'STRING', 'Book title'),
      ('author', 'STRING', 'Author name'),
      ('publisher', 'STRING', 'Publisher'),
      ('isbn', 'STRING', 'ISBN-13 or ISBN-10'),
      ('publication_date', 'STRING', 'Publication date'),
      ('language', 'STRING', 'Language'),
      ('format', 'STRING', 'Format (Hardcover, Paperback, eBook, Audiobook)'),
      ('pages', 'NUMBER', 'Number of pages'),
      ('genre', 'STRING', 'Genre'),
      ('edition', 'STRING', 'Edition number'),
    ]
  },
  {
    # Baby Gear
    'id': 112991,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('age_range', 'STRING', 'Age range'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('safety_certification', 'STRING', 'Safety certification'),
    ]
  },
  {
    # Women's Wide Leg Pants
    'id': 113434,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('waist_size', 'STRING', 'Waist size'),
      ('inseam', 'STRING', 'Inseam length'),
      ('fit', 'STRING', 'Fit type'),
      ('rise', 'STRING', 'Rise'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
    ]
  },
  {
    # Backpacks School
    'id': 113709,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('capacity', 'STRING', 'Capacity (liters)'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('number_of_compartments', 'NUMBER', 'Number of compartments'),
      ('laptop_compartment', 'BOOLEAN', 'Laptop compartment'),
      ('water_resistant', 'BOOLEAN', 'Water resistant'),
    ]
  },
  {
    # Men's Athletic Shirts
    'id': 113980,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('sleeve_length', 'STRING', 'Sleeve length'),
      ('fit', 'STRING', 'Fit type'),
      ('style', 'STRING', 'Style'),
    ]
  },
  {
    # Mystery & Thriller
    'id': 114859,
    'attributes': [
      ('title', 'STRING', 'Book title'),
      ('author', 'STRING', 'Author name'),
      ('publisher', 'STRING', 'Publisher'),
      ('isbn', 'STRING', 'ISBN'),
      ('publication_date', 'STRING', 'Publication date'),
      ('language', 'STRING', 'Language'),
      ('format', 'STRING', 'Format (Hardcover, Paperback, eBook)'),
      ('pages', 'NUMBER', 'Number of pages'),
      ('series', 'STRING', 'Series name (if part of a series)'),
    ]
  },
  {
    # GPS Navigation
    'id': 115300,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('type', 'STRING', 'Type (Portable, Built-in)'),
      ('maps_included', 'BOOLEAN', 'Maps included'),
      ('lifetime_updates', 'BOOLEAN', 'Lifetime map updates'),
    ]
  },
  {
    # Teapots
    'id': 117082,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('capacity', 'STRING', 'Capacity (liters)'),
      ('material', 'STRING', 'Material (Stainless Steel, Glass, etc.)'),
      ('color', 'STRING', 'Color'),
      ('cordless', 'BOOLEAN', 'Cordless'),
      ('temperature_control', 'BOOLEAN', 'Temperature control'),
    ]
  },
  {
    # Car Seat Covers
    'id': 117777,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('fit', 'STRING', 'Fit type'),
      ('washable', 'BOOLEAN', 'Washable'),
    ]
  },
  {
    # Glassware
    'id': 119211,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('capacity', 'STRING', 'Capacity (oz)'),
      ('dishwasher_safe', 'BOOLEAN', 'Dishwasher safe'),
      ('microwave_safe', 'BOOLEAN', 'Microwave safe'),
      ('quantity', 'NUMBER', 'Quantity in set'),
    ]
  },
  {
    # Electronics
    'id': 119229,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Home Theater Systems
    'id': 120084,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Nursery Gliders
    'id': 120389,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('dimensions', 'STRING', 'Dimensions'),
      ('weight_capacity', 'STRING', 'Weight capacity'),
      ('assembly_required', 'BOOLEAN', 'Assembly required'),
    ]
  },
  {
    # LED TVs
    'id': 121025,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('resolution', 'STRING', 'Resolution (4K, 1080p, 8K)'),
      ('display_type', 'STRING', 'Display type (LED, OLED, QLED)'),
      ('refresh_rate', 'STRING', 'Refresh rate (Hz)'),
      ('smart_tv', 'BOOLEAN', 'Smart TV features'),
      ('hdr', 'BOOLEAN', 'HDR support'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Coffee Makers
    'id': 121526,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('capacity', 'STRING', 'Capacity (cups)'),
      ('type', 'STRING', 'Type (Drip, Espresso, French Press, etc.)'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('programmable', 'BOOLEAN', 'Programmable'),
    ]
  },
  {
    # Wireless Mice
    'id': 121917,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Men's Peacoats
    'id': 122657,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Anti-Aging
    'id': 123360,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Soccer
    'id': 126707,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Ball size'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('indoor_outdoor', 'STRING', 'Indoor/Outdoor'),
    ]
  },
  {
    # Omega-3
    'id': 126928,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Brooches
    'id': 127861,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (Straight, Quilting)'),
      ('length', 'STRING', 'Length'),
      ('count', 'NUMBER', 'Number of pins'),
    ]
  },
  {
    # USB Flash Drives
    'id': 129317,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('capacity', 'STRING', 'Storage capacity'),
      ('type', 'STRING', 'USB type (USB 2.0, USB 3.0, USB-C)'),
      ('transfer_speed', 'STRING', 'Transfer speed'),
    ]
  },
  {
    # Girls' Tops
    'id': 129954,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('age_range', 'STRING', 'Age range'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Coffee
    'id': 130377,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('roast_level', 'STRING', 'Roast level (Light, Medium, Dark)'),
      ('origin', 'STRING', 'Origin'),
      ('weight', 'STRING', 'Weight'),
      ('grind', 'STRING', 'Grind (Whole Bean, Ground)'),
      ('flavor_notes', 'STRING', 'Flavor notes'),
    ]
  },
  {
    # Kettles
    'id': 130950,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('capacity', 'STRING', 'Capacity (liters)'),
      ('material', 'STRING', 'Material (Stainless Steel, Glass, etc.)'),
      ('color', 'STRING', 'Color'),
      ('cordless', 'BOOLEAN', 'Cordless'),
      ('temperature_control', 'BOOLEAN', 'Temperature control'),
    ]
  },
  {
    # Women's Suits
    'id': 131164,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Volleyball
    'id': 131229,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Ball size'),
      ('material', 'STRING', 'Material'),
      ('indoor_outdoor', 'STRING', 'Indoor/Outdoor'),
    ]
  },
  {
    # Cookie Cutters
    'id': 132148,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Candy
    'id': 132658,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('flavor', 'STRING', 'Flavor'),
      ('package_size', 'STRING', 'Package size'),
      ('weight', 'STRING', 'Weight'),
      ('ingredients', 'STRING', 'Ingredients'),
      ('allergens', 'STRING', 'Allergen information'),
    ]
  },
  {
    # Women's Tunics
    'id': 132737,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('sleeve_length', 'STRING', 'Sleeve length'),
      ('fit', 'STRING', 'Fit type'),
      ('style', 'STRING', 'Style'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Girls' Dresses
    'id': 133807,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('age_range', 'STRING', 'Age range'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Guitar Cases
    'id': 134144,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # RAM Memory
    'id': 135745,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('capacity', 'STRING', 'Memory capacity'),
      ('type', 'STRING', 'Type (DDR4, DDR5)'),
      ('speed', 'STRING', 'Speed (MHz)'),
      ('form_factor', 'STRING', 'Form factor'),
    ]
  },
  {
    # Diving
    'id': 136060,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Men's Briefs
    'id': 139564,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Cymbals
    'id': 140396,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Die-Cast Models
    'id': 141217,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('age_range', 'STRING', 'Age range'),
      ('material', 'STRING', 'Material'),
      ('batteries_required', 'BOOLEAN', 'Batteries required'),
      ('number_of_players', 'STRING', 'Number of players'),
      ('theme', 'STRING', 'Theme'),
    ]
  },
  {
    # Tech Magazines
    'id': 141541,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Mandolins
    'id': 142011,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Fiction Books
    'id': 144170,
    'attributes': [
      ('title', 'STRING', 'Book title'),
      ('author', 'STRING', 'Author name'),
      ('publisher', 'STRING', 'Publisher'),
      ('isbn', 'STRING', 'ISBN-13 or ISBN-10'),
      ('publication_date', 'STRING', 'Publication date'),
      ('language', 'STRING', 'Language'),
      ('format', 'STRING', 'Format (Hardcover, Paperback, eBook, Audiobook)'),
      ('pages', 'NUMBER', 'Number of pages'),
      ('genre', 'STRING', 'Genre'),
      ('edition', 'STRING', 'Edition number'),
    ]
  },
  {
    # Aprons
    'id': 144914,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Sink Organizers
    'id': 145678,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('dimensions', 'STRING', 'Dimensions'),
      ('number_of_compartments', 'NUMBER', 'Number of compartments'),
    ]
  },
  {
    # Champagne Flutes
    'id': 146975,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('type', 'STRING', 'Type'),
      ('key', 'STRING', 'Key'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color/Finish'),
    ]
  },
  {
    # Women's Cocktail Dresses
    'id': 147085,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's Shoes
    'id': 147222,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size (US)'),
      ('width', 'STRING', 'Width'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('style', 'STRING', 'Style'),
      ('closure', 'STRING', 'Closure type'),
      ('heel_height', 'STRING', 'Heel height'),
    ]
  },
  {
    # Bass Guitars
    'id': 147413,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('type', 'STRING', 'Type (Acoustic, Electric, Bass)'),
      ('color', 'STRING', 'Color/Finish'),
      ('number_of_strings', 'NUMBER', 'Number of strings'),
      ('body_material', 'STRING', 'Body material'),
      ('scale_length', 'STRING', 'Scale length'),
    ]
  },
  {
    # Door Mats
    'id': 148389,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Camera Flash
    'id': 149243,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('guide_number', 'STRING', 'Guide number'),
      ('compatibility', 'STRING', 'Camera compatibility'),
      ('ttl', 'BOOLEAN', 'TTL support'),
      ('battery_type', 'STRING', 'Battery type'),
    ]
  },
  {
    # Sticky Notes
    'id': 150753,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('quantity', 'NUMBER', 'Quantity per pack'),
      ('pack_count', 'NUMBER', 'Number of packs'),
    ]
  },
  {
    # Tires & Wheels
    'id': 151037,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Bedroom Furniture
    'id': 151572,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color/Finish'),
      ('dimensions', 'STRING', 'Dimensions (L x W x H)'),
      ('assembly_required', 'BOOLEAN', 'Assembly required'),
      ('style', 'STRING', 'Style'),
    ]
  },
  {
    # Shower Curtains
    'id': 151906,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('pattern', 'STRING', 'Pattern'),
      ('light_blocking', 'BOOLEAN', 'Light blocking'),
    ]
  },
  {
    # Building Materials
    'id': 152159,
    'attributes': [
      ('material', 'STRING', 'Material'),
    ]
  },
  {
    # Food Storage Containers
    'id': 153013,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('dimensions', 'STRING', 'Dimensions'),
      ('number_of_compartments', 'NUMBER', 'Number of compartments'),
    ]
  },
  {
    # Gaming Monitors
    'id': 154041,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('resolution', 'STRING', 'Resolution'),
      ('refresh_rate', 'STRING', 'Refresh rate (Hz)'),
      ('response_time', 'STRING', 'Response time (ms)'),
      ('panel_type', 'STRING', 'Panel type (IPS, VA, TN)'),
      ('curved', 'BOOLEAN', 'Curved display'),
    ]
  },
  {
    # Music Accessories
    'id': 154680,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Markers
    'id': 154799,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (Desk, Floor, Table)'),
      ('bulb_type', 'STRING', 'Bulb type'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('dimmable', 'BOOLEAN', 'Dimmable'),
    ]
  },
  {
    # Women's Dress Shorts
    'id': 154966,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('length', 'STRING', 'Dress length'),
      ('sleeve_length', 'STRING', 'Sleeve length'),
      ('style', 'STRING', 'Style'),
      ('occasion', 'STRING', 'Occasion'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Body Wash
    'id': 155086,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Living Room Furniture
    'id': 155274,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color/Finish'),
      ('dimensions', 'STRING', 'Dimensions (L x W x H)'),
      ('assembly_required', 'BOOLEAN', 'Assembly required'),
      ('style', 'STRING', 'Style'),
    ]
  },
  {
    # Travel Mugs
    'id': 156447,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('capacity', 'STRING', 'Capacity (oz)'),
      ('insulated', 'BOOLEAN', 'Insulated'),
      ('leak_proof', 'BOOLEAN', 'Leak-proof'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Sponges
    'id': 156461,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Stress Relief
    'id': 156573,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's Tights
    'id': 157348,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Car Seats
    'id': 157864,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('age_range', 'STRING', 'Age range'),
      ('weight_range', 'STRING', 'Weight range'),
      ('installation_type', 'STRING', 'Installation type'),
      ('safety_rating', 'STRING', 'Safety rating'),
    ]
  },
  {
    # Cookies
    'id': 157985,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Loveseats
    'id': 158015,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material (Fabric, Leather, etc.)'),
      ('color', 'STRING', 'Color'),
      ('seating_capacity', 'NUMBER', 'Seating capacity'),
      ('dimensions', 'STRING', 'Dimensions (L x W x H)'),
      ('assembly_required', 'BOOLEAN', 'Assembly required'),
      ('style', 'STRING', 'Style'),
    ]
  },
  {
    # Storage & Organization
    'id': 160194,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('dimensions', 'STRING', 'Dimensions'),
      ('number_of_compartments', 'NUMBER', 'Number of compartments'),
    ]
  },
  {
    # Trivets
    'id': 160220,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Oral Care
    'id': 161772,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's Thongs
    'id': 161867,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Pots & Planters
    'id': 161998,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('size', 'STRING', 'Size/Diameter'),
      ('capacity', 'STRING', 'Capacity'),
      ('non_stick', 'BOOLEAN', 'Non-stick coating'),
      ('dishwasher_safe', 'BOOLEAN', 'Dishwasher safe'),
      ('induction_compatible', 'BOOLEAN', 'Induction compatible'),
    ]
  },
  {
    # Gaming PCs
    'id': 162131,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('processor', 'STRING', 'CPU processor'),
      ('ram', 'STRING', 'RAM size'),
      ('storage', 'STRING', 'Storage capacity'),
      ('storage_type', 'STRING', 'Storage type (SSD, HDD)'),
      ('graphics_card', 'STRING', 'Graphics card (GPU)'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('refresh_rate', 'STRING', 'Refresh rate (Hz)'),
      ('resolution', 'STRING', 'Display resolution'),
      ('operating_system', 'STRING', 'Operating system'),
      ('color', 'STRING', 'Color'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Baseball
    'id': 162603,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Ball size'),
      ('material', 'STRING', 'Material'),
    ]
  },
  {
    # Binders
    'id': 162749,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('metal_type', 'STRING', 'Metal type (Gold, Silver, Platinum)'),
      ('stone_type', 'STRING', 'Stone type (if applicable)'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Men's Henley Shirts
    'id': 162801,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('sleeve_length', 'STRING', 'Sleeve length'),
      ('fit', 'STRING', 'Fit type'),
      ('style', 'STRING', 'Style'),
    ]
  },
  {
    # Girls' Pants
    'id': 163472,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('age_range', 'STRING', 'Age range'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Men's Cargo Pants
    'id': 165456,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('waist_size', 'STRING', 'Waist size'),
      ('inseam', 'STRING', 'Inseam length'),
      ('fit', 'STRING', 'Fit type'),
      ('rise', 'STRING', 'Rise'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
    ]
  },
  {
    # Garden Hoses
    'id': 165560,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('length', 'STRING', 'Length (feet)'),
      ('diameter', 'STRING', 'Diameter'),
      ('material', 'STRING', 'Material'),
      ('kink_resistant', 'BOOLEAN', 'Kink resistant'),
    ]
  },
  {
    # Umbrella Stands
    'id': 165772,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Personal Health
    'id': 167008,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Wireless Headphones
    'id': 167124,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('storage', 'STRING', 'Storage capacity'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('color', 'STRING', 'Color'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Women's Workout Tops
    'id': 169672,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('sleeve_length', 'STRING', 'Sleeve length'),
      ('fit', 'STRING', 'Fit type'),
      ('style', 'STRING', 'Style'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Security Camera Systems
    'id': 169964,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Camera model'),
      ('megapixels', 'STRING', 'Megapixels'),
      ('sensor_size', 'STRING', 'Sensor size'),
      ('zoom', 'STRING', 'Optical zoom'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('weight', 'STRING', 'Weight'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Bathroom Storage
    'id': 170327,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('dimensions', 'STRING', 'Dimensions'),
      ('number_of_compartments', 'NUMBER', 'Number of compartments'),
    ]
  },
  {
    # Makeup
    'id': 170383,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('product_type', 'STRING', 'Product type'),
      ('shade', 'STRING', 'Shade/Color'),
      ('size', 'STRING', 'Size'),
      ('cruelty_free', 'BOOLEAN', 'Cruelty-free'),
      ('vegan', 'BOOLEAN', 'Vegan'),
    ]
  },
  {
    # Dining Tables
    'id': 171747,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material (Wood, Glass, Metal)'),
      ('color', 'STRING', 'Color/Finish'),
      ('seating_capacity', 'NUMBER', 'Seating capacity'),
      ('dimensions', 'STRING', 'Dimensions (L x W x H)'),
      ('shape', 'STRING', 'Shape (Round, Rectangular, Square)'),
      ('assembly_required', 'BOOLEAN', 'Assembly required'),
    ]
  },
  {
    # Men's Boxer Briefs
    'id': 171757,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Lunch Boxes
    'id': 172255,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # LED Strip Lights
    'id': 173541,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (Desk, Floor, Table)'),
      ('bulb_type', 'STRING', 'Bulb type'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('dimmable', 'BOOLEAN', 'Dimmable'),
    ]
  },
  {
    # Boys' Shoes
    'id': 173599,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('age_range', 'STRING', 'Age range'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Moisturizers
    'id': 173943,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Athletic Socks Women
    'id': 174861,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's Rain Jackets
    'id': 176171,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Baby Clothing
    'id': 176223,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('age_range', 'STRING', 'Age range'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('safety_certification', 'STRING', 'Safety certification'),
    ]
  },
  {
    # Floor Mats
    'id': 176428,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('fit', 'STRING', 'Vehicle fit'),
      ('weather_resistant', 'BOOLEAN', 'Weather resistant'),
    ]
  },
  {
    # Outdoor Chairs
    'id': 176787,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('dimensions', 'STRING', 'Dimensions'),
      ('weight_capacity', 'STRING', 'Weight capacity'),
      ('assembly_required', 'BOOLEAN', 'Assembly required'),
    ]
  },
  {
    # Phone Chargers
    'id': 177173,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('storage', 'STRING', 'Storage capacity'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('color', 'STRING', 'Color'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Car Organizers
    'id': 177504,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('dimensions', 'STRING', 'Dimensions'),
      ('number_of_compartments', 'NUMBER', 'Number of compartments'),
    ]
  },
  {
    # 4K TVs
    'id': 177800,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('resolution', 'STRING', 'Resolution (4K, 1080p, 8K)'),
      ('display_type', 'STRING', 'Display type (LED, OLED, QLED)'),
      ('refresh_rate', 'STRING', 'Refresh rate (Hz)'),
      ('smart_tv', 'BOOLEAN', 'Smart TV features'),
      ('hdr', 'BOOLEAN', 'HDR support'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Fans
    'id': 178973,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's Rompers
    'id': 181107,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Towels
    'id': 182666,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('material', 'STRING', 'Material (Cotton, Microfiber, etc.)'),
      ('color', 'STRING', 'Color'),
      ('weight', 'STRING', 'Weight (GSM)'),
      ('absorbency', 'STRING', 'Absorbency level'),
    ]
  },
  {
    # Baby Sleepwear
    'id': 184551,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('age_range', 'STRING', 'Age range'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('safety_certification', 'STRING', 'Safety certification'),
    ]
  },
  {
    # Girls' Shoes
    'id': 185444,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('age_range', 'STRING', 'Age range'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Pie Dishes
    'id': 187238,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's Denim Jackets
    'id': 189163,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Legal Pads
    'id': 190924,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('ruling', 'STRING', 'Ruling (Wide, College, Narrow)'),
      ('sheets_per_pad', 'NUMBER', 'Sheets per pad'),
      ('pack_count', 'NUMBER', 'Number of pads'),
    ]
  },
  {
    # Women's Shorts
    'id': 191076,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Mobile Devices
    'id': 191426,
    'attributes': [
      ('brand', 'STRING', 'Brand (Samsung, Google, OnePlus, etc.)'),
      ('model', 'STRING', 'Model name'),
      ('storage', 'STRING', 'Storage capacity'),
      ('ram', 'STRING', 'RAM size'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('resolution', 'STRING', 'Display resolution'),
      ('processor', 'STRING', 'Processor'),
      ('camera_megapixels', 'STRING', 'Camera megapixels'),
      ('battery_capacity', 'STRING', 'Battery capacity (mAh)'),
      ('operating_system', 'STRING', 'Android version'),
      ('color', 'STRING', 'Color'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Water
    'id': 193026,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('capacity', 'STRING', 'Capacity (oz)'),
      ('material', 'STRING', 'Material (Plastic, Stainless Steel, Glass)'),
      ('bpa_free', 'BOOLEAN', 'BPA-free'),
      ('insulated', 'BOOLEAN', 'Insulated'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Electric Bikes
    'id': 193199,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('type', 'STRING', 'Type (Mountain, Road, Hybrid, etc.)'),
      ('frame_size', 'STRING', 'Frame size'),
      ('wheel_size', 'STRING', 'Wheel size'),
      ('number_of_speeds', 'NUMBER', 'Number of speeds'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Racing Wheels
    'id': 195620,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('metal_type', 'STRING', 'Metal type (Gold, Silver, Platinum)'),
      ('stone_type', 'STRING', 'Stone type (if applicable)'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Pretend Play
    'id': 196805,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('age_range', 'STRING', 'Age range'),
      ('material', 'STRING', 'Material'),
      ('batteries_required', 'BOOLEAN', 'Batteries required'),
      ('number_of_players', 'STRING', 'Number of players'),
      ('theme', 'STRING', 'Theme'),
    ]
  },
  {
    # Trash Cans
    'id': 198192,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Beverages
    'id': 198479,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Cribs
    'id': 199241,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('age_range', 'STRING', 'Age range'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('safety_certification', 'STRING', 'Safety certification'),
    ]
  },
  {
    # Bikes
    'id': 199759,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('type', 'STRING', 'Type (Mountain, Road, Hybrid, etc.)'),
      ('frame_size', 'STRING', 'Frame size'),
      ('wheel_size', 'STRING', 'Wheel size'),
      ('number_of_speeds', 'NUMBER', 'Number of speeds'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Highlighters
    'id': 200081,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (Desk, Floor, Table)'),
      ('bulb_type', 'STRING', 'Bulb type'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('dimmable', 'BOOLEAN', 'Dimmable'),
    ]
  },
  {
    # HDMI Cables
    'id': 202809,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Cable type (USB-C, HDMI, etc.)'),
      ('length', 'STRING', 'Length'),
      ('compatibility', 'STRING', 'Compatibility'),
    ]
  },
  {
    # Smart Locks
    'id': 202876,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Hand Towels
    'id': 203136,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('material', 'STRING', 'Material (Cotton, Microfiber, etc.)'),
      ('color', 'STRING', 'Color'),
      ('weight', 'STRING', 'Weight (GSM)'),
      ('absorbency', 'STRING', 'Absorbency level'),
    ]
  },
  {
    # Computer Cases
    'id': 203905,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Hiking Boots
    'id': 204139,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size (US)'),
      ('width', 'STRING', 'Width'),
      ('material', 'STRING', 'Material'),
      ('waterproof', 'BOOLEAN', 'Waterproof'),
      ('ankle_height', 'STRING', 'Ankle height'),
    ]
  },
  {
    # Tools & Equipment
    'id': 204307,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Boys' Jeans
    'id': 205519,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('age_range', 'STRING', 'Age range'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Pacifiers
    'id': 205548,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('age_range', 'STRING', 'Age range'),
      ('material', 'STRING', 'Material'),
      ('orthodontic', 'BOOLEAN', 'Orthodontic'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Fitness Trackers
    'id': 207020,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('display_type', 'STRING', 'Display type'),
      ('battery_life', 'STRING', 'Battery life (days)'),
      ('water_resistant', 'BOOLEAN', 'Water resistant'),
      ('heart_rate_monitor', 'BOOLEAN', 'Heart rate monitor'),
      ('gps', 'BOOLEAN', 'GPS'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Women's Graphic Tees
    'id': 207470,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('sleeve_length', 'STRING', 'Sleeve length'),
      ('fit', 'STRING', 'Fit type'),
      ('style', 'STRING', 'Style'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Hiking
    'id': 209762,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # String Lights
    'id': 211573,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('metal_type', 'STRING', 'Metal type (Gold, Silver, Platinum)'),
      ('stone_type', 'STRING', 'Stone type (if applicable)'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Shampoo
    'id': 213070,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size (oz)'),
      ('hair_type', 'STRING', 'Hair type'),
      ('ingredients', 'STRING', 'Key ingredients'),
      ('sulfate_free', 'BOOLEAN', 'Sulfate-free'),
    ]
  },
  {
    # Flatware
    'id': 213394,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Bed Sheets
    'id': 214212,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size (Twin, Full, Queen, King)'),
      ('thread_count', 'STRING', 'Thread count'),
      ('material', 'STRING', 'Material (Cotton, Microfiber, etc.)'),
      ('color', 'STRING', 'Color'),
      ('pattern', 'STRING', 'Pattern'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Women's Leather Jackets
    'id': 215340,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Pencils
    'id': 216990,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (Ballpoint, Gel, Rollerball)'),
      ('ink_color', 'STRING', 'Ink color'),
      ('tip_size', 'STRING', 'Tip size'),
      ('refillable', 'BOOLEAN', 'Refillable'),
      ('pack_count', 'NUMBER', 'Number of pens'),
    ]
  },
  {
    # Car Chargers
    'id': 218482,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('storage', 'STRING', 'Storage capacity'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('color', 'STRING', 'Color'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Flight Sticks
    'id': 221339,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (Desk, Floor, Table)'),
      ('bulb_type', 'STRING', 'Bulb type'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('dimmable', 'BOOLEAN', 'Dimmable'),
    ]
  },
  {
    # Plastic Containers
    'id': 221411,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('dimensions', 'STRING', 'Dimensions'),
      ('number_of_compartments', 'NUMBER', 'Number of compartments'),
    ]
  },
  {
    # Cat Toys
    'id': 221966,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('age_range', 'STRING', 'Age range'),
      ('type', 'STRING', 'Type'),
    ]
  },
  {
    # Air Purifiers
    'id': 222110,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('room_size', 'STRING', 'Room size coverage'),
      ('filter_type', 'STRING', 'Filter type'),
      ('noise_level', 'STRING', 'Noise level (dB)'),
      ('energy_rating', 'STRING', 'Energy rating'),
    ]
  },
  {
    # Digital Pianos
    'id': 222240,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('type', 'STRING', 'Type (Acoustic, Digital)'),
      ('number_of_keys', 'NUMBER', 'Number of keys'),
      ('color', 'STRING', 'Color/Finish'),
      ('dimensions', 'STRING', 'Dimensions'),
    ]
  },
  {
    # Women's Maternity
    'id': 222694,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Capos
    'id': 222811,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('type', 'STRING', 'Type (Acoustic, Electric, Bass)'),
      ('color', 'STRING', 'Color/Finish'),
      ('number_of_strings', 'NUMBER', 'Number of strings'),
      ('body_material', 'STRING', 'Body material'),
      ('scale_length', 'STRING', 'Scale length'),
    ]
  },
  {
    # Movies & TV
    'id': 223655,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Duvet Covers
    'id': 224116,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's Bomber Jackets
    'id': 224804,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Scanners
    'id': 226645,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('type', 'STRING', 'Type (Flatbed, Sheet-fed)'),
      ('resolution', 'STRING', 'Resolution (DPI)'),
      ('connectivity', 'STRING', 'Connectivity'),
    ]
  },
  {
    # Rugs & Carpets
    'id': 230113,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('pattern', 'STRING', 'Pattern'),
      ('pile_height', 'STRING', 'Pile height'),
    ]
  },
  {
    # Women's Cardigans
    'id': 230170,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Dog Collars & Leashes
    'id': 230857,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('width', 'STRING', 'Width'),
    ]
  },
  {
    # Crackers
    'id': 230972,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Smart Doorbells
    'id': 231113,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Amplifiers
    'id': 232554,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Kitchen Scales
    'id': 232600,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Lipstick
    'id': 233619,
    'attributes': [
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Car Accessories
    'id': 235022,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Mops & Brooms
    'id': 235435,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('size', 'STRING', 'Size/Diameter'),
      ('capacity', 'STRING', 'Capacity'),
      ('non_stick', 'BOOLEAN', 'Non-stick coating'),
      ('dishwasher_safe', 'BOOLEAN', 'Dishwasher safe'),
      ('induction_compatible', 'BOOLEAN', 'Induction compatible'),
    ]
  },
  {
    # Face Masks
    'id': 236140,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Mattress Pads
    'id': 238289,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size (Twin, Full, Queen, King)'),
      ('type', 'STRING', 'Type (Memory Foam, Innerspring, Hybrid)'),
      ('firmness', 'STRING', 'Firmness level'),
      ('thickness', 'STRING', 'Thickness (inches)'),
      ('material', 'STRING', 'Material'),
    ]
  },
  {
    # Graphics Cards (GPUs)
    'id': 240912,
    'attributes': [
      ('brand', 'STRING', 'Brand (NVIDIA, AMD)'),
      ('model', 'STRING', 'Model name'),
      ('memory', 'STRING', 'VRAM (GB)'),
      ('memory_type', 'STRING', 'Memory type (GDDR6, GDDR6X)'),
      ('clock_speed', 'STRING', 'Clock speed'),
      ('interface', 'STRING', 'Interface (PCIe)'),
      ('power_consumption', 'STRING', 'Power consumption (watts)'),
    ]
  },
  {
    # Fish & Aquatic
    'id': 242177,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size (gallons)'),
      ('material', 'STRING', 'Material (Glass, Acrylic)'),
      ('dimensions', 'STRING', 'Dimensions'),
      ('shape', 'STRING', 'Shape'),
    ]
  },
  {
    # Kitchen Knives
    'id': 242537,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Automotive
    'id': 243131,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Pots & Pans
    'id': 244434,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('size', 'STRING', 'Size/Diameter'),
      ('capacity', 'STRING', 'Capacity'),
      ('non_stick', 'BOOLEAN', 'Non-stick coating'),
      ('dishwasher_safe', 'BOOLEAN', 'Dishwasher safe'),
      ('induction_compatible', 'BOOLEAN', 'Induction compatible'),
    ]
  },
  {
    # Oatmeal
    'id': 244991,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Chromebooks
    'id': 245176,
    'attributes': [
      ('title', 'STRING', 'Book title'),
      ('author', 'STRING', 'Author name'),
      ('publisher', 'STRING', 'Publisher'),
      ('isbn', 'STRING', 'ISBN'),
      ('publication_date', 'STRING', 'Publication date'),
      ('language', 'STRING', 'Language'),
      ('format', 'STRING', 'Format (Hardcover, Paperback, eBook)'),
      ('pages', 'NUMBER', 'Number of pages'),
      ('genre', 'STRING', 'Genre'),
    ]
  },
  {
    # Hair Care
    'id': 245691,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # USB Cables
    'id': 246734,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Cable type (USB-C, HDMI, etc.)'),
      ('length', 'STRING', 'Length'),
      ('compatibility', 'STRING', 'Compatibility'),
    ]
  },
  {
    # Colanders
    'id': 247237,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Foundation
    'id': 248178,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Foam Rollers
    'id': 249445,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('length', 'STRING', 'Length'),
      ('diameter', 'STRING', 'Diameter'),
      ('density', 'STRING', 'Density'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Weather Stations
    'id': 249833,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Computers & Laptops
    'id': 249933,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('processor', 'STRING', 'CPU processor'),
      ('ram', 'STRING', 'RAM size'),
      ('storage', 'STRING', 'Storage capacity'),
      ('storage_type', 'STRING', 'Storage type (SSD/HDD)'),
      ('operating_system', 'STRING', 'Operating system'),
      ('color', 'STRING', 'Color'),
      ('weight', 'STRING', 'Weight'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Car Electronics
    'id': 253815,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Phone Cases
    'id': 254204,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('storage', 'STRING', 'Storage capacity'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('color', 'STRING', 'Color'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Dog Beds
    'id': 254438,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color/Finish'),
      ('dimensions', 'STRING', 'Dimensions (L x W x H)'),
      ('assembly_required', 'BOOLEAN', 'Assembly required'),
      ('style', 'STRING', 'Style'),
    ]
  },
  {
    # Desk Lamps
    'id': 254800,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (Desk, Floor, Table)'),
      ('bulb_type', 'STRING', 'Bulb type'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('dimmable', 'BOOLEAN', 'Dimmable'),
    ]
  },
  {
    # Wall Art
    'id': 255234,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (Acrylic, Oil, Watercolor)'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
      ('finish', 'STRING', 'Finish (Matte, Gloss)'),
    ]
  },
  {
    # Turntables
    'id': 255774,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Kids' Shoes
    'id': 258805,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('age_range', 'STRING', 'Age range'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Nightstands
    'id': 259018,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's Jeggings
    'id': 259397,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Men's Sweatpants
    'id': 260019,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('waist_size', 'STRING', 'Waist size'),
      ('inseam', 'STRING', 'Inseam length'),
      ('fit', 'STRING', 'Fit type'),
      ('rise', 'STRING', 'Rise'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
    ]
  },
  {
    # Cleaning Supplies
    'id': 260190,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's Panties
    'id': 260370,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('waist_size', 'STRING', 'Waist size'),
      ('inseam', 'STRING', 'Inseam length'),
      ('fit', 'STRING', 'Fit type'),
      ('rise', 'STRING', 'Rise'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
    ]
  },
  {
    # Jewelry
    'id': 260937,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('metal_type', 'STRING', 'Metal type (Gold, Silver, Platinum)'),
      ('stone_type', 'STRING', 'Stone type (if applicable)'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Candles
    'id': 261388,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('scent', 'STRING', 'Scent/Fragrance'),
      ('size', 'STRING', 'Size'),
      ('burn_time', 'STRING', 'Burn time (hours)'),
      ('material', 'STRING', 'Material (Soy, Beeswax, Paraffin)'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Headphone Amps
    'id': 261505,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('storage', 'STRING', 'Storage capacity'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('color', 'STRING', 'Color'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Educational Books
    'id': 261558,
    'attributes': [
      ('title', 'STRING', 'Book title'),
      ('author', 'STRING', 'Author name'),
      ('publisher', 'STRING', 'Publisher'),
      ('isbn', 'STRING', 'ISBN'),
      ('publication_date', 'STRING', 'Publication date'),
      ('language', 'STRING', 'Language'),
      ('format', 'STRING', 'Format (Hardcover, Paperback, eBook)'),
      ('pages', 'NUMBER', 'Number of pages'),
      ('genre', 'STRING', 'Genre'),
    ]
  },
  {
    # Coolers
    'id': 261869,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('capacity', 'STRING', 'Capacity (quarts)'),
      ('type', 'STRING', 'Type (Hard, Soft)'),
      ('number_of_wheels', 'NUMBER', 'Number of wheels'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Health & Fitness
    'id': 262001,
    'attributes': [
      ('title', 'STRING', 'Book title'),
      ('author', 'STRING', 'Author name'),
      ('publisher', 'STRING', 'Publisher'),
      ('isbn', 'STRING', 'ISBN'),
      ('publication_date', 'STRING', 'Publication date'),
      ('language', 'STRING', 'Language'),
      ('format', 'STRING', 'Format (Hardcover, Paperback, eBook)'),
      ('pages', 'NUMBER', 'Number of pages'),
      ('genre', 'STRING', 'Genre'),
    ]
  },
  {
    # Wireless Chargers
    'id': 262282,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (USB, Wireless, Car)'),
      ('output', 'STRING', 'Output power/voltage'),
      ('compatibility', 'STRING', 'Device compatibility'),
      ('cable_length', 'STRING', 'Cable length'),
    ]
  },
  {
    # Wearable Technology
    'id': 263026,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Piping Bags
    'id': 263350,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (Straight, Quilting)'),
      ('length', 'STRING', 'Length'),
      ('count', 'NUMBER', 'Number of pins'),
    ]
  },
  {
    # Toothpaste
    'id': 263363,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Small Animal Toys
    'id': 263952,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('age_range', 'STRING', 'Age range'),
      ('material', 'STRING', 'Material'),
      ('batteries_required', 'BOOLEAN', 'Batteries required'),
      ('number_of_players', 'STRING', 'Number of players'),
      ('theme', 'STRING', 'Theme'),
    ]
  },
  {
    # Men's Sweaters
    'id': 264703,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Percussion Instruments
    'id': 267033,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Men's Socks
    'id': 267346,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Wallets
    'id': 268302,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material (Leather, Fabric, etc.)'),
      ('color', 'STRING', 'Color'),
      ('type', 'STRING', 'Type (Bifold, Trifold, Cardholder)'),
      ('rfid_blocking', 'BOOLEAN', 'RFID blocking'),
    ]
  },
  {
    # Tongs
    'id': 269129,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Anklets
    'id': 269405,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('metal_type', 'STRING', 'Metal type (Gold, Silver, Platinum)'),
      ('stone_type', 'STRING', 'Stone type (if applicable)'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Cocktail Glasses
    'id': 271504,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('capacity', 'STRING', 'Capacity (oz)'),
      ('type', 'STRING', 'Type (Martini, Margarita, etc.)'),
      ('quantity', 'NUMBER', 'Quantity in set'),
    ]
  },
  {
    # Nuts
    'id': 271790,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Eyeliner
    'id': 271838,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's Long Sleeve Tops
    'id': 273667,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('sleeve_length', 'STRING', 'Sleeve length'),
      ('fit', 'STRING', 'Fit type'),
      ('style', 'STRING', 'Style'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Men's Formal Wear
    'id': 274049,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Tire size'),
      ('type', 'STRING', 'Type (All-season, Winter, Summer)'),
      ('speed_rating', 'STRING', 'Speed rating'),
      ('load_index', 'STRING', 'Load index'),
    ]
  },
  {
    # Hard Drives
    'id': 274082,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('capacity', 'STRING', 'Storage capacity'),
      ('type', 'STRING', 'Type (HDD, SSD, NVMe)'),
      ('interface', 'STRING', 'Interface (USB 3.0, USB-C, Thunderbolt)'),
      ('form_factor', 'STRING', 'Form factor'),
      ('speed', 'STRING', 'Read/Write speed'),
    ]
  },
  {
    # Pressure Cookers
    'id': 274534,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Pain Relief
    'id': 274893,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Outdoor Decor
    'id': 275243,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Dictionaries
    'id': 275575,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Young Adult
    'id': 275773,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Petite Clothing
    'id': 276106,
    'attributes': [
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Dining Room Furniture
    'id': 276124,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color/Finish'),
      ('dimensions', 'STRING', 'Dimensions (L x W x H)'),
      ('assembly_required', 'BOOLEAN', 'Assembly required'),
      ('style', 'STRING', 'Style'),
    ]
  },
  {
    # Outdoor Recreation
    'id': 277608,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Fine Jewelry
    'id': 278134,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('metal_type', 'STRING', 'Metal type (Gold, Silver, Platinum)'),
      ('stone_type', 'STRING', 'Stone type (if applicable)'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Popcorn
    'id': 278348,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Corkscrews
    'id': 278697,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Dog Supplies
    'id': 278938,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's Midi Dresses
    'id': 280026,
    'attributes': [
      ('dimensions', 'STRING', 'Dimensions'),
    ]
  },
  {
    # Gaming
    'id': 280702,
    'attributes': [
      ('title', 'STRING', 'Game title'),
      ('platform', 'STRING', 'Platform (PlayStation, Xbox, Nintendo, PC)'),
      ('genre', 'STRING', 'Genre'),
      ('rating', 'STRING', 'ESRB rating'),
      ('release_date', 'STRING', 'Release date'),
      ('edition', 'STRING', 'Edition'),
    ]
  },
  {
    # Toasters
    'id': 280920,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Pantry Staples
    'id': 281610,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('size', 'STRING', 'Size/Diameter'),
      ('capacity', 'STRING', 'Capacity'),
      ('non_stick', 'BOOLEAN', 'Non-stick coating'),
      ('dishwasher_safe', 'BOOLEAN', 'Dishwasher safe'),
      ('induction_compatible', 'BOOLEAN', 'Induction compatible'),
    ]
  },
  {
    # Concealer
    'id': 282647,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('product_type', 'STRING', 'Product type'),
      ('shade', 'STRING', 'Shade/Color'),
      ('size', 'STRING', 'Size'),
      ('cruelty_free', 'BOOLEAN', 'Cruelty-free'),
      ('vegan', 'BOOLEAN', 'Vegan'),
    ]
  },
  {
    # Bracelets
    'id': 283623,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('metal_type', 'STRING', 'Metal type (Gold, Silver, Platinum)'),
      ('stone_type', 'STRING', 'Stone type (if applicable)'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Dressers
    'id': 283923,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Sleep Aids
    'id': 285147,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Modems
    'id': 285465,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('wifi_standard', 'STRING', 'Wi-Fi standard (Wi-Fi 6, Wi-Fi 5)'),
      ('speed', 'STRING', 'Speed (Mbps)'),
      ('number_of_antennas', 'NUMBER', 'Number of antennas'),
    ]
  },
  {
    # Book Lights
    'id': 286197,
    'attributes': [
      ('title', 'STRING', 'Book title'),
      ('author', 'STRING', 'Author name'),
      ('publisher', 'STRING', 'Publisher'),
      ('isbn', 'STRING', 'ISBN'),
      ('publication_date', 'STRING', 'Publication date'),
      ('language', 'STRING', 'Language'),
      ('format', 'STRING', 'Format (Hardcover, Paperback, eBook)'),
      ('pages', 'NUMBER', 'Number of pages'),
      ('genre', 'STRING', 'Genre'),
    ]
  },
  {
    # Women's Camisoles
    'id': 291554,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('sleeve_length', 'STRING', 'Sleeve length'),
      ('fit', 'STRING', 'Fit type'),
      ('style', 'STRING', 'Style'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Wireless Keyboards
    'id': 291974,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Audio Interfaces
    'id': 293475,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Powder
    'id': 293583,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Girls' Activewear
    'id': 294121,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('age_range', 'STRING', 'Age range'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Women's Skirts
    'id': 296566,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('length', 'STRING', 'Length'),
      ('type', 'STRING', 'Type'),
      ('ability_level', 'STRING', 'Ability level'),
      ('width', 'STRING', 'Width'),
    ]
  },
  {
    # DisplayPort Cables
    'id': 296994,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Cable type (USB-C, HDMI, etc.)'),
      ('length', 'STRING', 'Length'),
      ('compatibility', 'STRING', 'Compatibility'),
    ]
  },
  {
    # Cycling
    'id': 298024,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('type', 'STRING', 'Type (Mountain, Road, Hybrid, etc.)'),
      ('frame_size', 'STRING', 'Frame size'),
      ('wheel_size', 'STRING', 'Wheel size'),
      ('number_of_speeds', 'NUMBER', 'Number of speeds'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Textbooks
    'id': 302486,
    'attributes': [
      ('title', 'STRING', 'Textbook title'),
      ('author', 'STRING', 'Author name'),
      ('publisher', 'STRING', 'Publisher'),
      ('isbn', 'STRING', 'ISBN'),
      ('edition', 'STRING', 'Edition'),
      ('publication_date', 'STRING', 'Publication date'),
      ('subject', 'STRING', 'Subject area'),
      ('grade_level', 'STRING', 'Grade level'),
      ('format', 'STRING', 'Format (Hardcover, Paperback, eBook)'),
      ('pages', 'NUMBER', 'Number of pages'),
    ]
  },
  {
    # Curtains & Drapes
    'id': 303610,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('pattern', 'STRING', 'Pattern'),
      ('light_blocking', 'BOOLEAN', 'Light blocking'),
    ]
  },
  {
    # Smart Rings
    'id': 303679,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('metal_type', 'STRING', 'Metal type (Gold, Silver, Platinum)'),
      ('stone_type', 'STRING', 'Stone type (if applicable)'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Men's Dress Shoes
    'id': 311019,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Pitchers
    'id': 312197,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Soundbars
    'id': 312327,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Chess Sets
    'id': 313393,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Non-Fiction Books
    'id': 313855,
    'attributes': [
      ('title', 'STRING', 'Book title'),
      ('author', 'STRING', 'Author name'),
      ('publisher', 'STRING', 'Publisher'),
      ('isbn', 'STRING', 'ISBN'),
      ('publication_date', 'STRING', 'Publication date'),
      ('language', 'STRING', 'Language'),
      ('format', 'STRING', 'Format (Hardcover, Paperback, eBook)'),
      ('pages', 'NUMBER', 'Number of pages'),
      ('genre', 'STRING', 'Genre'),
    ]
  },
  {
    # Musical Instruments Toys
    'id': 315381,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('age_range', 'STRING', 'Age range'),
      ('material', 'STRING', 'Material'),
      ('batteries_required', 'BOOLEAN', 'Batteries required'),
      ('number_of_players', 'STRING', 'Number of players'),
      ('theme', 'STRING', 'Theme'),
    ]
  },
  {
    # Women's Yoga Pants
    'id': 315790,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('waist_size', 'STRING', 'Waist size'),
      ('inseam', 'STRING', 'Inseam length'),
      ('fit', 'STRING', 'Fit type'),
      ('rise', 'STRING', 'Rise'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
    ]
  },
  {
    # Women's Maxi Dresses
    'id': 316882,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Girls' Clothing
    'id': 318706,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('age_range', 'STRING', 'Age range'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Kitchen & Dining
    'id': 319328,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Men's T-Shirts
    'id': 319466,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('sleeve_length', 'STRING', 'Sleeve length'),
      ('fit', 'STRING', 'Fit type'),
      ('style', 'STRING', 'Style'),
    ]
  },
  {
    # Men's Shoes
    'id': 320293,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size (US)'),
      ('width', 'STRING', 'Width'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('style', 'STRING', 'Style'),
      ('closure', 'STRING', 'Closure type'),
    ]
  },
  {
    # Magazine Racks
    'id': 321104,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's Fragrances
    'id': 322943,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Headphones
    'id': 322958,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('storage', 'STRING', 'Storage capacity'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('color', 'STRING', 'Color'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Backpacks
    'id': 323336,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('capacity', 'STRING', 'Capacity (liters)'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('number_of_compartments', 'NUMBER', 'Number of compartments'),
      ('laptop_compartment', 'BOOLEAN', 'Laptop compartment'),
      ('water_resistant', 'BOOLEAN', 'Water resistant'),
    ]
  },
  {
    # Women's Sweaters
    'id': 323527,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Guitars
    'id': 324523,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('type', 'STRING', 'Type (Acoustic, Electric, Bass)'),
      ('color', 'STRING', 'Color/Finish'),
      ('number_of_strings', 'NUMBER', 'Number of strings'),
      ('body_material', 'STRING', 'Body material'),
      ('scale_length', 'STRING', 'Scale length'),
    ]
  },
  {
    # Chip & Dip Sets
    'id': 324965,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Meat Thermometers
    'id': 325000,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Speakers
    'id': 326512,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Billiards
    'id': 326976,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Car Care
    'id': 327104,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Treadmills
    'id': 331748,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('max_speed', 'STRING', 'Maximum speed (mph)'),
      ('incline', 'STRING', 'Incline range'),
      ('display', 'STRING', 'Display type'),
      ('weight_capacity', 'STRING', 'Weight capacity (lbs)'),
    ]
  },
  {
    # Paper Products
    'id': 332060,
    'attributes': [
      ('title', 'STRING', 'Book title'),
      ('author', 'STRING', 'Author name'),
      ('publisher', 'STRING', 'Publisher'),
      ('isbn', 'STRING', 'ISBN'),
      ('publication_date', 'STRING', 'Publication date'),
      ('language', 'STRING', 'Language'),
      ('format', 'STRING', 'Format (Hardcover, Paperback, eBook)'),
      ('pages', 'NUMBER', 'Number of pages'),
      ('genre', 'STRING', 'Genre'),
    ]
  },
  {
    # Men's Sleepwear
    'id': 332646,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Art Supplies
    'id': 334439,
    'attributes': [
      ('material', 'STRING', 'Material'),
    ]
  },
  {
    # SSDs
    'id': 335212,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('capacity', 'STRING', 'Storage capacity'),
      ('type', 'STRING', 'Type (HDD, SSD, NVMe)'),
      ('interface', 'STRING', 'Interface (USB 3.0, USB-C, Thunderbolt)'),
      ('form_factor', 'STRING', 'Form factor'),
      ('speed', 'STRING', 'Read/Write speed'),
    ]
  },
  {
    # Bagpipes
    'id': 336268,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Streaming Devices
    'id': 337569,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Stylus Pens
    'id': 339855,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Kitchen Utensils
    'id': 340050,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Men's Fleece
    'id': 341087,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Lighting
    'id': 343315,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (Desk, Floor, Table)'),
      ('bulb_type', 'STRING', 'Bulb type'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('dimmable', 'BOOLEAN', 'Dimmable'),
    ]
  },
  {
    # Women's Mini Dresses
    'id': 345766,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Picture Frames
    'id': 345951,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('orientation', 'STRING', 'Orientation (Portrait, Landscape)'),
    ]
  },
  {
    # Hats & Caps
    'id': 347134,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Men's Sneakers
    'id': 348446,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size (US)'),
      ('width', 'STRING', 'Width'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('style', 'STRING', 'Style'),
      ('closure', 'STRING', 'Closure type'),
    ]
  },
  {
    # Spatulas
    'id': 349318,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's Boots
    'id': 351212,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Drum Accessories
    'id': 352499,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Notebooks
    'id': 354004,
    'attributes': [
      ('title', 'STRING', 'Book title'),
      ('author', 'STRING', 'Author name'),
      ('publisher', 'STRING', 'Publisher'),
      ('isbn', 'STRING', 'ISBN'),
      ('publication_date', 'STRING', 'Publication date'),
      ('language', 'STRING', 'Language'),
      ('format', 'STRING', 'Format (Hardcover, Paperback, eBook)'),
      ('pages', 'NUMBER', 'Number of pages'),
      ('genre', 'STRING', 'Genre'),
    ]
  },
  {
    # Cleaning Solutions
    'id': 355785,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Butter Dishes
    'id': 355824,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Science Fiction
    'id': 356218,
    'attributes': [
      ('title', 'STRING', 'Book title'),
      ('author', 'STRING', 'Author name'),
      ('publisher', 'STRING', 'Publisher'),
      ('isbn', 'STRING', 'ISBN'),
      ('publication_date', 'STRING', 'Publication date'),
      ('language', 'STRING', 'Language'),
      ('format', 'STRING', 'Format (Hardcover, Paperback, eBook)'),
      ('pages', 'NUMBER', 'Number of pages'),
      ('genre', 'STRING', 'Genre'),
    ]
  },
  {
    # Wine Glasses
    'id': 357649,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material (Glass, Crystal)'),
      ('type', 'STRING', 'Type (Red, White, Champagne)'),
      ('capacity', 'STRING', 'Capacity (oz)'),
      ('quantity', 'NUMBER', 'Quantity in set'),
    ]
  },
  {
    # Recliners
    'id': 359949,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('dimensions', 'STRING', 'Dimensions'),
      ('weight_capacity', 'STRING', 'Weight capacity'),
      ('assembly_required', 'BOOLEAN', 'Assembly required'),
    ]
  },
  {
    # Smartwatches
    'id': 362995,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('screen_size', 'STRING', 'Screen size'),
      ('operating_system', 'STRING', 'Operating system'),
      ('battery_life', 'STRING', 'Battery life'),
      ('water_resistant', 'BOOLEAN', 'Water resistant'),
      ('cellular', 'BOOLEAN', 'Cellular connectivity'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Audio Cables
    'id': 363328,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Cable type (USB-C, HDMI, etc.)'),
      ('length', 'STRING', 'Length'),
      ('compatibility', 'STRING', 'Compatibility'),
    ]
  },
  {
    # Digital Cameras
    'id': 364771,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Camera model'),
      ('megapixels', 'STRING', 'Megapixels'),
      ('sensor_size', 'STRING', 'Sensor size'),
      ('zoom', 'STRING', 'Optical zoom'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('weight', 'STRING', 'Weight'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Boys' Pants
    'id': 365214,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('age_range', 'STRING', 'Age range'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Luggage
    'id': 365226,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Amplifiers
    'id': 366544,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('type', 'STRING', 'Type (Acoustic, Electric, Bass)'),
      ('color', 'STRING', 'Color/Finish'),
      ('number_of_strings', 'NUMBER', 'Number of strings'),
      ('body_material', 'STRING', 'Body material'),
      ('scale_length', 'STRING', 'Scale length'),
    ]
  },
  {
    # Mirrorless Cameras
    'id': 366754,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Camera model'),
      ('megapixels', 'STRING', 'Megapixels'),
      ('sensor_size', 'STRING', 'Sensor size'),
      ('lens_mount', 'STRING', 'Lens mount type'),
      ('iso_range', 'STRING', 'ISO range'),
      ('video_resolution', 'STRING', 'Video resolution'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('weight', 'STRING', 'Weight'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Microwaves
    'id': 368385,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Smart Speakers
    'id': 368471,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Men's Activewear
    'id': 369793,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Patio Sets
    'id': 373897,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Cameras & Photography
    'id': 374669,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Camera model'),
      ('megapixels', 'STRING', 'Megapixels'),
      ('sensor_size', 'STRING', 'Sensor size'),
      ('zoom', 'STRING', 'Optical zoom'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('weight', 'STRING', 'Weight'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Jump Starters
    'id': 375705,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Horror
    'id': 375982,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Shaving Cream
    'id': 376608,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Gaming Chairs
    'id': 377355,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('dimensions', 'STRING', 'Dimensions'),
      ('weight_capacity', 'STRING', 'Weight capacity'),
      ('assembly_required', 'BOOLEAN', 'Assembly required'),
    ]
  },
  {
    # Memory Cards
    'id': 377455,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('dimensions', 'STRING', 'Dimensions'),
      ('number_of_compartments', 'NUMBER', 'Number of compartments'),
    ]
  },
  {
    # Women's Wrap Dresses
    'id': 380444,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Cake Stands
    'id': 380779,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Pillows
    'id': 381747,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Ottomans
    'id': 381777,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Plants & Seeds
    'id': 382550,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('plant_type', 'STRING', 'Plant type'),
      ('quantity', 'NUMBER', 'Seed count'),
      ('organic', 'BOOLEAN', 'Organic'),
    ]
  },
  {
    # Baby Bath
    'id': 382788,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('age_range', 'STRING', 'Age range'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('safety_certification', 'STRING', 'Safety certification'),
    ]
  },
  {
    # Loaf Pans
    'id': 385967,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('size', 'STRING', 'Size/Diameter'),
      ('capacity', 'STRING', 'Capacity'),
      ('non_stick', 'BOOLEAN', 'Non-stick coating'),
      ('dishwasher_safe', 'BOOLEAN', 'Dishwasher safe'),
      ('induction_compatible', 'BOOLEAN', 'Induction compatible'),
    ]
  },
  {
    # China Cabinets
    'id': 386390,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Harmonicas
    'id': 386799,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Slow Cookers
    'id': 387588,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('size', 'STRING', 'Size/Diameter'),
      ('capacity', 'STRING', 'Capacity'),
      ('non_stick', 'BOOLEAN', 'Non-stick coating'),
      ('dishwasher_safe', 'BOOLEAN', 'Dishwasher safe'),
      ('induction_compatible', 'BOOLEAN', 'Induction compatible'),
    ]
  },
  {
    # Tuners
    'id': 387712,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Network Switches
    'id': 389101,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Football
    'id': 389255,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Cooling Racks
    'id': 390985,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Smart TVs
    'id': 392106,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Violins
    'id': 393408,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('type', 'STRING', 'Type'),
      ('key', 'STRING', 'Key'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color/Finish'),
    ]
  },
  {
    # Car Wash
    'id': 394222,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Men's Hoodies
    'id': 394316,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('sleeve_length', 'STRING', 'Sleeve length'),
      ('fit', 'STRING', 'Fit type'),
      ('style', 'STRING', 'Style'),
    ]
  },
  {
    # Granola
    'id': 394667,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Hair Tools
    'id': 395397,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Cat Supplies
    'id': 395620,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Men's Sandals
    'id': 396150,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Tablecloths
    'id': 397027,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's Pantyhose
    'id': 398922,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('waist_size', 'STRING', 'Waist size'),
      ('inseam', 'STRING', 'Inseam length'),
      ('fit', 'STRING', 'Fit type'),
      ('rise', 'STRING', 'Rise'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
    ]
  },
  {
    # Webcams
    'id': 400010,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Camera model'),
      ('megapixels', 'STRING', 'Megapixels'),
      ('sensor_size', 'STRING', 'Sensor size'),
      ('zoom', 'STRING', 'Optical zoom'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('weight', 'STRING', 'Weight'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Microphone Stands
    'id': 401435,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('storage', 'STRING', 'Storage capacity'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('color', 'STRING', 'Color'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Office Supplies
    'id': 402260,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Biographies
    'id': 403010,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Action Cameras
    'id': 404574,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Camera model'),
      ('megapixels', 'STRING', 'Megapixels'),
      ('sensor_size', 'STRING', 'Sensor size'),
      ('zoom', 'STRING', 'Optical zoom'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('weight', 'STRING', 'Weight'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Women's Hoodies
    'id': 405195,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('sleeve_length', 'STRING', 'Sleeve length'),
      ('fit', 'STRING', 'Fit type'),
      ('style', 'STRING', 'Style'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Gaming Headsets
    'id': 406235,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('storage', 'STRING', 'Storage capacity'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('color', 'STRING', 'Color'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Girls' Jeans
    'id': 407019,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('age_range', 'STRING', 'Age range'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Comforters
    'id': 408055,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's Sleepwear
    'id': 408602,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Handbags
    'id': 408625,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Men's Chinos
    'id': 410142,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('waist_size', 'STRING', 'Waist size'),
      ('inseam', 'STRING', 'Inseam length'),
      ('fit', 'STRING', 'Fit type'),
      ('rise', 'STRING', 'Rise'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
    ]
  },
  {
    # Weights
    'id': 411429,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('weight', 'STRING', 'Weight (lbs)'),
      ('material', 'STRING', 'Material'),
      ('type', 'STRING', 'Type (Fixed, Adjustable)'),
    ]
  },
  {
    # Jewelry Sets
    'id': 411688,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('metal_type', 'STRING', 'Metal type (Gold, Silver, Platinum)'),
      ('stone_type', 'STRING', 'Stone type (if applicable)'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Mattresses
    'id': 411851,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size (Twin, Full, Queen, King)'),
      ('type', 'STRING', 'Type (Memory Foam, Innerspring, Hybrid)'),
      ('firmness', 'STRING', 'Firmness level'),
      ('thickness', 'STRING', 'Thickness (inches)'),
      ('material', 'STRING', 'Material'),
    ]
  },
  {
    # Men's Graphic Tees
    'id': 411967,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('sleeve_length', 'STRING', 'Sleeve length'),
      ('fit', 'STRING', 'Fit type'),
      ('style', 'STRING', 'Style'),
    ]
  },
  {
    # Women's Kimonos
    'id': 412431,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Men's Clothing
    'id': 412555,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Paper Clips
    'id': 412631,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('material', 'STRING', 'Material'),
      ('quantity', 'NUMBER', 'Quantity per box'),
    ]
  },
  {
    # Synthesizers
    'id': 412713,
    'attributes': [
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Nursery
    'id': 413131,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color/Finish'),
      ('dimensions', 'STRING', 'Dimensions (L x W x H)'),
      ('assembly_required', 'BOOLEAN', 'Assembly required'),
      ('style', 'STRING', 'Style'),
    ]
  },
  {
    # Pizza Cutters
    'id': 413406,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Data Storage
    'id': 414534,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('dimensions', 'STRING', 'Dimensions'),
      ('number_of_compartments', 'NUMBER', 'Number of compartments'),
    ]
  },
  {
    # Lightning Cables
    'id': 414990,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Cable type (USB-C, HDMI, etc.)'),
      ('length', 'STRING', 'Length'),
      ('compatibility', 'STRING', 'Compatibility'),
    ]
  },
  {
    # Printer Paper
    'id': 415150,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('type', 'STRING', 'Type (Inkjet, Laser, All-in-One)'),
      ('print_speed', 'STRING', 'Print speed (ppm)'),
      ('connectivity', 'STRING', 'Connectivity (USB, Wi-Fi, Ethernet)'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # DSLR Cameras
    'id': 415709,
    'attributes': [
      ('brand', 'STRING', 'Brand (Canon, Nikon, Sony, etc.)'),
      ('model', 'STRING', 'Camera model'),
      ('megapixels', 'STRING', 'Megapixels'),
      ('sensor_size', 'STRING', 'Sensor size (Full Frame, APS-C, etc.)'),
      ('lens_mount', 'STRING', 'Lens mount type'),
      ('iso_range', 'STRING', 'ISO range'),
      ('video_resolution', 'STRING', 'Video resolution'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('weight', 'STRING', 'Weight'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Bird Supplies
    'id': 415941,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Dart Boards
    'id': 418043,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Study Guides
    'id': 418380,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Baby Outerwear
    'id': 419293,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('age_range', 'STRING', 'Age range'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('safety_certification', 'STRING', 'Safety certification'),
    ]
  },
  {
    # Vitamin C
    'id': 420043,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('product_type', 'STRING', 'Product type'),
      ('dosage', 'STRING', 'Dosage per serving'),
      ('quantity', 'NUMBER', 'Quantity (count)'),
      ('expiration_date', 'STRING', 'Expiration date'),
      ('ingredients', 'STRING', 'Key ingredients'),
    ]
  },
  {
    # Middle Grade
    'id': 420084,
    'attributes': [
      ('title', 'STRING', 'Book title'),
      ('author', 'STRING', 'Author name'),
      ('publisher', 'STRING', 'Publisher'),
      ('isbn', 'STRING', 'ISBN'),
      ('publication_date', 'STRING', 'Publication date'),
      ('language', 'STRING', 'Language'),
      ('format', 'STRING', 'Format (Hardcover, Paperback, eBook)'),
      ('pages', 'NUMBER', 'Number of pages'),
      ('genre', 'STRING', 'Genre'),
    ]
  },
  {
    # Picture Books
    'id': 421041,
    'attributes': [
      ('title', 'STRING', 'Book title'),
      ('author', 'STRING', 'Author name'),
      ('publisher', 'STRING', 'Publisher'),
      ('isbn', 'STRING', 'ISBN'),
      ('publication_date', 'STRING', 'Publication date'),
      ('language', 'STRING', 'Language'),
      ('format', 'STRING', 'Format (Hardcover, Paperback, eBook)'),
      ('pages', 'NUMBER', 'Number of pages'),
      ('genre', 'STRING', 'Genre'),
    ]
  },
  {
    # Ukuleles
    'id': 421137,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Backpacking Packs
    'id': 421141,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('capacity', 'STRING', 'Capacity (liters)'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('number_of_compartments', 'NUMBER', 'Number of compartments'),
      ('laptop_compartment', 'BOOLEAN', 'Laptop compartment'),
      ('water_resistant', 'BOOLEAN', 'Water resistant'),
    ]
  },
  {
    # Team Sports
    'id': 422836,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Home Improvement
    'id': 423176,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Dish Racks
    'id': 423324,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Xbox
    'id': 424195,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Netbooks
    'id': 426025,
    'attributes': [
      ('title', 'STRING', 'Book title'),
      ('author', 'STRING', 'Author name'),
      ('publisher', 'STRING', 'Publisher'),
      ('isbn', 'STRING', 'ISBN'),
      ('publication_date', 'STRING', 'Publication date'),
      ('language', 'STRING', 'Language'),
      ('format', 'STRING', 'Format (Hardcover, Paperback, eBook)'),
      ('pages', 'NUMBER', 'Number of pages'),
      ('genre', 'STRING', 'Genre'),
    ]
  },
  {
    # Receivers
    'id': 427634,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Vases
    'id': 428298,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Parenting
    'id': 429122,
    'attributes': [
      ('title', 'STRING', 'Book title'),
      ('author', 'STRING', 'Author name'),
      ('publisher', 'STRING', 'Publisher'),
      ('isbn', 'STRING', 'ISBN'),
      ('publication_date', 'STRING', 'Publication date'),
      ('language', 'STRING', 'Language'),
      ('format', 'STRING', 'Format (Hardcover, Paperback, eBook)'),
      ('pages', 'NUMBER', 'Number of pages'),
      ('genre', 'STRING', 'Genre'),
    ]
  },
  {
    # Lotion
    'id': 429995,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # No Show Socks
    'id': 434641,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Historical Fiction
    'id': 436897,
    'attributes': [
      ('title', 'STRING', 'Book title'),
      ('author', 'STRING', 'Author name'),
      ('publisher', 'STRING', 'Publisher'),
      ('isbn', 'STRING', 'ISBN'),
      ('publication_date', 'STRING', 'Publication date'),
      ('language', 'STRING', 'Language'),
      ('format', 'STRING', 'Format (Hardcover, Paperback, eBook)'),
      ('pages', 'NUMBER', 'Number of pages'),
      ('genre', 'STRING', 'Genre'),
    ]
  },
  {
    # Memory Card Readers
    'id': 437601,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('capacity', 'STRING', 'Storage capacity'),
      ('type', 'STRING', 'Type (SD, SDHC, SDXC, MicroSD)'),
      ('speed_class', 'STRING', 'Speed class'),
      ('read_speed', 'STRING', 'Read speed'),
      ('write_speed', 'STRING', 'Write speed'),
    ]
  },
  {
    # Phone Cables
    'id': 437708,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('storage', 'STRING', 'Storage capacity'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('color', 'STRING', 'Color'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Cable Organizers
    'id': 438239,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Cable type (USB-C, HDMI, etc.)'),
      ('length', 'STRING', 'Length'),
      ('compatibility', 'STRING', 'Compatibility'),
    ]
  },
  {
    # Projectors
    'id': 438471,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Laptop Chargers
    'id': 439203,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('processor', 'STRING', 'CPU processor'),
      ('ram', 'STRING', 'RAM size'),
      ('storage', 'STRING', 'Storage capacity'),
      ('storage_type', 'STRING', 'Storage type (SSD/HDD)'),
      ('operating_system', 'STRING', 'Operating system'),
      ('color', 'STRING', 'Color'),
      ('weight', 'STRING', 'Weight'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Camping
    'id': 439974,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (Straight, Quilting)'),
      ('length', 'STRING', 'Length'),
      ('count', 'NUMBER', 'Number of pins'),
    ]
  },
  {
    # Kids' Clothing
    'id': 440580,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('age_range', 'STRING', 'Age range'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Cat Litter
    'id': 440624,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('age_range', 'STRING', 'Age range'),
      ('type', 'STRING', 'Type'),
    ]
  },
  {
    # Desk Organizers
    'id': 440993,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('dimensions', 'STRING', 'Dimensions'),
      ('number_of_compartments', 'NUMBER', 'Number of compartments'),
    ]
  },
  {
    # Baby Activity Centers
    'id': 442147,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('age_range', 'STRING', 'Age range'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('safety_certification', 'STRING', 'Safety certification'),
    ]
  },
  {
    # Can Openers
    'id': 443327,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (Ballpoint, Gel, Rollerball)'),
      ('ink_color', 'STRING', 'Ink color'),
      ('tip_size', 'STRING', 'Tip size'),
      ('refillable', 'BOOLEAN', 'Refillable'),
      ('pack_count', 'NUMBER', 'Number of pens'),
    ]
  },
  {
    # Kitchen Timers
    'id': 443852,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Girls' Outerwear
    'id': 444101,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('age_range', 'STRING', 'Age range'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Crochet Hooks
    'id': 444387,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Hook size'),
      ('material', 'STRING', 'Material'),
    ]
  },
  {
    # Literary Fiction
    'id': 444411,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Mobile Games
    'id': 444736,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('age_range', 'STRING', 'Age range'),
      ('number_of_players', 'STRING', 'Number of players'),
      ('play_time', 'STRING', 'Play time (minutes)'),
      ('theme', 'STRING', 'Theme'),
    ]
  },
  {
    # Smart Sensors
    'id': 445412,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Dish Soap
    'id': 445872,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Men's Polo Shirts
    'id': 447483,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('sleeve_length', 'STRING', 'Sleeve length'),
      ('fit', 'STRING', 'Fit type'),
      ('style', 'STRING', 'Style'),
    ]
  },
  {
    # Women's Tops
    'id': 447584,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('sleeve_length', 'STRING', 'Sleeve length'),
      ('fit', 'STRING', 'Fit type'),
      ('style', 'STRING', 'Style'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Antenna
    'id': 449156,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Wheel Covers
    'id': 449445,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Mirrors
    'id': 449676,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # High Chairs
    'id': 451369,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Table Runners
    'id': 453225,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Filters
    'id': 454787,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('focal_length', 'STRING', 'Focal length'),
      ('aperture', 'STRING', 'Maximum aperture'),
      ('lens_mount', 'STRING', 'Lens mount'),
      ('image_stabilization', 'BOOLEAN', 'Image stabilization'),
    ]
  },
  {
    # Monitor Arms
    'id': 454944,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('resolution', 'STRING', 'Resolution'),
      ('refresh_rate', 'STRING', 'Refresh rate (Hz)'),
      ('panel_type', 'STRING', 'Panel type'),
    ]
  },
  {
    # Security Alarms
    'id': 455955,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Designer Fashion
    'id': 456378,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
    ]
  },
  {
    # Cables & Adapters
    'id': 456533,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Cable type (USB-C, HDMI, etc.)'),
      ('length', 'STRING', 'Length'),
      ('compatibility', 'STRING', 'Compatibility'),
    ]
  },
  {
    # Women's Blouses
    'id': 457875,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('sleeve_length', 'STRING', 'Sleeve length'),
      ('fit', 'STRING', 'Fit type'),
      ('style', 'STRING', 'Style'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Men's Dress Shirts
    'id': 457916,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('sleeve_length', 'STRING', 'Sleeve length'),
      ('fit', 'STRING', 'Fit type'),
      ('style', 'STRING', 'Style'),
    ]
  },
  {
    # Women's Shapewear
    'id': 458761,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Keyboards
    'id': 460939,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # MIDI Controllers
    'id': 461106,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's Sundresses
    'id': 461132,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Power Supplies
    'id': 461616,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Poker Sets
    'id': 463350,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Baby Care
    'id': 463778,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('age_range', 'STRING', 'Age range'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('safety_certification', 'STRING', 'Safety certification'),
    ]
  },
  {
    # Decorative Objects
    'id': 464512,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Routers
    'id': 465295,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('wifi_standard', 'STRING', 'Wi-Fi standard (Wi-Fi 6, Wi-Fi 5)'),
      ('speed', 'STRING', 'Speed (Mbps)'),
      ('number_of_antennas', 'NUMBER', 'Number of antennas'),
    ]
  },
  {
    # Watering Equipment
    'id': 466012,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('metal_type', 'STRING', 'Metal type (Gold, Silver, Platinum)'),
      ('stone_type', 'STRING', 'Stone type (if applicable)'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Baby Carriers
    'id': 468128,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('age_range', 'STRING', 'Age range'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('safety_certification', 'STRING', 'Safety certification'),
    ]
  },
  {
    # Wastebaskets
    'id': 469466,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Home Hubs
    'id': 469678,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Adapter Dongles
    'id': 470185,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Sports & Outdoors
    'id': 470819,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # PC Games
    'id': 471470,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('age_range', 'STRING', 'Age range'),
      ('number_of_players', 'STRING', 'Number of players'),
      ('play_time', 'STRING', 'Play time (minutes)'),
      ('theme', 'STRING', 'Theme'),
    ]
  },
  {
    # Dinnerware
    'id': 472286,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Docking Stations
    'id': 473737,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('processor', 'STRING', 'CPU processor'),
      ('ram', 'STRING', 'RAM size'),
      ('storage', 'STRING', 'Storage capacity'),
      ('storage_type', 'STRING', 'Storage type (SSD/HDD)'),
      ('operating_system', 'STRING', 'Operating system'),
      ('color', 'STRING', 'Color'),
      ('weight', 'STRING', 'Weight'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Home Decor
    'id': 473796,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # E-Readers
    'id': 475655,
    'attributes': [
      ('title', 'STRING', 'Book title'),
      ('author', 'STRING', 'Author name'),
      ('publisher', 'STRING', 'Publisher'),
      ('isbn', 'STRING', 'ISBN'),
      ('publication_date', 'STRING', 'Publication date'),
      ('language', 'STRING', 'Language'),
      ('format', 'STRING', 'Format (Hardcover, Paperback, eBook)'),
      ('pages', 'NUMBER', 'Number of pages'),
      ('genre', 'STRING', 'Genre'),
    ]
  },
  {
    # Closet Organizers
    'id': 477581,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('dimensions', 'STRING', 'Dimensions'),
      ('number_of_compartments', 'NUMBER', 'Number of compartments'),
    ]
  },
  {
    # Portable SSDs
    'id': 477969,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('capacity', 'STRING', 'Storage capacity'),
      ('type', 'STRING', 'Type (HDD, SSD, NVMe)'),
      ('interface', 'STRING', 'Interface (USB 3.0, USB-C, Thunderbolt)'),
      ('form_factor', 'STRING', 'Form factor'),
      ('speed', 'STRING', 'Read/Write speed'),
    ]
  },
  {
    # LED Bulbs
    'id': 478568,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (Desk, Floor, Table)'),
      ('bulb_type', 'STRING', 'Bulb type'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('dimmable', 'BOOLEAN', 'Dimmable'),
    ]
  },
  {
    # Dolls
    'id': 478735,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Men's Casual Shoes
    'id': 479051,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Razors
    'id': 481290,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Makeup Brushes
    'id': 481324,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('product_type', 'STRING', 'Product type'),
      ('shade', 'STRING', 'Shade/Color'),
      ('size', 'STRING', 'Size'),
      ('cruelty_free', 'BOOLEAN', 'Cruelty-free'),
      ('vegan', 'BOOLEAN', 'Vegan'),
    ]
  },
  {
    # Screen Protectors
    'id': 481431,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Small Animal Supplies
    'id': 481454,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's Flats
    'id': 481655,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Boys' Sleepwear
    'id': 482026,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('age_range', 'STRING', 'Age range'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Knitting Needles
    'id': 482060,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Needle size'),
      ('length', 'STRING', 'Length'),
      ('material', 'STRING', 'Material'),
      ('type', 'STRING', 'Type (Straight, Circular, Double-pointed)'),
    ]
  },
  {
    # Coat Racks
    'id': 484020,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Washcloths
    'id': 485489,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Bar Stools
    'id': 486734,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Artificial Plants
    'id': 487064,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Board Games
    'id': 487268,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('age_range', 'STRING', 'Age range'),
      ('number_of_players', 'STRING', 'Number of players'),
      ('play_time', 'STRING', 'Play time (minutes)'),
      ('theme', 'STRING', 'Theme'),
      ('difficulty', 'STRING', 'Difficulty level'),
    ]
  },
  {
    # Engagement Rings
    'id': 487310,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('metal_type', 'STRING', 'Metal type (Gold, Silver, Platinum)'),
      ('stone_type', 'STRING', 'Stone type (if applicable)'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Writing Instruments
    'id': 487356,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (Ballpoint, Gel, Rollerball)'),
      ('ink_color', 'STRING', 'Ink color'),
      ('tip_size', 'STRING', 'Tip size'),
      ('refillable', 'BOOLEAN', 'Refillable'),
      ('pack_count', 'NUMBER', 'Number of pens'),
    ]
  },
  {
    # Printers
    'id': 488980,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('type', 'STRING', 'Type (Inkjet, Laser, All-in-One)'),
      ('print_speed', 'STRING', 'Print speed (ppm)'),
      ('connectivity', 'STRING', 'Connectivity (USB, Wi-Fi, Ethernet)'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Body Jewelry
    'id': 491560,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('metal_type', 'STRING', 'Metal type (Gold, Silver, Platinum)'),
      ('stone_type', 'STRING', 'Stone type (if applicable)'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Universal Chargers
    'id': 492514,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (USB, Wireless, Car)'),
      ('output', 'STRING', 'Output power/voltage'),
      ('compatibility', 'STRING', 'Device compatibility'),
      ('cable_length', 'STRING', 'Cable length'),
    ]
  },
  {
    # Cat Grooming
    'id': 494654,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Men's Jeans
    'id': 495610,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('waist_size', 'STRING', 'Waist size'),
      ('inseam', 'STRING', 'Inseam length'),
      ('fit', 'STRING', 'Fit (Slim, Straight, Relaxed, etc.)'),
      ('rise', 'STRING', 'Rise'),
      ('color', 'STRING', 'Color/Wash'),
      ('material', 'STRING', 'Material'),
      ('stretch', 'BOOLEAN', 'Stretch denim'),
    ]
  },
  {
    # Smart Carbon Monoxide Detectors
    'id': 495869,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Laundry Baskets
    'id': 495916,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Pour Over Coffee
    'id': 496064,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('capacity', 'STRING', 'Capacity (cups)'),
      ('type', 'STRING', 'Type (Drip, Espresso, French Press, etc.)'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('programmable', 'BOOLEAN', 'Programmable'),
    ]
  },
  {
    # Cookware
    'id': 496900,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('size', 'STRING', 'Size/Diameter'),
      ('capacity', 'STRING', 'Capacity'),
      ('non_stick', 'BOOLEAN', 'Non-stick coating'),
      ('dishwasher_safe', 'BOOLEAN', 'Dishwasher safe'),
      ('induction_compatible', 'BOOLEAN', 'Induction compatible'),
    ]
  },
  {
    # Garage Storage
    'id': 498396,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('dimensions', 'STRING', 'Dimensions'),
      ('number_of_compartments', 'NUMBER', 'Number of compartments'),
    ]
  },
  {
    # Smart Home Security
    'id': 498791,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Fertilizers
    'id': 498937,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (Liquid, Granular)'),
      ('npk_ratio', 'STRING', 'NPK ratio'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Vacuum Cleaners
    'id': 498964,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('type', 'STRING', 'Type (Upright, Canister, Stick, Robot)'),
      ('power', 'STRING', 'Power (watts)'),
      ('bagless', 'BOOLEAN', 'Bagless'),
      ('cordless', 'BOOLEAN', 'Cordless'),
    ]
  },
  {
    # Hair Treatments
    'id': 499153,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Breakfast Bars
    'id': 499262,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Powerline Adapters
    'id': 499768,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # MP3 Players
    'id': 501561,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Necklaces
    'id': 501786,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('metal_type', 'STRING', 'Metal type (Gold, Silver, Platinum)'),
      ('stone_type', 'STRING', 'Stone type (if applicable)'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Compression Socks
    'id': 502046,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Window Sensors
    'id': 502376,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Smartphones
    'id': 502532,
    'attributes': [
      ('brand', 'STRING', 'Brand (Samsung, Google, OnePlus, etc.)'),
      ('model', 'STRING', 'Model name'),
      ('storage', 'STRING', 'Storage capacity'),
      ('ram', 'STRING', 'RAM size'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('resolution', 'STRING', 'Display resolution'),
      ('processor', 'STRING', 'Processor'),
      ('camera_megapixels', 'STRING', 'Camera megapixels'),
      ('battery_capacity', 'STRING', 'Battery capacity (mAh)'),
      ('operating_system', 'STRING', 'Android version'),
      ('color', 'STRING', 'Color'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Men's Vests
    'id': 506954,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's Vests
    'id': 508449,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Power Banks
    'id': 508569,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (USB, Wireless, Car)'),
      ('output', 'STRING', 'Output power/voltage'),
      ('compatibility', 'STRING', 'Device compatibility'),
      ('cable_length', 'STRING', 'Cable length'),
    ]
  },
  {
    # Gaming Accessories
    'id': 509681,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Wind Instruments
    'id': 510347,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Wedding Bands
    'id': 511194,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('metal_type', 'STRING', 'Metal type (Gold, Silver, Platinum)'),
      ('stone_type', 'STRING', 'Stone type (if applicable)'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Jewelry Boxes
    'id': 511908,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('metal_type', 'STRING', 'Metal type (Gold, Silver, Platinum)'),
      ('stone_type', 'STRING', 'Stone type (if applicable)'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Women's Sheath Dresses
    'id': 515020,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Religion & Spirituality
    'id': 516531,
    'attributes': [
      ('title', 'STRING', 'Book title'),
      ('author', 'STRING', 'Author name'),
      ('publisher', 'STRING', 'Publisher'),
      ('isbn', 'STRING', 'ISBN'),
      ('publication_date', 'STRING', 'Publication date'),
      ('language', 'STRING', 'Language'),
      ('format', 'STRING', 'Format (Hardcover, Paperback, eBook)'),
      ('pages', 'NUMBER', 'Number of pages'),
      ('genre', 'STRING', 'Genre'),
    ]
  },
  {
    # Thermometers
    'id': 517658,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Tall Clothing
    'id': 517845,
    'attributes': [
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # String Instruments
    'id': 518526,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('metal_type', 'STRING', 'Metal type (Gold, Silver, Platinum)'),
      ('stone_type', 'STRING', 'Stone type (if applicable)'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Sauces & Condiments
    'id': 522566,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # SD Cards
    'id': 524926,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('capacity', 'STRING', 'Storage capacity'),
      ('type', 'STRING', 'Type (SD, SDHC, SDXC, MicroSD)'),
      ('speed_class', 'STRING', 'Speed class'),
      ('read_speed', 'STRING', 'Read speed'),
      ('write_speed', 'STRING', 'Write speed'),
    ]
  },
  {
    # Baby Toys
    'id': 524970,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('age_range', 'STRING', 'Age range'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('safety_certification', 'STRING', 'Safety certification'),
    ]
  },
  {
    # Women's Parkas
    'id': 525034,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Pet Supplies
    'id': 525415,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Car Vacuum
    'id': 526247,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('type', 'STRING', 'Type (Upright, Canister, Stick, Robot)'),
      ('power', 'STRING', 'Power (watts)'),
      ('bagless', 'BOOLEAN', 'Bagless'),
      ('cordless', 'BOOLEAN', 'Cordless'),
    ]
  },
  {
    # Exercise & Fitness
    'id': 527236,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Instant Cameras
    'id': 527912,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Camera model'),
      ('megapixels', 'STRING', 'Megapixels'),
      ('sensor_size', 'STRING', 'Sensor size'),
      ('zoom', 'STRING', 'Optical zoom'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('weight', 'STRING', 'Weight'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Coffee Tables
    'id': 527985,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Arts & Crafts
    'id': 528473,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Cake Pans
    'id': 529600,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('size', 'STRING', 'Size/Diameter'),
      ('capacity', 'STRING', 'Capacity'),
      ('non_stick', 'BOOLEAN', 'Non-stick coating'),
      ('dishwasher_safe', 'BOOLEAN', 'Dishwasher safe'),
      ('induction_compatible', 'BOOLEAN', 'Induction compatible'),
    ]
  },
  {
    # Business & Finance
    'id': 529869,
    'attributes': [
      ('title', 'STRING', 'Book title'),
      ('author', 'STRING', 'Author name'),
      ('publisher', 'STRING', 'Publisher'),
      ('isbn', 'STRING', 'ISBN'),
      ('publication_date', 'STRING', 'Publication date'),
      ('language', 'STRING', 'Language'),
      ('format', 'STRING', 'Format (Hardcover, Paperback, eBook)'),
      ('pages', 'NUMBER', 'Number of pages'),
      ('genre', 'STRING', 'Genre'),
    ]
  },
  {
    # First Aid
    'id': 531291,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Mail Organizers
    'id': 531509,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('dimensions', 'STRING', 'Dimensions'),
      ('number_of_compartments', 'NUMBER', 'Number of compartments'),
    ]
  },
  {
    # Smart Security Cameras
    'id': 532863,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Camera model'),
      ('megapixels', 'STRING', 'Megapixels'),
      ('sensor_size', 'STRING', 'Sensor size'),
      ('zoom', 'STRING', 'Optical zoom'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('weight', 'STRING', 'Weight'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Oven Mitts
    'id': 535732,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('size', 'STRING', 'Size/Diameter'),
      ('capacity', 'STRING', 'Capacity'),
      ('non_stick', 'BOOLEAN', 'Non-stick coating'),
      ('dishwasher_safe', 'BOOLEAN', 'Dishwasher safe'),
      ('induction_compatible', 'BOOLEAN', 'Induction compatible'),
    ]
  },
  {
    # Mascara
    'id': 536486,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Garden & Outdoor
    'id': 536883,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Card Games
    'id': 537329,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('age_range', 'STRING', 'Age range'),
      ('number_of_players', 'STRING', 'Number of players'),
      ('play_time', 'STRING', 'Play time (minutes)'),
      ('theme', 'STRING', 'Theme'),
    ]
  },
  {
    # Bookshelves
    'id': 537822,
    'attributes': [
      ('title', 'STRING', 'Book title'),
      ('author', 'STRING', 'Author name'),
      ('publisher', 'STRING', 'Publisher'),
      ('isbn', 'STRING', 'ISBN'),
      ('publication_date', 'STRING', 'Publication date'),
      ('language', 'STRING', 'Language'),
      ('format', 'STRING', 'Format (Hardcover, Paperback, eBook)'),
      ('pages', 'NUMBER', 'Number of pages'),
      ('genre', 'STRING', 'Genre'),
    ]
  },
  {
    # Bird Feeders
    'id': 538284,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # DVDs
    'id': 539697,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Muffin Tins
    'id': 539935,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('size', 'STRING', 'Size/Diameter'),
      ('capacity', 'STRING', 'Capacity'),
      ('non_stick', 'BOOLEAN', 'Non-stick coating'),
      ('dishwasher_safe', 'BOOLEAN', 'Dishwasher safe'),
      ('induction_compatible', 'BOOLEAN', 'Induction compatible'),
    ]
  },
  {
    # Processors (CPUs)
    'id': 540059,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Conditioner
    'id': 540582,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size (oz)'),
      ('hair_type', 'STRING', 'Hair type'),
      ('ingredients', 'STRING', 'Key ingredients'),
      ('sulfate_free', 'BOOLEAN', 'Sulfate-free'),
    ]
  },
  {
    # Rings
    'id': 541351,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('metal_type', 'STRING', 'Metal type (Gold, Silver, Platinum)'),
      ('stone_type', 'STRING', 'Stone type (if applicable)'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Snowboarding
    'id': 541868,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('length', 'STRING', 'Length'),
      ('type', 'STRING', 'Type'),
      ('ability_level', 'STRING', 'Ability level'),
      ('width', 'STRING', 'Width'),
    ]
  },
  {
    # Men's Dress Socks
    'id': 545033,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Kitchen Storage
    'id': 545588,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('dimensions', 'STRING', 'Dimensions'),
      ('number_of_compartments', 'NUMBER', 'Number of compartments'),
    ]
  },
  {
    # TV Stands
    'id': 545714,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Bakeware
    'id': 545979,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('size', 'STRING', 'Size/Diameter'),
      ('capacity', 'STRING', 'Capacity'),
      ('non_stick', 'BOOLEAN', 'Non-stick coating'),
      ('dishwasher_safe', 'BOOLEAN', 'Dishwasher safe'),
      ('induction_compatible', 'BOOLEAN', 'Induction compatible'),
    ]
  },
  {
    # Aquariums
    'id': 546917,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size (gallons)'),
      ('material', 'STRING', 'Material (Glass, Acrylic)'),
      ('dimensions', 'STRING', 'Dimensions'),
      ('shape', 'STRING', 'Shape'),
    ]
  },
  {
    # Stuffed Animals
    'id': 547331,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('age_range', 'STRING', 'Age range'),
      ('material', 'STRING', 'Material'),
      ('batteries_required', 'BOOLEAN', 'Batteries required'),
      ('number_of_players', 'STRING', 'Number of players'),
      ('theme', 'STRING', 'Theme'),
    ]
  },
  {
    # Men's Underwear
    'id': 548868,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Desk Accessories
    'id': 549990,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Gaming Mice
    'id': 551490,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Food & Beverages
    'id': 552035,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Boys' Clothing
    'id': 553675,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('age_range', 'STRING', 'Age range'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Juice
    'id': 555219,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Skincare
    'id': 555790,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('length', 'STRING', 'Length'),
      ('type', 'STRING', 'Type'),
      ('ability_level', 'STRING', 'Ability level'),
      ('width', 'STRING', 'Width'),
    ]
  },
  {
    # Dog Grooming
    'id': 556397,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Sewing Machines
    'id': 557529,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('type', 'STRING', 'Type (Mechanical, Electronic, Computerized)'),
      ('stitches', 'NUMBER', 'Number of stitches'),
      ('buttonhole_styles', 'NUMBER', 'Number of buttonhole styles'),
    ]
  },
  {
    # Android Tablets
    'id': 558299,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('storage', 'STRING', 'Storage capacity'),
      ('ram', 'STRING', 'RAM size'),
      ('operating_system', 'STRING', 'Operating system'),
      ('color', 'STRING', 'Color'),
      ('cellular', 'BOOLEAN', 'Cellular connectivity'),
    ]
  },
  {
    # Swimming
    'id': 558770,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Laptop Stands
    'id': 558994,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('processor', 'STRING', 'CPU processor'),
      ('ram', 'STRING', 'RAM size'),
      ('storage', 'STRING', 'Storage capacity'),
      ('storage_type', 'STRING', 'Storage type (SSD/HDD)'),
      ('operating_system', 'STRING', 'Operating system'),
      ('color', 'STRING', 'Color'),
      ('weight', 'STRING', 'Weight'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Women's Sandals
    'id': 560837,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Cookbooks
    'id': 561624,
    'attributes': [
      ('title', 'STRING', 'Book title'),
      ('author', 'STRING', 'Author name'),
      ('publisher', 'STRING', 'Publisher'),
      ('isbn', 'STRING', 'ISBN'),
      ('publication_date', 'STRING', 'Publication date'),
      ('language', 'STRING', 'Language'),
      ('format', 'STRING', 'Format (Hardcover, Paperback, eBook)'),
      ('pages', 'NUMBER', 'Number of pages'),
      ('genre', 'STRING', 'Genre'),
    ]
  },
  {
    # Fragrances
    'id': 562032,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Building Sets
    'id': 562432,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Men's Joggers
    'id': 562633,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('waist_size', 'STRING', 'Waist size'),
      ('inseam', 'STRING', 'Inseam length'),
      ('fit', 'STRING', 'Fit type'),
      ('rise', 'STRING', 'Rise'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
    ]
  },
  {
    # Feature Phones
    'id': 562900,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('storage', 'STRING', 'Storage capacity'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('color', 'STRING', 'Color'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Sunglasses
    'id': 563173,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Men's Windbreakers
    'id': 569487,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Men's Board Shorts
    'id': 569895,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # All-in-One Computers
    'id': 573844,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Bird Toys
    'id': 576004,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('age_range', 'STRING', 'Age range'),
      ('material', 'STRING', 'Material'),
      ('batteries_required', 'BOOLEAN', 'Batteries required'),
      ('number_of_players', 'STRING', 'Number of players'),
      ('theme', 'STRING', 'Theme'),
    ]
  },
  {
    # Silver Jewelry
    'id': 576417,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('metal_type', 'STRING', 'Metal type (Gold, Silver, Platinum)'),
      ('stone_type', 'STRING', 'Stone type (if applicable)'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Women's Puffer Jackets
    'id': 577351,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Sleeping Bags
    'id': 578464,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (Straight, Quilting)'),
      ('length', 'STRING', 'Length'),
      ('count', 'NUMBER', 'Number of pins'),
    ]
  },
  {
    # Model Kits
    'id': 578603,
    'attributes': [
      ('model', 'STRING', 'Model'),
    ]
  },
  {
    # Motor Oil
    'id': 579044,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('viscosity', 'STRING', 'Viscosity (e.g., 5W-30)'),
      ('type', 'STRING', 'Type (Conventional, Synthetic, Blend)'),
      ('size', 'STRING', 'Size (quarts)'),
    ]
  },
  {
    # Boys' Activewear
    'id': 580020,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('age_range', 'STRING', 'Age range'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Cooling Systems
    'id': 582276,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Laptop Sleeves
    'id': 583529,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('processor', 'STRING', 'CPU processor'),
      ('ram', 'STRING', 'RAM size'),
      ('storage', 'STRING', 'Storage capacity'),
      ('storage_type', 'STRING', 'Storage type (SSD/HDD)'),
      ('operating_system', 'STRING', 'Operating system'),
      ('color', 'STRING', 'Color'),
      ('weight', 'STRING', 'Weight'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Romance
    'id': 583909,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Teething Toys
    'id': 584146,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('age_range', 'STRING', 'Age range'),
      ('material', 'STRING', 'Material'),
      ('batteries_required', 'BOOLEAN', 'Batteries required'),
      ('number_of_players', 'STRING', 'Number of players'),
      ('theme', 'STRING', 'Theme'),
    ]
  },
  {
    # Men's Rain Jackets
    'id': 585266,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # OLED TVs
    'id': 587137,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('resolution', 'STRING', 'Resolution (4K, 1080p, 8K)'),
      ('display_type', 'STRING', 'Display type (LED, OLED, QLED)'),
      ('refresh_rate', 'STRING', 'Refresh rate (Hz)'),
      ('smart_tv', 'BOOLEAN', 'Smart TV features'),
      ('hdr', 'BOOLEAN', 'HDR support'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Deodorant
    'id': 588807,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Men's Swimwear
    'id': 589595,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Men's Trousers
    'id': 589772,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Small Appliances
    'id': 591115,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Bookcases
    'id': 595369,
    'attributes': [
      ('title', 'STRING', 'Book title'),
      ('author', 'STRING', 'Author name'),
      ('publisher', 'STRING', 'Publisher'),
      ('isbn', 'STRING', 'ISBN'),
      ('publication_date', 'STRING', 'Publication date'),
      ('language', 'STRING', 'Language'),
      ('format', 'STRING', 'Format (Hardcover, Paperback, eBook)'),
      ('pages', 'NUMBER', 'Number of pages'),
      ('genre', 'STRING', 'Genre'),
    ]
  },
  {
    # Musical Instruments
    'id': 595445,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Ellipticals
    'id': 596141,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('stride_length', 'STRING', 'Stride length'),
      ('resistance_levels', 'NUMBER', 'Resistance levels'),
      ('display', 'STRING', 'Display type'),
      ('weight_capacity', 'STRING', 'Weight capacity (lbs)'),
    ]
  },
  {
    # Women's Boyfriend Jeans
    'id': 596470,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Ice Skating
    'id': 597626,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('type', 'STRING', 'Type (Figure, Hockey, Recreational)'),
      ('blade_material', 'STRING', 'Blade material'),
    ]
  },
  {
    # Women's Pant Suits
    'id': 598929,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('waist_size', 'STRING', 'Waist size'),
      ('inseam', 'STRING', 'Inseam length'),
      ('fit', 'STRING', 'Fit type'),
      ('rise', 'STRING', 'Rise'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
    ]
  },
  {
    # Office Furniture
    'id': 599021,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color/Finish'),
      ('dimensions', 'STRING', 'Dimensions (L x W x H)'),
      ('assembly_required', 'BOOLEAN', 'Assembly required'),
      ('style', 'STRING', 'Style'),
    ]
  },
  {
    # Watches
    'id': 599223,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('type', 'STRING', 'Type (Analog, Digital, Hybrid)'),
      ('material', 'STRING', 'Material'),
      ('band_material', 'STRING', 'Band material'),
      ('water_resistant', 'BOOLEAN', 'Water resistant'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Acne Treatment
    'id': 600570,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Mixing Spoons
    'id': 600588,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Early Readers
    'id': 600955,
    'attributes': [
      ('title', 'STRING', 'Book title'),
      ('author', 'STRING', 'Author name'),
      ('publisher', 'STRING', 'Publisher'),
      ('isbn', 'STRING', 'ISBN'),
      ('publication_date', 'STRING', 'Publication date'),
      ('language', 'STRING', 'Language'),
      ('format', 'STRING', 'Format (Hardcover, Paperback, eBook)'),
      ('pages', 'NUMBER', 'Number of pages'),
      ('genre', 'STRING', 'Genre'),
    ]
  },
  {
    # Remote Control Toys
    'id': 601014,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('age_range', 'STRING', 'Age range'),
      ('material', 'STRING', 'Material'),
      ('batteries_required', 'BOOLEAN', 'Batteries required'),
      ('number_of_players', 'STRING', 'Number of players'),
      ('theme', 'STRING', 'Theme'),
    ]
  },
  {
    # Fishing
    'id': 602237,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Accent Chairs
    'id': 602276,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('dimensions', 'STRING', 'Dimensions'),
      ('weight_capacity', 'STRING', 'Weight capacity'),
      ('assembly_required', 'BOOLEAN', 'Assembly required'),
    ]
  },
  {
    # Salad Spinners
    'id': 602793,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (Straight, Quilting)'),
      ('length', 'STRING', 'Length'),
      ('count', 'NUMBER', 'Number of pins'),
    ]
  },
  {
    # Gaming Keyboards
    'id': 603326,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Thermoses
    'id': 603601,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('capacity', 'STRING', 'Capacity (oz)'),
      ('material', 'STRING', 'Material'),
      ('insulation', 'STRING', 'Insulation type'),
      ('leak_proof', 'BOOLEAN', 'Leak-proof'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Video Doorbell Systems
    'id': 603990,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Tea
    'id': 604353,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Gemstone Jewelry
    'id': 608657,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('metal_type', 'STRING', 'Metal type (Gold, Silver, Platinum)'),
      ('stone_type', 'STRING', 'Stone type (if applicable)'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Surge Protectors
    'id': 608941,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Motion Sensors
    'id': 610332,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Men's Suits
    'id': 611494,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Folders
    'id': 611644,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('type', 'STRING', 'Type (Manila, Hanging, Pocket)'),
      ('color', 'STRING', 'Color'),
      ('quantity', 'NUMBER', 'Quantity per pack'),
    ]
  },
  {
    # Motherboards
    'id': 612126,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Hand Tools
    'id': 613211,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Skiing
    'id': 614329,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('length', 'STRING', 'Length'),
      ('type', 'STRING', 'Type'),
      ('ability_level', 'STRING', 'Ability level'),
      ('width', 'STRING', 'Width'),
    ]
  },
  {
    # Guitar Pedals
    'id': 615542,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('type', 'STRING', 'Type (Acoustic, Electric, Bass)'),
      ('color', 'STRING', 'Color/Finish'),
      ('number_of_strings', 'NUMBER', 'Number of strings'),
      ('body_material', 'STRING', 'Body material'),
      ('scale_length', 'STRING', 'Scale length'),
    ]
  },
  {
    # Pendant Lights
    'id': 617603,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (Desk, Floor, Table)'),
      ('bulb_type', 'STRING', 'Bulb type'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('dimmable', 'BOOLEAN', 'Dimmable'),
    ]
  },
  {
    # Women's Jumpsuits
    'id': 618589,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # MicroSD Cards
    'id': 618747,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('capacity', 'STRING', 'Storage capacity'),
      ('type', 'STRING', 'Type (SD, SDHC, SDXC, MicroSD)'),
      ('speed_class', 'STRING', 'Speed class'),
      ('read_speed', 'STRING', 'Read speed'),
      ('write_speed', 'STRING', 'Write speed'),
    ]
  },
  {
    # Comic Books
    'id': 619141,
    'attributes': [
      ('title', 'STRING', 'Book title'),
      ('author', 'STRING', 'Author name'),
      ('publisher', 'STRING', 'Publisher'),
      ('isbn', 'STRING', 'ISBN'),
      ('publication_date', 'STRING', 'Publication date'),
      ('language', 'STRING', 'Language'),
      ('format', 'STRING', 'Format (Hardcover, Paperback, eBook)'),
      ('pages', 'NUMBER', 'Number of pages'),
      ('genre', 'STRING', 'Genre'),
    ]
  },
  {
    # Women's Leggings
    'id': 619978,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's Jeans
    'id': 620581,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('waist_size', 'STRING', 'Waist size'),
      ('inseam', 'STRING', 'Inseam length'),
      ('fit', 'STRING', 'Fit (Skinny, Straight, Bootcut, etc.)'),
      ('rise', 'STRING', 'Rise (Low, Mid, High)'),
      ('color', 'STRING', 'Color/Wash'),
      ('material', 'STRING', 'Material (Denim composition)'),
      ('stretch', 'BOOLEAN', 'Stretch denim'),
    ]
  },
  {
    # TV Series
    'id': 621221,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Hair Color
    'id': 621763,
    'attributes': [
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Lunch Containers
    'id': 621974,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Desks
    'id': 622061,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Food Processors
    'id': 623430,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Wardrobes
    'id': 627678,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Boys' Outerwear
    'id': 630457,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('age_range', 'STRING', 'Age range'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Camera Bags
    'id': 631706,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('capacity', 'STRING', 'Capacity'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('water_resistant', 'BOOLEAN', 'Water resistant'),
    ]
  },
  {
    # Tents
    'id': 632613,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (Straight, Quilting)'),
      ('length', 'STRING', 'Length'),
      ('count', 'NUMBER', 'Number of pins'),
    ]
  },
  {
    # Men's Outerwear
    'id': 634354,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Napkin Rings
    'id': 635707,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('metal_type', 'STRING', 'Metal type (Gold, Silver, Platinum)'),
      ('stone_type', 'STRING', 'Stone type (if applicable)'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Household
    'id': 636188,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Hardware
    'id': 638775,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Sun Shades
    'id': 639024,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Scissors
    'id': 639832,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('type', 'STRING', 'Type (Office, Craft, Kitchen)'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Men's Robes
    'id': 640417,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Car Wax
    'id': 640568,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Vanities
    'id': 641509,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Tablet Cases
    'id': 642142,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('storage', 'STRING', 'Storage capacity'),
      ('ram', 'STRING', 'RAM size'),
      ('operating_system', 'STRING', 'Operating system'),
      ('color', 'STRING', 'Color'),
      ('cellular', 'BOOLEAN', 'Cellular connectivity'),
    ]
  },
  {
    # Eyeshadow
    'id': 642158,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type'),
      ('number_of_wells', 'NUMBER', 'Number of wells'),
      ('material', 'STRING', 'Material'),
    ]
  },
  {
    # Gaming Consoles
    'id': 643023,
    'attributes': [
      ('title', 'STRING', 'Game title'),
      ('platform', 'STRING', 'Platform (PlayStation, Xbox, Nintendo, PC)'),
      ('genre', 'STRING', 'Genre'),
      ('rating', 'STRING', 'ESRB rating'),
      ('release_date', 'STRING', 'Release date'),
      ('edition', 'STRING', 'Edition'),
    ]
  },
  {
    # Women's Trench Coats
    'id': 643209,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Chips
    'id': 643403,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('size', 'STRING', 'Size/Diameter'),
      ('capacity', 'STRING', 'Capacity'),
      ('non_stick', 'BOOLEAN', 'Non-stick coating'),
      ('dishwasher_safe', 'BOOLEAN', 'Dishwasher safe'),
      ('induction_compatible', 'BOOLEAN', 'Induction compatible'),
    ]
  },
  {
    # Facial Cleansers
    'id': 643500,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Smart Displays
    'id': 644937,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Spices & Seasonings
    'id': 646133,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Bird Food
    'id': 646890,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type'),
      ('size', 'STRING', 'Size'),
      ('bird_type', 'STRING', 'Bird type'),
    ]
  },
  {
    # Point & Shoot Cameras
    'id': 647398,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Camera model'),
      ('megapixels', 'STRING', 'Megapixels'),
      ('sensor_size', 'STRING', 'Sensor size'),
      ('zoom', 'STRING', 'Optical zoom'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('weight', 'STRING', 'Weight'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Table Lamps
    'id': 647531,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (Desk, Floor, Table)'),
      ('bulb_type', 'STRING', 'Bulb type'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('dimmable', 'BOOLEAN', 'Dimmable'),
    ]
  },
  {
    # French Presses
    'id': 648405,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('capacity', 'STRING', 'Capacity (cups)'),
      ('type', 'STRING', 'Type (Drip, Espresso, French Press, etc.)'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('programmable', 'BOOLEAN', 'Programmable'),
    ]
  },
  {
    # Science & Nature
    'id': 648465,
    'attributes': [
      ('title', 'STRING', 'Book title'),
      ('author', 'STRING', 'Author name'),
      ('publisher', 'STRING', 'Publisher'),
      ('isbn', 'STRING', 'ISBN'),
      ('publication_date', 'STRING', 'Publication date'),
      ('language', 'STRING', 'Language'),
      ('format', 'STRING', 'Format (Hardcover, Paperback, eBook)'),
      ('pages', 'NUMBER', 'Number of pages'),
      ('genre', 'STRING', 'Genre'),
    ]
  },
  {
    # Vitamin D
    'id': 649874,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('product_type', 'STRING', 'Product type'),
      ('dosage', 'STRING', 'Dosage per serving'),
      ('quantity', 'NUMBER', 'Quantity (count)'),
      ('expiration_date', 'STRING', 'Expiration date'),
      ('ingredients', 'STRING', 'Key ingredients'),
    ]
  },
  {
    # Keyboard Instruments
    'id': 650377,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('type', 'STRING', 'Type (Acoustic, Digital)'),
      ('number_of_keys', 'NUMBER', 'Number of keys'),
      ('color', 'STRING', 'Color/Finish'),
      ('dimensions', 'STRING', 'Dimensions'),
    ]
  },
  {
    # Sofas & Couches
    'id': 652958,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material (Fabric, Leather, etc.)'),
      ('color', 'STRING', 'Color'),
      ('seating_capacity', 'NUMBER', 'Seating capacity'),
      ('dimensions', 'STRING', 'Dimensions (L x W x H)'),
      ('assembly_required', 'BOOLEAN', 'Assembly required'),
      ('style', 'STRING', 'Style'),
    ]
  },
  {
    # Range Extenders
    'id': 654897,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's Athletic Leggings
    'id': 654941,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Gravy Boats
    'id': 657218,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's High-Waisted Jeans
    'id': 658659,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Beauty & Personal Care
    'id': 659260,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Yoga Mats
    'id': 659460,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('thickness', 'STRING', 'Thickness (mm)'),
      ('material', 'STRING', 'Material'),
      ('length', 'STRING', 'Length'),
      ('width', 'STRING', 'Width'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Smart Home
    'id': 659557,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Music
    'id': 663485,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Mugs & Cups
    'id': 663502,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material (Ceramic, Glass, Stainless Steel)'),
      ('capacity', 'STRING', 'Capacity (oz)'),
      ('dishwasher_safe', 'BOOLEAN', 'Dishwasher safe'),
      ('microwave_safe', 'BOOLEAN', 'Microwave safe'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Rice
    'id': 666512,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Surfing
    'id': 666835,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('length', 'STRING', 'Length'),
      ('width', 'STRING', 'Width'),
      ('thickness', 'STRING', 'Thickness'),
      ('volume', 'STRING', 'Volume (liters)'),
      ('fin_setup', 'STRING', 'Fin setup'),
    ]
  },
  {
    # Cereal
    'id': 666976,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Smart Glasses
    'id': 667220,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Shot Glasses
    'id': 667873,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('capacity', 'STRING', 'Capacity (oz)'),
      ('quantity', 'NUMBER', 'Quantity in set'),
    ]
  },
  {
    # Shoe Racks
    'id': 668476,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('dimensions', 'STRING', 'Dimensions'),
      ('number_of_compartments', 'NUMBER', 'Number of compartments'),
    ]
  },
  {
    # Lawn Mowers
    'id': 669659,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('type', 'STRING', 'Type (Push, Self-propelled, Riding)'),
      ('cutting_width', 'STRING', 'Cutting width'),
      ('power_source', 'STRING', 'Power source (Gas, Electric, Battery)'),
    ]
  },
  {
    # Mice
    'id': 670451,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Car Chargers USB
    'id': 672994,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (USB, Wireless, Car)'),
      ('output', 'STRING', 'Output power/voltage'),
      ('compatibility', 'STRING', 'Device compatibility'),
      ('cable_length', 'STRING', 'Cable length'),
    ]
  },
  {
    # Women's Outerwear
    'id': 673283,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's One-Piece Swimsuits
    'id': 673532,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Whisks
    'id': 674907,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Plumbing
    'id': 675293,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Pianos
    'id': 675611,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('type', 'STRING', 'Type (Acoustic, Digital)'),
      ('number_of_keys', 'NUMBER', 'Number of keys'),
      ('color', 'STRING', 'Color/Finish'),
      ('dimensions', 'STRING', 'Dimensions'),
    ]
  },
  {
    # Belts
    'id': 677837,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Bed Skirts
    'id': 677939,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('length', 'STRING', 'Length'),
      ('type', 'STRING', 'Type'),
      ('ability_level', 'STRING', 'Ability level'),
      ('width', 'STRING', 'Width'),
    ]
  },
  {
    # Knee High Socks
    'id': 678538,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Men's Blazers
    'id': 679600,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Strollers
    'id': 679861,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('age_range', 'STRING', 'Age range'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('safety_certification', 'STRING', 'Safety certification'),
    ]
  },
  {
    # Kitchen Gadgets
    'id': 680871,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's Stockings
    'id': 681185,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Boys' T-Shirts
    'id': 682434,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('age_range', 'STRING', 'Age range'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Women's Pea Coats
    'id': 682679,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's Bermuda Shorts
    'id': 682767,
    'attributes': [
      ('dimensions', 'STRING', 'Dimensions'),
    ]
  },
  {
    # Loungers
    'id': 684285,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Computer Components
    'id': 685397,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Sound Cards
    'id': 685439,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # CD Players
    'id': 685593,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Road Bikes
    'id': 687037,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('type', 'STRING', 'Type (Mountain, Road, Hybrid, etc.)'),
      ('frame_size', 'STRING', 'Frame size'),
      ('wheel_size', 'STRING', 'Wheel size'),
      ('number_of_speeds', 'NUMBER', 'Number of speeds'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # 4K Monitors
    'id': 687140,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('resolution', 'STRING', 'Resolution'),
      ('refresh_rate', 'STRING', 'Refresh rate (Hz)'),
      ('panel_type', 'STRING', 'Panel type'),
    ]
  },
  {
    # Dining Chairs
    'id': 690180,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('dimensions', 'STRING', 'Dimensions'),
      ('weight_capacity', 'STRING', 'Weight capacity'),
      ('assembly_required', 'BOOLEAN', 'Assembly required'),
    ]
  },
  {
    # Guitar Picks
    'id': 690328,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Winter Sports
    'id': 690420,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Rolling Pins
    'id': 692392,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (Straight, Quilting)'),
      ('length', 'STRING', 'Length'),
      ('count', 'NUMBER', 'Number of pins'),
    ]
  },
  {
    # Water Sports
    'id': 692475,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Throw Pillows
    'id': 693845,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Extension Cords
    'id': 700152,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Reference Books
    'id': 701553,
    'attributes': [
      ('title', 'STRING', 'Book title'),
      ('author', 'STRING', 'Author name'),
      ('publisher', 'STRING', 'Publisher'),
      ('isbn', 'STRING', 'ISBN'),
      ('publication_date', 'STRING', 'Publication date'),
      ('language', 'STRING', 'Language'),
      ('format', 'STRING', 'Format (Hardcover, Paperback, eBook)'),
      ('pages', 'NUMBER', 'Number of pages'),
      ('genre', 'STRING', 'Genre'),
    ]
  },
  {
    # Men's Boots
    'id': 704135,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Car Jacks
    'id': 704319,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Men's Jackets
    'id': 704327,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # iPhones
    'id': 704898,
    'attributes': [
      ('model', 'STRING', 'iPhone model (e.g., iPhone 15 Pro)'),
      ('storage', 'STRING', 'Storage capacity (128GB, 256GB, 512GB, 1TB)'),
      ('color', 'STRING', 'Color'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('year', 'NUMBER', 'Release year'),
      ('network', 'STRING', 'Network compatibility (5G, 4G LTE)'),
      ('condition', 'STRING', 'Condition (New, Refurbished, Used)'),
    ]
  },
  {
    # Plus Size Clothing
    'id': 704998,
    'attributes': [
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Men's Athletic Socks
    'id': 705019,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Wireless Earbuds
    'id': 706887,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # NAS Drives
    'id': 707000,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('dimensions', 'STRING', 'Dimensions'),
      ('number_of_compartments', 'NUMBER', 'Number of compartments'),
    ]
  },
  {
    # Car Phone Mounts
    'id': 707629,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('storage', 'STRING', 'Storage capacity'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('color', 'STRING', 'Color'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Tablets
    'id': 709477,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('storage', 'STRING', 'Storage capacity'),
      ('ram', 'STRING', 'RAM size'),
      ('operating_system', 'STRING', 'Operating system'),
      ('color', 'STRING', 'Color'),
      ('cellular', 'BOOLEAN', 'Cellular connectivity'),
    ]
  },
  {
    # Chandeliers
    'id': 709796,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (Desk, Floor, Table)'),
      ('bulb_type', 'STRING', 'Bulb type'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('dimmable', 'BOOLEAN', 'Dimmable'),
    ]
  },
  {
    # Men's Coats
    'id': 709854,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Aquarium Decor
    'id': 712273,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size (gallons)'),
      ('material', 'STRING', 'Material (Glass, Acrylic)'),
      ('dimensions', 'STRING', 'Dimensions'),
      ('shape', 'STRING', 'Shape'),
    ]
  },
  {
    # Bass Drums
    'id': 713188,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's Caftans
    'id': 713807,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's Trousers
    'id': 714257,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's Dresses
    'id': 714774,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('length', 'STRING', 'Dress length'),
      ('sleeve_length', 'STRING', 'Sleeve length'),
      ('style', 'STRING', 'Style'),
      ('occasion', 'STRING', 'Occasion'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Yarn
    'id': 714948,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('weight', 'STRING', 'Yarn weight'),
      ('fiber_content', 'STRING', 'Fiber content'),
      ('color', 'STRING', 'Color'),
      ('yardage', 'STRING', 'Yardage'),
    ]
  },
  {
    # Dehumidifiers
    'id': 715567,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Step Stools
    'id': 715608,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Shelving Units
    'id': 715788,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('dimensions', 'STRING', 'Dimensions'),
      ('number_of_compartments', 'NUMBER', 'Number of compartments'),
    ]
  },
  {
    # Patio Umbrellas
    'id': 715812,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Moka Pots
    'id': 719310,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('size', 'STRING', 'Size/Diameter'),
      ('capacity', 'STRING', 'Capacity'),
      ('non_stick', 'BOOLEAN', 'Non-stick coating'),
      ('dishwasher_safe', 'BOOLEAN', 'Dishwasher safe'),
      ('induction_compatible', 'BOOLEAN', 'Induction compatible'),
    ]
  },
  {
    # Women's Activewear
    'id': 719733,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # News Magazines
    'id': 720001,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Baking Supplies
    'id': 720533,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Bowls
    'id': 720873,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Psychology
    'id': 721260,
    'attributes': [
      ('title', 'STRING', 'Book title'),
      ('author', 'STRING', 'Author name'),
      ('publisher', 'STRING', 'Publisher'),
      ('isbn', 'STRING', 'ISBN'),
      ('publication_date', 'STRING', 'Publication date'),
      ('language', 'STRING', 'Language'),
      ('format', 'STRING', 'Format (Hardcover, Paperback, eBook)'),
      ('pages', 'NUMBER', 'Number of pages'),
      ('genre', 'STRING', 'Genre'),
    ]
  },
  {
    # Women's Crop Tops
    'id': 721733,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('sleeve_length', 'STRING', 'Sleeve length'),
      ('fit', 'STRING', 'Fit type'),
      ('style', 'STRING', 'Style'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Sports Magazines
    'id': 723425,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Dish Brushes
    'id': 723831,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Gaming Laptops
    'id': 724822,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('processor', 'STRING', 'CPU processor'),
      ('ram', 'STRING', 'RAM size'),
      ('storage', 'STRING', 'Storage capacity'),
      ('storage_type', 'STRING', 'Storage type (SSD, HDD)'),
      ('graphics_card', 'STRING', 'Graphics card (GPU)'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('refresh_rate', 'STRING', 'Refresh rate (Hz)'),
      ('resolution', 'STRING', 'Display resolution'),
      ('operating_system', 'STRING', 'Operating system'),
      ('color', 'STRING', 'Color'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # PlayStation Games
    'id': 725254,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('age_range', 'STRING', 'Age range'),
      ('number_of_players', 'STRING', 'Number of players'),
      ('play_time', 'STRING', 'Play time (minutes)'),
      ('theme', 'STRING', 'Theme'),
    ]
  },
  {
    # Women's Bodysuits
    'id': 725386,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('sleeve_length', 'STRING', 'Sleeve length'),
      ('fit', 'STRING', 'Fit type'),
      ('style', 'STRING', 'Style'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Aquarium Filters
    'id': 725795,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size (gallons)'),
      ('material', 'STRING', 'Material (Glass, Acrylic)'),
      ('dimensions', 'STRING', 'Dimensions'),
      ('shape', 'STRING', 'Shape'),
    ]
  },
  {
    # Baby Monitors
    'id': 726055,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('age_range', 'STRING', 'Age range'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('safety_certification', 'STRING', 'Safety certification'),
    ]
  },
  {
    # Tool Sets
    'id': 726691,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Measuring Cups
    'id': 727224,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('metal_type', 'STRING', 'Metal type (Gold, Silver, Platinum)'),
      ('stone_type', 'STRING', 'Stone type (if applicable)'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Hygrometers
    'id': 730766,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Studio Monitors
    'id': 730936,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('resolution', 'STRING', 'Resolution'),
      ('refresh_rate', 'STRING', 'Refresh rate (Hz)'),
      ('panel_type', 'STRING', 'Panel type'),
    ]
  },
  {
    # Ethernet Cables
    'id': 732277,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Cable type (USB-C, HDMI, etc.)'),
      ('length', 'STRING', 'Length'),
      ('compatibility', 'STRING', 'Compatibility'),
    ]
  },
  {
    # Ladles
    'id': 733286,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Men's Fragrances
    'id': 733612,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Music Downloads
    'id': 733689,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Children's Jewelry
    'id': 734780,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('metal_type', 'STRING', 'Metal type (Gold, Silver, Platinum)'),
      ('stone_type', 'STRING', 'Stone type (if applicable)'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Subwoofers
    'id': 735141,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's Bras
    'id': 735228,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Mobile Accessories
    'id': 735694,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Tablet Sleeves
    'id': 736189,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('storage', 'STRING', 'Storage capacity'),
      ('ram', 'STRING', 'RAM size'),
      ('operating_system', 'STRING', 'Operating system'),
      ('color', 'STRING', 'Color'),
      ('cellular', 'BOOLEAN', 'Cellular connectivity'),
    ]
  },
  {
    # Storage Bins
    'id': 737355,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('dimensions', 'STRING', 'Dimensions'),
      ('number_of_compartments', 'NUMBER', 'Number of compartments'),
    ]
  },
  {
    # Bottle Openers
    'id': 740703,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (Ballpoint, Gel, Rollerball)'),
      ('ink_color', 'STRING', 'Ink color'),
      ('tip_size', 'STRING', 'Tip size'),
      ('refillable', 'BOOLEAN', 'Refillable'),
      ('pack_count', 'NUMBER', 'Number of pens'),
    ]
  },
  {
    # Vinyl Records
    'id': 741293,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Multivitamins
    'id': 742501,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('product_type', 'STRING', 'Product type'),
      ('dosage', 'STRING', 'Dosage per serving'),
      ('quantity', 'NUMBER', 'Quantity (count)'),
      ('expiration_date', 'STRING', 'Expiration date'),
      ('ingredients', 'STRING', 'Key ingredients'),
    ]
  },
  {
    # Stand Mixers
    'id': 742751,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # 4K Ultra HD
    'id': 743033,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Graters
    'id': 743055,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Dash Cams
    'id': 743344,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Camera model'),
      ('megapixels', 'STRING', 'Megapixels'),
      ('sensor_size', 'STRING', 'Sensor size'),
      ('zoom', 'STRING', 'Optical zoom'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('weight', 'STRING', 'Weight'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Banjos
    'id': 744774,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Bath Mats
    'id': 744894,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('pattern', 'STRING', 'Pattern'),
      ('pile_height', 'STRING', 'Pile height'),
    ]
  },
  {
    # Changing Tables
    'id': 745075,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('age_range', 'STRING', 'Age range'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('safety_certification', 'STRING', 'Safety certification'),
    ]
  },
  {
    # Juicers
    'id': 746246,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Diamond Jewelry
    'id': 747278,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('metal_type', 'STRING', 'Metal type (Gold, Silver, Platinum)'),
      ('stone_type', 'STRING', 'Stone type (if applicable)'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Congas
    'id': 748420,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Acoustic Guitars
    'id': 749210,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('type', 'STRING', 'Type (Acoustic, Electric, Bass)'),
      ('color', 'STRING', 'Color/Finish'),
      ('number_of_strings', 'NUMBER', 'Number of strings'),
      ('body_material', 'STRING', 'Body material'),
      ('scale_length', 'STRING', 'Scale length'),
    ]
  },
  {
    # KVM Switches
    'id': 749315,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's Bootcut Jeans
    'id': 750347,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Girls' Sleepwear
    'id': 751753,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('age_range', 'STRING', 'Age range'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Earrings
    'id': 752366,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('metal_type', 'STRING', 'Metal type (Gold, Silver, Platinum)'),
      ('stone_type', 'STRING', 'Stone type (if applicable)'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Air Fryers
    'id': 752486,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Clocks
    'id': 754866,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Sunscreen
    'id': 757000,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Napkins
    'id': 758032,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's Cover-Ups
    'id': 758258,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # VR Headsets
    'id': 759045,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # CDs
    'id': 759267,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Smart Lights
    'id': 759327,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (Desk, Floor, Table)'),
      ('bulb_type', 'STRING', 'Bulb type'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('dimmable', 'BOOLEAN', 'Dimmable'),
    ]
  },
  {
    # Smart Bulbs
    'id': 759563,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (Desk, Floor, Table)'),
      ('bulb_type', 'STRING', 'Bulb type'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('dimmable', 'BOOLEAN', 'Dimmable'),
    ]
  },
  {
    # Girls' T-Shirts
    'id': 760004,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('age_range', 'STRING', 'Age range'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Ice Cream Scoops
    'id': 761031,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Cellos
    'id': 761521,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('type', 'STRING', 'Type'),
      ('key', 'STRING', 'Key'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color/Finish'),
    ]
  },
  {
    # Ironing Boards
    'id': 761664,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('height', 'STRING', 'Height'),
      ('material', 'STRING', 'Material'),
    ]
  },
  {
    # Action Figures
    'id': 761977,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Gloves
    'id': 762660,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Small Animal Food
    'id': 764148,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type'),
      ('size', 'STRING', 'Size'),
      ('animal_type', 'STRING', 'Animal type'),
    ]
  },
  {
    # Outdoor Play
    'id': 764231,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('age_range', 'STRING', 'Age range'),
      ('material', 'STRING', 'Material'),
      ('batteries_required', 'BOOLEAN', 'Batteries required'),
      ('number_of_players', 'STRING', 'Number of players'),
      ('theme', 'STRING', 'Theme'),
    ]
  },
  {
    # Bluetooth Speakers
    'id': 764862,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Microphones
    'id': 765635,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('storage', 'STRING', 'Storage capacity'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('color', 'STRING', 'Color'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Music Stands
    'id': 765665,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Power Tools
    'id': 766315,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Bandages
    'id': 767410,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Children's Books
    'id': 767412,
    'attributes': [
      ('title', 'STRING', 'Book title'),
      ('author', 'STRING', 'Author name'),
      ('publisher', 'STRING', 'Publisher'),
      ('isbn', 'STRING', 'ISBN'),
      ('publication_date', 'STRING', 'Publication date'),
      ('language', 'STRING', 'Language'),
      ('format', 'STRING', 'Format (Hardcover, Paperback, eBook)'),
      ('pages', 'NUMBER', 'Number of pages'),
      ('genre', 'STRING', 'Genre'),
    ]
  },
  {
    # Paint & Supplies
    'id': 771497,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (Acrylic, Oil, Watercolor)'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
      ('finish', 'STRING', 'Finish (Matte, Gloss)'),
    ]
  },
  {
    # Filing Cabinets
    'id': 772098,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('dimensions', 'STRING', 'Dimensions'),
      ('number_of_compartments', 'NUMBER', 'Number of compartments'),
    ]
  },
  {
    # Guitar Strings
    'id': 772333,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('metal_type', 'STRING', 'Metal type (Gold, Silver, Platinum)'),
      ('stone_type', 'STRING', 'Stone type (if applicable)'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Coasters
    'id': 772868,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Shaving
    'id': 775269,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Personal Care
    'id': 775921,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Car Audio
    'id': 777653,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Pasta
    'id': 777700,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Fashion Jewelry
    'id': 778486,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('metal_type', 'STRING', 'Metal type (Gold, Silver, Platinum)'),
      ('stone_type', 'STRING', 'Stone type (if applicable)'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Furniture
    'id': 779568,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color/Finish'),
      ('dimensions', 'STRING', 'Dimensions (L x W x H)'),
      ('assembly_required', 'BOOLEAN', 'Assembly required'),
      ('style', 'STRING', 'Style'),
    ]
  },
  {
    # Video Games
    'id': 779644,
    'attributes': [
      ('title', 'STRING', 'Game title'),
      ('platform', 'STRING', 'Platform (PlayStation, Xbox, Nintendo, PC)'),
      ('genre', 'STRING', 'Genre'),
      ('rating', 'STRING', 'ESRB rating'),
      ('release_date', 'STRING', 'Release date'),
      ('edition', 'STRING', 'Edition'),
    ]
  },
  {
    # Pillow Cases
    'id': 780092,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Breakfast Foods
    'id': 781972,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Ties & Bow Ties
    'id': 782242,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Desktop Computers
    'id': 782318,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Car Tires
    'id': 783321,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Tire size'),
      ('type', 'STRING', 'Type (All-season, Winter, Summer)'),
      ('speed_rating', 'STRING', 'Speed rating'),
      ('load_index', 'STRING', 'Load index'),
    ]
  },
  {
    # Computer Peripherals
    'id': 783594,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Sewing Kits
    'id': 786093,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('includes', 'STRING', 'What\'s included'),
    ]
  },
  {
    # Snacks
    'id': 786948,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Home & Garden Magazines
    'id': 788258,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Scarves
    'id': 788886,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Electric Guitars
    'id': 790059,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('type', 'STRING', 'Type (Acoustic, Electric, Bass)'),
      ('color', 'STRING', 'Color/Finish'),
      ('number_of_strings', 'NUMBER', 'Number of strings'),
      ('body_material', 'STRING', 'Body material'),
      ('scale_length', 'STRING', 'Scale length'),
    ]
  },
  {
    # Outdoor Tables
    'id': 790641,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Vintage Clothing
    'id': 794448,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Blankets
    'id': 798906,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Mouthwash
    'id': 798983,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Boys' Shirts
    'id': 799789,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('age_range', 'STRING', 'Age range'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Baby Bodysuits
    'id': 800190,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('age_range', 'STRING', 'Age range'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('safety_certification', 'STRING', 'Safety certification'),
    ]
  },
  {
    # Trading Cards
    'id': 802239,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Staplers
    'id': 802557,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (Desktop, Mini)'),
      ('staple_capacity', 'STRING', 'Staple capacity'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Blush
    'id': 803408,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Fantasy
    'id': 804407,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Dinner Plates
    'id': 804887,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's Bikinis
    'id': 805988,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Diapers
    'id': 806965,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('age_range', 'STRING', 'Age range'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('safety_certification', 'STRING', 'Safety certification'),
    ]
  },
  {
    # Smart Thermostats
    'id': 807077,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('capacity', 'STRING', 'Capacity (oz)'),
      ('material', 'STRING', 'Material'),
      ('insulation', 'STRING', 'Insulation type'),
      ('leak_proof', 'BOOLEAN', 'Leak-proof'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Bongos
    'id': 807177,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Boys' Shorts
    'id': 807336,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('age_range', 'STRING', 'Age range'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # AAA Batteries
    'id': 807432,
    'attributes': [
      ('voltage', 'STRING', 'Voltage per cell (typically 1.5V)'),
      ('chemistry', 'STRING', 'Battery chemistry (Alkaline, Lithium, etc.)'),
      ('quantity', 'NUMBER', 'Number of batteries in pack'),
      ('rechargeable', 'BOOLEAN', 'Rechargeable'),
      ('brand', 'STRING', 'Brand name'),
      ('expiration_date', 'STRING', 'Expiration date'),
    ]
  },
  {
    # Girls' Shorts
    'id': 807544,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('age_range', 'STRING', 'Age range'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Dog Toys
    'id': 807850,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('age_range', 'STRING', 'Age range'),
      ('breed_size', 'STRING', 'Breed size (Small, Medium, Large)'),
    ]
  },
  {
    # Magazines
    'id': 808023,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's Tank Tops
    'id': 811026,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('sleeve_length', 'STRING', 'Sleeve length'),
      ('fit', 'STRING', 'Fit type'),
      ('style', 'STRING', 'Style'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Networking
    'id': 811857,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Kitchen Towels
    'id': 812269,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('material', 'STRING', 'Material (Cotton, Microfiber, etc.)'),
      ('color', 'STRING', 'Color'),
      ('weight', 'STRING', 'Weight (GSM)'),
      ('absorbency', 'STRING', 'Absorbency level'),
    ]
  },
  {
    # Women's A-Line Skirts
    'id': 812454,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('length', 'STRING', 'Length'),
      ('type', 'STRING', 'Type'),
      ('ability_level', 'STRING', 'Ability level'),
      ('width', 'STRING', 'Width'),
    ]
  },
  {
    # USB-C Cables
    'id': 813524,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Cable type (USB-C, HDMI, etc.)'),
      ('length', 'STRING', 'Length'),
      ('compatibility', 'STRING', 'Compatibility'),
    ]
  },
  {
    # Women's Jackets
    'id': 813597,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Sustainable Fashion
    'id': 815243,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Blenders
    'id': 817297,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Fashion Magazines
    'id': 817460,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Weight Management
    'id': 817553,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('weight', 'STRING', 'Weight (lbs)'),
      ('material', 'STRING', 'Material'),
      ('type', 'STRING', 'Type (Fixed, Adjustable)'),
    ]
  },
  {
    # Women's Maxi Skirts
    'id': 819156,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('length', 'STRING', 'Length'),
      ('type', 'STRING', 'Type'),
      ('ability_level', 'STRING', 'Ability level'),
      ('width', 'STRING', 'Width'),
    ]
  },
  {
    # Key Holders
    'id': 820782,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Men's Casual Shirts
    'id': 821403,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('sleeve_length', 'STRING', 'Sleeve length'),
      ('fit', 'STRING', 'Fit type'),
      ('style', 'STRING', 'Style'),
    ]
  },
  {
    # Bath Accessories
    'id': 821605,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Studio Equipment
    'id': 822132,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's Clothing
    'id': 824617,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Rattles
    'id': 826084,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('age_range', 'STRING', 'Age range'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('safety_certification', 'STRING', 'Safety certification'),
    ]
  },
  {
    # Tubas
    'id': 828609,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Canned Goods
    'id': 829262,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Books & Media
    'id': 829289,
    'attributes': [
      ('title', 'STRING', 'Book title'),
      ('author', 'STRING', 'Author name'),
      ('publisher', 'STRING', 'Publisher'),
      ('isbn', 'STRING', 'ISBN'),
      ('publication_date', 'STRING', 'Publication date'),
      ('language', 'STRING', 'Language'),
      ('format', 'STRING', 'Format (Hardcover, Paperback, eBook)'),
      ('pages', 'NUMBER', 'Number of pages'),
      ('genre', 'STRING', 'Genre'),
    ]
  },
  {
    # LEGO
    'id': 829947,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Floor Lamps
    'id': 830150,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (Desk, Floor, Table)'),
      ('bulb_type', 'STRING', 'Bulb type'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('dimmable', 'BOOLEAN', 'Dimmable'),
    ]
  },
  {
    # Women's Sports Bras
    'id': 830309,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Tape Dispensers
    'id': 830750,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (Ballpoint, Gel, Rollerball)'),
      ('ink_color', 'STRING', 'Ink color'),
      ('tip_size', 'STRING', 'Tip size'),
      ('refillable', 'BOOLEAN', 'Refillable'),
      ('pack_count', 'NUMBER', 'Number of pens'),
    ]
  },
  {
    # USB Hubs
    'id': 831232,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('size', 'STRING', 'Size/Diameter'),
      ('capacity', 'STRING', 'Capacity'),
      ('non_stick', 'BOOLEAN', 'Non-stick coating'),
      ('dishwasher_safe', 'BOOLEAN', 'Dishwasher safe'),
      ('induction_compatible', 'BOOLEAN', 'Induction compatible'),
    ]
  },
  {
    # Lip Gloss
    'id': 831581,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Body Spray
    'id': 834353,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Camping Chairs
    'id': 836710,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('dimensions', 'STRING', 'Dimensions'),
      ('weight_capacity', 'STRING', 'Weight capacity'),
      ('assembly_required', 'BOOLEAN', 'Assembly required'),
    ]
  },
  {
    # Medical Supplies
    'id': 837012,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Bath
    'id': 837378,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Blu-ray
    'id': 838360,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Xylophones
    'id': 838373,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('storage', 'STRING', 'Storage capacity'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('color', 'STRING', 'Color'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Drawer Organizers
    'id': 839415,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('dimensions', 'STRING', 'Dimensions'),
      ('number_of_compartments', 'NUMBER', 'Number of compartments'),
    ]
  },
  {
    # Bird Cages
    'id': 840664,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('material', 'STRING', 'Material'),
      ('bar_spacing', 'STRING', 'Bar spacing'),
      ('includes_accessories', 'BOOLEAN', 'Includes accessories'),
    ]
  },
  {
    # Placemats
    'id': 841232,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Baby Wipes
    'id': 841659,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('age_range', 'STRING', 'Age range'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('safety_certification', 'STRING', 'Safety certification'),
    ]
  },
  {
    # Trombones
    'id': 841684,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('type', 'STRING', 'Type'),
      ('key', 'STRING', 'Key'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color/Finish'),
    ]
  },
  {
    # Encyclopedias
    'id': 841930,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Water Bottles
    'id': 842058,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('capacity', 'STRING', 'Capacity (oz)'),
      ('material', 'STRING', 'Material (Plastic, Stainless Steel, Glass)'),
      ('bpa_free', 'BOOLEAN', 'BPA-free'),
      ('insulated', 'BOOLEAN', 'Insulated'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # TV Wall Mounts
    'id': 842417,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Health Monitors
    'id': 843983,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('resolution', 'STRING', 'Resolution'),
      ('refresh_rate', 'STRING', 'Refresh rate (Hz)'),
      ('panel_type', 'STRING', 'Panel type'),
    ]
  },
  {
    # Game Controllers
    'id': 844003,
    'attributes': [
      ('title', 'STRING', 'Game title'),
      ('platform', 'STRING', 'Platform (PlayStation, Xbox, Nintendo, PC)'),
      ('genre', 'STRING', 'Genre'),
      ('rating', 'STRING', 'ESRB rating'),
      ('release_date', 'STRING', 'Release date'),
      ('edition', 'STRING', 'Edition'),
    ]
  },
  {
    # Exercise Bikes
    'id': 844403,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('type', 'STRING', 'Type (Mountain, Road, Hybrid, etc.)'),
      ('frame_size', 'STRING', 'Frame size'),
      ('wheel_size', 'STRING', 'Wheel size'),
      ('number_of_speeds', 'NUMBER', 'Number of speeds'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # DVD Players
    'id': 845237,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Remote Controls
    'id': 845301,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Glass Containers
    'id': 845603,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('dimensions', 'STRING', 'Dimensions'),
      ('number_of_compartments', 'NUMBER', 'Number of compartments'),
    ]
  },
  {
    # Women's Blazers
    'id': 846282,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Beer Glasses
    'id': 847091,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('capacity', 'STRING', 'Capacity (oz)'),
      ('type', 'STRING', 'Type (Pint, Mug, Stein)'),
      ('quantity', 'NUMBER', 'Quantity in set'),
    ]
  },
  {
    # Blinds & Shades
    'id': 848314,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Fishing Rods
    'id': 851956,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('length', 'STRING', 'Length'),
      ('action', 'STRING', 'Action (Light, Medium, Heavy)'),
      ('power', 'STRING', 'Power rating'),
      ('pieces', 'STRING', 'Number of pieces'),
    ]
  },
  {
    # Men's Shirts
    'id': 853941,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('sleeve_length', 'STRING', 'Sleeve length'),
      ('fit', 'STRING', 'Fit type'),
      ('style', 'STRING', 'Style'),
    ]
  },
  {
    # Women's Skinny Jeans
    'id': 854690,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('length', 'STRING', 'Length'),
      ('type', 'STRING', 'Type'),
      ('ability_level', 'STRING', 'Ability level'),
      ('width', 'STRING', 'Width'),
    ]
  },
  {
    # Clarinets
    'id': 855675,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('type', 'STRING', 'Type'),
      ('key', 'STRING', 'Key'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color/Finish'),
    ]
  },
  {
    # Night Lights
    'id': 858220,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (Desk, Floor, Table)'),
      ('bulb_type', 'STRING', 'Bulb type'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('dimmable', 'BOOLEAN', 'Dimmable'),
    ]
  },
  {
    # Women's Underwear
    'id': 860877,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's T-Shirts
    'id': 861714,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('sleeve_length', 'STRING', 'Sleeve length'),
      ('fit', 'STRING', 'Fit type'),
      ('style', 'STRING', 'Style'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Smart Smoke Detectors
    'id': 862312,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's Skirt Suits
    'id': 862341,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('length', 'STRING', 'Length'),
      ('type', 'STRING', 'Type'),
      ('ability_level', 'STRING', 'Ability level'),
      ('width', 'STRING', 'Width'),
    ]
  },
  {
    # Oils & Vinegars
    'id': 863071,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Xbox Games
    'id': 864950,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('age_range', 'STRING', 'Age range'),
      ('number_of_players', 'STRING', 'Number of players'),
      ('play_time', 'STRING', 'Play time (minutes)'),
      ('theme', 'STRING', 'Theme'),
    ]
  },
  {
    # Earbuds
    'id': 865794,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('storage', 'STRING', 'Storage capacity'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('color', 'STRING', 'Color'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Hamster Cages
    'id': 867652,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('material', 'STRING', 'Material'),
      ('includes_accessories', 'BOOLEAN', 'Includes accessories'),
    ]
  },
  {
    # Laundry Detergent
    'id': 869252,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # School Supplies
    'id': 869378,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Pens
    'id': 871970,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (Ballpoint, Gel, Rollerball)'),
      ('ink_color', 'STRING', 'Ink color'),
      ('tip_size', 'STRING', 'Tip size'),
      ('refillable', 'BOOLEAN', 'Refillable'),
      ('pack_count', 'NUMBER', 'Number of pens'),
    ]
  },
  {
    # Nintendo Games
    'id': 872183,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('age_range', 'STRING', 'Age range'),
      ('number_of_players', 'STRING', 'Number of players'),
      ('play_time', 'STRING', 'Play time (minutes)'),
      ('theme', 'STRING', 'Theme'),
    ]
  },
  {
    # Espresso Machines
    'id': 873769,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Android Phones
    'id': 874318,
    'attributes': [
      ('brand', 'STRING', 'Brand (Samsung, Google, OnePlus, etc.)'),
      ('model', 'STRING', 'Model name'),
      ('storage', 'STRING', 'Storage capacity'),
      ('ram', 'STRING', 'RAM size'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('resolution', 'STRING', 'Display resolution'),
      ('processor', 'STRING', 'Processor'),
      ('camera_megapixels', 'STRING', 'Camera megapixels'),
      ('battery_capacity', 'STRING', 'Battery capacity (mAh)'),
      ('operating_system', 'STRING', 'Android version'),
      ('color', 'STRING', 'Color'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Gold Jewelry
    'id': 875202,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('metal_type', 'STRING', 'Metal type (Gold, Silver, Platinum)'),
      ('stone_type', 'STRING', 'Stone type (if applicable)'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Fishing Tackle
    'id': 875820,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type'),
      ('color', 'STRING', 'Color'),
      ('weight', 'STRING', 'Weight'),
    ]
  },
  {
    # Monitors
    'id': 876365,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('resolution', 'STRING', 'Resolution'),
      ('refresh_rate', 'STRING', 'Refresh rate (Hz)'),
      ('panel_type', 'STRING', 'Panel type'),
    ]
  },
  {
    # Garment Steamers
    'id': 877234,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type'),
      ('water_capacity', 'STRING', 'Water capacity'),
      ('heat_up_time', 'STRING', 'Heat-up time'),
    ]
  },
  {
    # PlayStation
    'id': 878926,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Mixing Bowls
    'id': 880496,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Film Cameras
    'id': 882632,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Camera model'),
      ('megapixels', 'STRING', 'Megapixels'),
      ('sensor_size', 'STRING', 'Sensor size'),
      ('zoom', 'STRING', 'Optical zoom'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('weight', 'STRING', 'Weight'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Vitamins & Supplements
    'id': 885074,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('product_type', 'STRING', 'Product type'),
      ('dosage', 'STRING', 'Dosage per serving'),
      ('quantity', 'NUMBER', 'Quantity (count)'),
      ('expiration_date', 'STRING', 'Expiration date'),
      ('ingredients', 'STRING', 'Key ingredients'),
    ]
  },
  {
    # Men's Swim Trunks
    'id': 886697,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Business Laptops
    'id': 887133,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('processor', 'STRING', 'CPU processor'),
      ('ram', 'STRING', 'RAM size'),
      ('storage', 'STRING', 'Storage capacity'),
      ('storage_type', 'STRING', 'Storage type (SSD/HDD)'),
      ('operating_system', 'STRING', 'Operating system'),
      ('color', 'STRING', 'Color'),
      ('weight', 'STRING', 'Weight'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Gardening Tools
    'id': 888052,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Tool type'),
      ('material', 'STRING', 'Material'),
      ('handle_length', 'STRING', 'Handle length'),
    ]
  },
  {
    # Women's Capris
    'id': 890684,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('waist_size', 'STRING', 'Waist size'),
      ('inseam', 'STRING', 'Inseam length'),
      ('fit', 'STRING', 'Fit type'),
      ('rise', 'STRING', 'Rise'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
    ]
  },
  {
    # Ultrawide Monitors
    'id': 893056,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('resolution', 'STRING', 'Resolution'),
      ('refresh_rate', 'STRING', 'Refresh rate (Hz)'),
      ('panel_type', 'STRING', 'Panel type'),
    ]
  },
  {
    # Smart Plugs
    'id': 896301,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Office Chairs
    'id': 896647,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
      ('dimensions', 'STRING', 'Dimensions'),
      ('weight_capacity', 'STRING', 'Weight capacity'),
      ('assembly_required', 'BOOLEAN', 'Assembly required'),
    ]
  },
  {
    # Electrical
    'id': 898072,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Chocolate
    'id': 898217,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('flavor', 'STRING', 'Flavor'),
      ('package_size', 'STRING', 'Package size'),
      ('weight', 'STRING', 'Weight'),
      ('ingredients', 'STRING', 'Ingredients'),
      ('allergens', 'STRING', 'Allergen information'),
    ]
  },
  {
    # TVs
    'id': 898647,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Basketball
    'id': 898867,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Ball size'),
      ('material', 'STRING', 'Material'),
      ('indoor_outdoor', 'STRING', 'Indoor/Outdoor'),
    ]
  },
  {
    # MacBooks
    'id': 900256,
    'attributes': [
      ('title', 'STRING', 'Book title'),
      ('author', 'STRING', 'Author name'),
      ('publisher', 'STRING', 'Publisher'),
      ('isbn', 'STRING', 'ISBN'),
      ('publication_date', 'STRING', 'Publication date'),
      ('language', 'STRING', 'Language'),
      ('format', 'STRING', 'Format (Hardcover, Paperback, eBook)'),
      ('pages', 'NUMBER', 'Number of pages'),
      ('genre', 'STRING', 'Genre'),
    ]
  },
  {
    # Thermometers Indoor
    'id': 901106,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Fabric
    'id': 901918,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('width', 'STRING', 'Width'),
      ('color', 'STRING', 'Color'),
      ('pattern', 'STRING', 'Pattern'),
    ]
  },
  {
    # Mountain Bikes
    'id': 902309,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('type', 'STRING', 'Type (Mountain, Road, Hybrid, etc.)'),
      ('frame_size', 'STRING', 'Frame size'),
      ('wheel_size', 'STRING', 'Wheel size'),
      ('number_of_speeds', 'NUMBER', 'Number of speeds'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Men's Pants
    'id': 902767,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('waist_size', 'STRING', 'Waist size'),
      ('inseam', 'STRING', 'Inseam length'),
      ('fit', 'STRING', 'Fit type'),
      ('rise', 'STRING', 'Rise'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
    ]
  },
  {
    # Women's Formal Wear
    'id': 905602,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Men's Cardigans
    'id': 906016,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Self-Help
    'id': 907161,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Salt & Pepper Shakers
    'id': 909059,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's Athletic Jackets
    'id': 911701,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Men's Shorts
    'id': 912469,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Laptops
    'id': 915007,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('processor', 'STRING', 'CPU processor'),
      ('ram', 'STRING', 'RAM size'),
      ('storage', 'STRING', 'Storage capacity'),
      ('storage_type', 'STRING', 'Storage type (SSD/HDD)'),
      ('operating_system', 'STRING', 'Operating system'),
      ('color', 'STRING', 'Color'),
      ('weight', 'STRING', 'Weight'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Guitar Stands
    'id': 915340,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('type', 'STRING', 'Type (Acoustic, Electric, Bass)'),
      ('color', 'STRING', 'Color/Finish'),
      ('number_of_strings', 'NUMBER', 'Number of strings'),
      ('body_material', 'STRING', 'Body material'),
      ('scale_length', 'STRING', 'Scale length'),
    ]
  },
  {
    # Drum Sets
    'id': 916738,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Puzzles
    'id': 918100,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Dog Training
    'id': 919078,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Baby Products
    'id': 919299,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('age_range', 'STRING', 'Age range'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('safety_certification', 'STRING', 'Safety certification'),
    ]
  },
  {
    # Baby Health
    'id': 920382,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('age_range', 'STRING', 'Age range'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('safety_certification', 'STRING', 'Safety certification'),
    ]
  },
  {
    # Women's Coats
    'id': 920558,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Girls' Skirts
    'id': 921060,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('age_range', 'STRING', 'Age range'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Travel
    'id': 921323,
    'attributes': [
      ('title', 'STRING', 'Book title'),
      ('author', 'STRING', 'Author name'),
      ('publisher', 'STRING', 'Publisher'),
      ('isbn', 'STRING', 'ISBN'),
      ('publication_date', 'STRING', 'Publication date'),
      ('language', 'STRING', 'Language'),
      ('format', 'STRING', 'Format (Hardcover, Paperback, eBook)'),
      ('pages', 'NUMBER', 'Number of pages'),
      ('genre', 'STRING', 'Genre'),
    ]
  },
  {
    # Camera Lenses
    'id': 923152,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('focal_length', 'STRING', 'Focal length'),
      ('aperture', 'STRING', 'Maximum aperture'),
      ('lens_mount', 'STRING', 'Lens mount'),
      ('image_stabilization', 'BOOLEAN', 'Image stabilization'),
    ]
  },
  {
    # Men's Tank Tops
    'id': 924638,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('sleeve_length', 'STRING', 'Sleeve length'),
      ('fit', 'STRING', 'Fit type'),
      ('style', 'STRING', 'Style'),
    ]
  },
  {
    # Blood Pressure Monitors
    'id': 924722,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('resolution', 'STRING', 'Resolution'),
      ('refresh_rate', 'STRING', 'Refresh rate (Hz)'),
      ('panel_type', 'STRING', 'Panel type'),
    ]
  },
  {
    # Kayaking
    'id': 924892,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (Sit-on-top, Sit-in)'),
      ('length', 'STRING', 'Length'),
      ('capacity', 'STRING', 'Capacity (lbs)'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # iPad
    'id': 925187,
    'attributes': [
      ('model', 'STRING', 'iPad model'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('storage', 'STRING', 'Storage capacity'),
      ('cellular', 'BOOLEAN', 'Cellular connectivity'),
      ('color', 'STRING', 'Color'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Hammocks
    'id': 927215,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Metronomes
    'id': 930971,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # PA Systems
    'id': 931883,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Outdoor Furniture
    'id': 932669,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color/Finish'),
      ('dimensions', 'STRING', 'Dimensions (L x W x H)'),
      ('assembly_required', 'BOOLEAN', 'Assembly required'),
      ('style', 'STRING', 'Style'),
    ]
  },
  {
    # Organs
    'id': 932922,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Camera Accessories
    'id': 932957,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Camera model'),
      ('megapixels', 'STRING', 'Megapixels'),
      ('sensor_size', 'STRING', 'Sensor size'),
      ('zoom', 'STRING', 'Optical zoom'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('weight', 'STRING', 'Weight'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Serums
    'id': 933643,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Irons
    'id': 934698,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type'),
      ('power', 'STRING', 'Power (watts)'),
      ('water_capacity', 'STRING', 'Water capacity'),
      ('steam_settings', 'STRING', 'Steam settings'),
    ]
  },
  {
    # Hair Styling
    'id': 935120,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # French Horns
    'id': 936046,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Battery Chargers
    'id': 939079,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (USB, Wireless, Car)'),
      ('output', 'STRING', 'Output power/voltage'),
      ('compatibility', 'STRING', 'Device compatibility'),
      ('cable_length', 'STRING', 'Cable length'),
    ]
  },
  {
    # Oboes
    'id': 939230,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's Shirts
    'id': 939604,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('sleeve_length', 'STRING', 'Sleeve length'),
      ('fit', 'STRING', 'Fit type'),
      ('style', 'STRING', 'Style'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Cufflinks
    'id': 940977,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Manga
    'id': 941467,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('size', 'STRING', 'Size/Diameter'),
      ('capacity', 'STRING', 'Capacity'),
      ('non_stick', 'BOOLEAN', 'Non-stick coating'),
      ('dishwasher_safe', 'BOOLEAN', 'Dishwasher safe'),
      ('induction_compatible', 'BOOLEAN', 'Induction compatible'),
    ]
  },
  {
    # Humidifiers
    'id': 942164,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Calculators
    'id': 943584,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (Basic, Scientific, Graphing)'),
      ('display_type', 'STRING', 'Display type'),
      ('power_source', 'STRING', 'Power source'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Women's Athletic Tops
    'id': 945181,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
      ('sleeve_length', 'STRING', 'Sleeve length'),
      ('fit', 'STRING', 'Fit type'),
      ('style', 'STRING', 'Style'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Beds
    'id': 945223,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Cable Management
    'id': 947691,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Cable type (USB-C, HDMI, etc.)'),
      ('length', 'STRING', 'Length'),
      ('compatibility', 'STRING', 'Compatibility'),
    ]
  },
  {
    # Maracas
    'id': 948818,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Men's Parkas
    'id': 950244,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Fashion Accessories
    'id': 950353,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Philosophy
    'id': 950675,
    'attributes': [
      ('title', 'STRING', 'Book title'),
      ('author', 'STRING', 'Author name'),
      ('publisher', 'STRING', 'Publisher'),
      ('isbn', 'STRING', 'ISBN'),
      ('publication_date', 'STRING', 'Publication date'),
      ('language', 'STRING', 'Language'),
      ('format', 'STRING', 'Format (Hardcover, Paperback, eBook)'),
      ('pages', 'NUMBER', 'Number of pages'),
      ('genre', 'STRING', 'Genre'),
    ]
  },
  {
    # Serving Dishes
    'id': 952053,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Snare Drums
    'id': 952913,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Ladders
    'id': 953226,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Batteries & Chargers
    'id': 953986,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (USB, Wireless, Car)'),
      ('output', 'STRING', 'Output power/voltage'),
      ('compatibility', 'STRING', 'Device compatibility'),
      ('cable_length', 'STRING', 'Cable length'),
    ]
  },
  {
    # Tambourines
    'id': 954189,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Wall Sconces
    'id': 954998,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (Desk, Floor, Table)'),
      ('bulb_type', 'STRING', 'Bulb type'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('dimmable', 'BOOLEAN', 'Dimmable'),
    ]
  },
  {
    # Dog Food
    'id': 957235,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('age_range', 'STRING', 'Age range'),
      ('breed_size', 'STRING', 'Breed size (Small, Medium, Large)'),
    ]
  },
  {
    # Ceiling Lights
    'id': 957836,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (Desk, Floor, Table)'),
      ('bulb_type', 'STRING', 'Bulb type'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('dimmable', 'BOOLEAN', 'Dimmable'),
    ]
  },
  {
    # Pastry Brushes
    'id': 959187,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Throw Blankets
    'id': 959985,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Toothbrushes
    'id': 960913,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's Pencil Skirts
    'id': 960918,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (Ballpoint, Gel, Rollerball)'),
      ('ink_color', 'STRING', 'Ink color'),
      ('tip_size', 'STRING', 'Tip size'),
      ('refillable', 'BOOLEAN', 'Refillable'),
      ('pack_count', 'NUMBER', 'Number of pens'),
    ]
  },
  {
    # Sports Drinks
    'id': 960993,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Grills & Outdoor Cooking
    'id': 961098,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('type', 'STRING', 'Type (Gas, Charcoal, Electric)'),
      ('cooking_area', 'STRING', 'Cooking area (sq in)'),
      ('material', 'STRING', 'Material'),
    ]
  },
  {
    # Health & Wellness
    'id': 961226,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Buffets & Sideboards
    'id': 961237,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color/Finish'),
      ('dimensions', 'STRING', 'Dimensions (L x W x H)'),
      ('assembly_required', 'BOOLEAN', 'Assembly required'),
      ('style', 'STRING', 'Style'),
    ]
  },
  {
    # Tire Pressure Gauges
    'id': 964162,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Tire size'),
      ('type', 'STRING', 'Type (All-season, Winter, Summer)'),
      ('speed_rating', 'STRING', 'Speed rating'),
      ('load_index', 'STRING', 'Load index'),
    ]
  },
  {
    # Cat Trees
    'id': 964831,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Network Adapters
    'id': 965969,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Garden Statues
    'id': 966190,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Footwear
    'id': 966463,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Keyboards
    'id': 967250,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # 2-in-1 Laptops
    'id': 967662,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('processor', 'STRING', 'CPU processor'),
      ('ram', 'STRING', 'RAM size'),
      ('storage', 'STRING', 'Storage capacity'),
      ('storage_type', 'STRING', 'Storage type (SSD/HDD)'),
      ('operating_system', 'STRING', 'Operating system'),
      ('color', 'STRING', 'Color'),
      ('weight', 'STRING', 'Weight'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Nintendo Switch
    'id': 968579,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Bike Helmets
    'id': 968865,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('type', 'STRING', 'Type (Mountain, Road, Hybrid, etc.)'),
      ('frame_size', 'STRING', 'Frame size'),
      ('wheel_size', 'STRING', 'Wheel size'),
      ('number_of_speeds', 'NUMBER', 'Number of speeds'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Women's Pants
    'id': 969786,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('waist_size', 'STRING', 'Waist size'),
      ('inseam', 'STRING', 'Inseam length'),
      ('fit', 'STRING', 'Fit type'),
      ('rise', 'STRING', 'Rise'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material/Fabric'),
    ]
  },
  {
    # Cat Food
    'id': 971189,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size'),
      ('age_range', 'STRING', 'Age range'),
      ('type', 'STRING', 'Type'),
    ]
  },
  {
    # Blu-ray Players
    'id': 971448,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's Heels
    'id': 973579,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's Athletic Shorts
    'id': 974713,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Trumpets
    'id': 974856,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('type', 'STRING', 'Type'),
      ('key', 'STRING', 'Key'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color/Finish'),
    ]
  },
  {
    # Probiotics
    'id': 975093,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('product_type', 'STRING', 'Product type'),
      ('dosage', 'STRING', 'Dosage per serving'),
      ('quantity', 'NUMBER', 'Quantity (count)'),
      ('expiration_date', 'STRING', 'Expiration date'),
      ('ingredients', 'STRING', 'Key ingredients'),
    ]
  },
  {
    # Resistance Bands
    'id': 975477,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('resistance_level', 'STRING', 'Resistance level'),
      ('length', 'STRING', 'Length'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Pearl Jewelry
    'id': 975655,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('material', 'STRING', 'Material'),
      ('metal_type', 'STRING', 'Metal type (Gold, Silver, Platinum)'),
      ('stone_type', 'STRING', 'Stone type (if applicable)'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
    ]
  },
  {
    # Fish Food
    'id': 975680,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (Flakes, Pellets, Freeze-dried)'),
      ('size', 'STRING', 'Size'),
      ('fish_type', 'STRING', 'Fish type'),
    ]
  },
  {
    # Toys & Games
    'id': 976775,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('age_range', 'STRING', 'Age range'),
      ('material', 'STRING', 'Material'),
      ('batteries_required', 'BOOLEAN', 'Batteries required'),
      ('number_of_players', 'STRING', 'Number of players'),
      ('theme', 'STRING', 'Theme'),
    ]
  },
  {
    # Audio & Video
    'id': 976940,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Soft Drinks
    'id': 977044,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Flutes
    'id': 979641,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('type', 'STRING', 'Type'),
      ('key', 'STRING', 'Key'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color/Finish'),
    ]
  },
  {
    # Rechargeable Batteries
    'id': 979660,
    'attributes': [
      ('voltage', 'STRING', 'Voltage rating'),
      ('capacity', 'STRING', 'Battery capacity (mAh)'),
      ('chemistry', 'STRING', 'Battery chemistry type'),
      ('size', 'STRING', 'Battery size'),
      ('quantity', 'NUMBER', 'Number of batteries in pack'),
      ('rechargeable', 'BOOLEAN', 'Rechargeable'),
      ('brand', 'STRING', 'Brand name'),
    ]
  },
  {
    # Bedding
    'id': 981480,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('size', 'STRING', 'Size (Twin, Full, Queen, King)'),
      ('thread_count', 'STRING', 'Thread count'),
      ('material', 'STRING', 'Material (Cotton, Microfiber, etc.)'),
      ('color', 'STRING', 'Color'),
      ('pattern', 'STRING', 'Pattern'),
      ('care_instructions', 'STRING', 'Care instructions'),
    ]
  },
  {
    # Cutting Boards
    'id': 983761,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('type', 'STRING', 'Type (Straight, Quilting)'),
      ('length', 'STRING', 'Length'),
      ('count', 'NUMBER', 'Number of pins'),
    ]
  },
  {
    # Energy Drinks
    'id': 984640,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Protein Powder
    'id': 986285,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('product_type', 'STRING', 'Product type'),
      ('dosage', 'STRING', 'Dosage per serving'),
      ('quantity', 'NUMBER', 'Quantity (count)'),
      ('expiration_date', 'STRING', 'Expiration date'),
      ('ingredients', 'STRING', 'Key ingredients'),
    ]
  },
  {
    # Space Heaters
    'id': 988294,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Peelers
    'id': 990146,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Women's Swimwear
    'id': 992766,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Recorders
    'id': 992901,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('type', 'STRING', 'Type'),
      ('key', 'STRING', 'Key'),
      ('material', 'STRING', 'Material'),
      ('color', 'STRING', 'Color/Finish'),
    ]
  },
  {
    # History
    'id': 993314,
    'attributes': [
      ('title', 'STRING', 'Book title'),
      ('author', 'STRING', 'Author name'),
      ('publisher', 'STRING', 'Publisher'),
      ('isbn', 'STRING', 'ISBN'),
      ('publication_date', 'STRING', 'Publication date'),
      ('language', 'STRING', 'Language'),
      ('format', 'STRING', 'Format (Hardcover, Paperback, eBook)'),
      ('pages', 'NUMBER', 'Number of pages'),
      ('genre', 'STRING', 'Genre'),
    ]
  },
  {
    # Women's Mini Skirts
    'id': 993396,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('length', 'STRING', 'Length'),
      ('type', 'STRING', 'Type'),
      ('ability_level', 'STRING', 'Ability level'),
      ('width', 'STRING', 'Width'),
    ]
  },
  {
    # Men's Boxers
    'id': 994033,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model'),
      ('color', 'STRING', 'Color'),
      ('size', 'STRING', 'Size'),
    ]
  },
  {
    # Playpens
    'id': 997596,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('age_range', 'STRING', 'Age range'),
      ('size', 'STRING', 'Size'),
      ('color', 'STRING', 'Color'),
      ('material', 'STRING', 'Material'),
      ('safety_certification', 'STRING', 'Safety certification'),
    ]
  },
  {
    # Tripods
    'id': 998145,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Camera model'),
      ('megapixels', 'STRING', 'Megapixels'),
      ('sensor_size', 'STRING', 'Sensor size'),
      ('zoom', 'STRING', 'Optical zoom'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('weight', 'STRING', 'Weight'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
  {
    # Women's Pleated Skirts
    'id': 998336,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('length', 'STRING', 'Length'),
      ('type', 'STRING', 'Type'),
      ('ability_level', 'STRING', 'Ability level'),
      ('width', 'STRING', 'Width'),
    ]
  },
  {
    # Saxophones
    'id': 999454,
    'attributes': [
      ('brand', 'STRING', 'Brand'),
      ('model', 'STRING', 'Model name'),
      ('storage', 'STRING', 'Storage capacity'),
      ('screen_size', 'STRING', 'Screen size (inches)'),
      ('color', 'STRING', 'Color'),
      ('year', 'NUMBER', 'Release year'),
    ]
  },
]
