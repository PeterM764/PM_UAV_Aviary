import numpy as np
import os
from aviary.subsystems.mass.UAV_mass.variable_info.mass_variables import Aircraft
from aviary.subsystems.mass.UAV_mass.utils.materials_database import materials
from aviary.utils.functions import get_path

'''
These are the functions currently needed to load the airfoil 
CSV into the UAV mass wing and tail components
'''

def load_airfoil_csv(file_path, delimiter=',', header=False):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Airfoil CSV file '{file_path}' not found.")

    skip = 1 if header else 0
    data = np.loadtxt(file_path, delimiter=delimiter, skiprows=skip)

    if data.shape[1] < 2:
        raise ValueError('CSV must contain at least two columns for x and y coordinates.')

    x = data[:, 0]
    y = data[:, 1]

    x_min = np.min(x)
    x_max = np.max(x)
    chord_length = x_max - x_min

    if chord_length <= 0:
        raise ValueError('Invalid airfoil: chord length must be > 0.')

    x_normalized = (x - x_min) / chord_length
    y_normalized = y / chord_length

    return x_normalized, y_normalized
    
def load_airfoil_if_needed(comp, Part):

    if getattr(comp, "_airfoil_loaded", False):
        return

    path = comp.options[Part.AIRFOIL_PATH]

    # If an airfoil option is missing/blank in inputs, avoid resolving to CWD
    # (which can be a directory under tests) and use a sensible UAV default.
    default_name = 'n0012-il.csv'
    if Part is Aircraft.Wing:
        default_name = 'mh84-il.csv'
    default_path = os.path.join(os.path.dirname(__file__), default_name)

    if not path or str(path).strip() == '':
        path = default_path
    else:
        path = str(get_path(path))
        if os.path.isdir(path):
            path = default_path

    x, y = load_airfoil_csv(path, header=True)
    comp.n_area = 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))

    rib_materials = comp.options[Part.RIB_MATERIALS]
    comp.rho_rib = np.array([materials.get_item(m)[0] for m in rib_materials])

    rib_thickness, _ = comp.options[Part.RIB_THICKNESS]
    if len(rib_materials) != len(rib_thickness):
        raise ValueError("Mismatch in rib materials/thicknesses")

    comp._airfoil_loaded = True