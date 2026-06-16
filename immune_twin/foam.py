import numpy as np

def entropy(field_values):
    """Вычисление энтропии Шеннона для массива значений."""
    if len(field_values) == 0:
        return 0
    hist, _ = np.histogram(field_values, bins=20, density=True)
    hist = hist[hist > 0]
    return -np.sum(hist * np.log2(hist))

def compute_phi(foam_field):
    """Глобальная Φ как пространственная энтропия foam-поля."""
    flat = foam_field.flatten()
    return entropy(flat)
