### weight_manager.py ###
"""
This module manages weights assigned to security-related variables.
Users can specify weights for each variable to calculate the security index.
"""

class WeightManager:
    def __init__(self):
        self.weights = {}

    def set_weights(self, variable_weights):
        """
        Assign weights to variables.
        
        Parameters:
        variable_weights (dict): A dictionary with variable names as keys and weights as values.

        Returns:
        None
        """
        if not isinstance(variable_weights, dict):
            raise ValueError("Weights must be provided as a dictionary.")

        total_weight = sum(variable_weights.values())
        if not 0.99 <= total_weight <= 1.01:
            raise ValueError("Weights must sum up to 1.0.")

        self.weights = variable_weights

    def get_weights(self):
        """
        Retrieve the assigned weights.

        Returns:
        dict: Current weights.
        """
        if not self.weights:
            raise ValueError("Weights have not been set.")
        return self.weights