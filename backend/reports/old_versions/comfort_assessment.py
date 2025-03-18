import numpy as np


class ComfortLevelAssessment:
    def __init__(self):
        # Comfort ranges based on ASHRAE and indoor air quality standards
        self.comfort_ranges = {
            'temperature': {
                'optimal_min': 20,
                'optimal_max': 24,
                'acceptable_min': 18,
                'acceptable_max': 26
            },
            'humidity': {
                'optimal_min': 30,
                'optimal_max': 50,
                'acceptable_min': 20,
                'acceptable_max': 60
            },
            'co2': {
                'optimal_max': 400,  # ppm
                'acceptable_max': 1000,  # ppm
                'poor_max': 2000  # ppm
            },
            'voc': {
                'optimal_max': 50,  # ppb
                'acceptable_max': 200,  # ppb
                'poor_max': 500  # ppb
            }
        }

    def _score_parameter(self, value, param_type):
        """
        Score individual parameter based on its value and predefined ranges
        Returns a score between 0 (worst) and 100 (best)
        """
        ranges = self.comfort_ranges[param_type]

        if param_type in ['temperature', 'humidity']:
            # For temperature and humidity, calculate score based on closeness to optimal range
            if ranges['optimal_min'] <= value <= ranges['optimal_max']:
                return 100
            elif ranges['acceptable_min'] <= value <= ranges['acceptable_max']:
                # Linear interpolation for acceptable range
                if value < ranges['optimal_min']:
                    return 50 + (value - ranges['acceptable_min']) / (ranges['optimal_min'] - ranges['acceptable_min']) * 50
                else:
                    return 50 - (value - ranges['optimal_max']) / (ranges['acceptable_max'] - ranges['optimal_max']) * 50
            else:
                return 0

        elif param_type in ['co2', 'voc']:
            # For CO2 and VOC, lower is better
            if value <= ranges['optimal_max']:
                return 100
            elif value <= ranges['acceptable_max']:
                # Linear interpolation for acceptable range
                return 100 - (value - ranges['optimal_max']) / (ranges['acceptable_max'] - ranges['optimal_max']) * 50
            elif value <= ranges['poor_max']:
                # Linear interpolation for poor range
                return 50 - (value - ranges['acceptable_max']) / (ranges['poor_max'] - ranges['acceptable_max']) * 50
            else:
                return 0

    def assess_comfort(self, temperature, humidity, co2, voc):
        """
        Comprehensive comfort level assessment

        Args:
            temperature (float): Temperature in Celsius
            humidity (float): Relative humidity percentage
            co2 (float): CO2 concentration in ppm
            voc (float): VOC concentration in ppb

        Returns:
            dict: Comfort assessment with individual and overall scores
        """
        # Calculate individual parameter scores
        temp_score = self._score_parameter(temperature, 'temperature')
        humidity_score = self._score_parameter(humidity, 'humidity')
        co2_score = self._score_parameter(co2, 'co2')
        voc_score = self._score_parameter(voc, 'voc')

        # Calculate overall comfort score (weighted average)
        # More weight to temperature and CO2 as they have more direct impact on comfort
        overall_score = (
            temp_score * 0.3 +
            humidity_score * 0.2 +
            co2_score * 0.3 +
            voc_score * 0.2
        )

        # Categorize overall comfort
        if overall_score >= 90:
            comfort_category = "Excellent"
        elif overall_score >= 75:
            comfort_category = "Good"
        elif overall_score >= 50:
            comfort_category = "Moderate"
        elif overall_score >= 25:
            comfort_category = "Poor"
        else:
            comfort_category = "Unacceptable"

        return {
            'temperature': {
                'value': temperature,
                'score': temp_score,
                'assessment': self._interpret_parameter_score(temp_score, 'temperature')
            },
            'humidity': {
                'value': humidity,
                'score': humidity_score,
                'assessment': self._interpret_parameter_score(humidity_score, 'humidity')
            },
            'co2': {
                'value': co2,
                'score': co2_score,
                'assessment': self._interpret_parameter_score(co2_score, 'co2')
            },
            'voc': {
                'value': voc,
                'score': voc_score,
                'assessment': self._interpret_parameter_score(voc_score, 'voc')
            },
            'overall_score': overall_score,
            'comfort_category': comfort_category
        }

    def _interpret_parameter_score(self, score, param_type):
        """
        Provide a textual interpretation of the parameter score
        """
        if score >= 90:
            return f"{param_type.upper()} levels are optimal"
        elif score >= 75:
            return f"{param_type.upper()} levels are good"
        elif score >= 50:
            return f"{param_type.upper()} levels are moderate"
        elif score >= 25:
            return f"{param_type.upper()} levels are poor"
        else:
            return f"{param_type.upper()} levels are unacceptable"

# Example usage


def evaluate_monitoring_data(times, temperatures, humidities, co2_levels, voc_levels):
    """
    Evaluate comfort levels for a series of measurements

    Args:
        times (list): Time points
        temperatures (list): Temperature measurements
        humidities (list): Humidity measurements
        co2_levels (list): CO2 concentration measurements
        voc_levels (list): VOC concentration measurements

    Returns:
        list: Comfort assessments for each time point
    """
    comfort_assessor = ComfortLevelAssessment()

    assessments = []
    for i in range(len(times)):
        assessment = comfort_assessor.assess_comfort(
            temperatures[i],
            humidities[i],
            co2_levels[i],
            voc_levels[i]
        )
        assessment['time'] = times[i]
        assessments.append(assessment)

    return assessments


# In your Quarto document, you can add this to print or analyze the comfort levels
if __name__ == "__main__":
    # Sample monitoring data
    times = ['8:30', '9:00', '9:30', '10:00',
             '10:30', '11:00', '11:30', '12:00']
    temperature = [22.5, 23.1, 23.8, 24.2, 24.7, 25.0, 25.3, 25.6]
    humidity = [45, 47, 46, 44, 42, 40, 39, 38]
    co2 = [400, 450, 500, 550, 600, 650, 700, 750]
    voc = [50, 55, 60, 65, 70, 75, 80, 85]

    # Evaluate comfort levels
    comfort_assessments = evaluate_monitoring_data(
        times, temperature, humidity, co2, voc
    )

    # Print detailed comfort assessments
    for assessment in comfort_assessments:
        print(f"Time: {assessment['time']}")
        print(
            f"Overall Comfort: {assessment['comfort_category']} (Score: {assessment['overall_score']:.2f})")
        for param, details in assessment.items():
            if param not in ['time', 'overall_score', 'comfort_category']:
                print(
                    f"{param.capitalize()}: {details['value']} - Score: {details['score']:.2f} ({details['assessment']})")
        print("---")
