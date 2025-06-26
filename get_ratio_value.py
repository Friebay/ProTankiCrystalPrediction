import numpy as np
from scipy.interpolate import PchipInterpolator
from plot import predict_crystal_ratio


def create_spline_model():
    """
    Create the spline model using the same dataset from plot.py
    
    Returns:
        PchipInterpolator: The fitted spline model
    """
    # Define the dataset (same as in plot.py)
    dataset1 = np.array([
        [1.020, 1.525],
        [1.049, 1.560],
        [1.087, 1.607],
        [1.149, 1.673],
        [1.163, 1.688],
        [1.193, 1.720],
        [1.250, 1.778],
        [1.250, 1.778],
        [1.284, 1.811],
        [1.333, 1.862],
        [1.364, 1.887],
        [1.389, 1.907],
        [1.389, 1.907],
        [1.400, 1.922],
        [1.417, 1.932],
        [1.429, 1.944],
        [1.450, 1.960],
        [1.485, 1.989],
        [1.500, 2.002],
        [1.800, 2.214],
        [1.852, 2.249],
        [1.887, 2.268],
        [1.931, 2.295],
        [2.041, 2.356],
        [2.250, 2.459],
        [2.500, 2.595],
        [2.730, 2.659],
        [3.000, 2.750],
        [3.000, 2.757],
        [3.125, 2.787],
        [3.333, 2.846],
        [3.511, 2.892],
        [4.000, 3.010],
        [4.667, 3.118],
        [5.000, 3.168],
        [5.000, 3.168],
        [5.479, 3.229],
        [5.801, 3.265],
        [5.941, 3.282],
        [6.000, 3.288],
        [6.301, 3.315],
        [7.500, 3.412],
        [7.500, 3.412],
        [8.000, 3.444],
        [8.333, 3.462],
        [8.500, 3.474],
        [9.336, 3.516],
        [10.000, 3.550],
        [10.000, 3.551],
        [11.111, 3.586],
        [11.111, 3.591],
        [12.333, 3.625],
        [14.000, 3.666],
        [14.271, 3.673],
        [15.714, 3.704],
        [16.667, 3.721],
        [21.357, 3.777],
        [22.000, 3.782],
        [29.000, 3.834],
        [30.000, 3.839],
        [33.333, 3.854],
        [34.448, 3.859],
        [37.500, 3.871],
        [50.000, 3.902]
    ])

    X = dataset1[:, 0]
    y = dataset1[:, 1]
    
    # Sort the data by x-values
    sorted_indices = np.argsort(X)
    X_sorted = X[sorted_indices]
    y_sorted = y[sorted_indices]
    
    # Handle duplicate x-values by averaging their y-values
    unique_x = []
    unique_y = []
    current_x = None
    y_sum = 0
    count = 0
    
    for i in range(len(X_sorted)):
        if i > 0 and abs(X_sorted[i] - current_x) < 1e-10:  # Same x-value
            y_sum += y_sorted[i]
            count += 1
        else:
            if current_x is not None:
                unique_x.append(current_x)
                unique_y.append(y_sum / count)
            
            current_x = X_sorted[i]
            y_sum = y_sorted[i]
            count = 1
    
    # Add the last group
    if count > 0:
        unique_x.append(current_x)
        unique_y.append(y_sum / count)
    
    # Create arrays from the unique values
    unique_x = np.array(unique_x)
    unique_y = np.array(unique_y)
    
    # Create the monotone cubic spline
    spline = PchipInterpolator(unique_x, unique_y)
    return spline


def read_score_files():
    """
    Read the red_score.txt and blue_score.txt files and return their values.
    
    Returns:
        tuple: (red_score, blue_score) as integers
    """
    try:
        # Read red score
        with open('red_score.txt', 'r') as file:
            red_score = int(file.read().strip())
        
        # Read blue score
        with open('blue_score.txt', 'r') as file:
            blue_score = int(file.read().strip())
        
        return red_score, blue_score
    
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        return None, None
    except ValueError as e:
        print(f"Error: Invalid number format - {e}")
        return None, None
    except Exception as e:
        print(f"Error reading files: {e}")
        return None, None


def get_ratio_value():
    """
    Calculate the ratio between winner and loser scores.
    
    Returns:
        float: The ratio of winner_score to loser_score, or None if calculation fails
    """
    red_score, blue_score = read_score_files()
    
    if red_score is None or blue_score is None:
        return None
    
    # Determine winner and loser
    if red_score > blue_score:
        winner_score, loser_score = red_score, blue_score
    elif blue_score > red_score:
        winner_score, loser_score = blue_score, red_score
    else:
        # Tie case
        return 1.0
    
    if loser_score == 0:
        print("Warning: Loser score is 0, cannot calculate ratio")
        return float('inf') if winner_score > 0 else 1.0
    
    ratio = winner_score / loser_score
    return ratio


def main():
    """
    Main function to demonstrate reading the score files, calculating ratio, and predicting crystal distribution.
    """
    red_score, blue_score = read_score_files()
    
    if red_score is not None and blue_score is not None:
        print(f"Red score: {red_score}")
        print(f"Blue score: {blue_score}")
        
        # Determine winner
        if red_score > blue_score:
            print(f"Winner: Red ({red_score}), Loser: Blue ({blue_score})")
        elif blue_score > red_score:
            print(f"Winner: Blue ({blue_score}), Loser: Red ({red_score})")
        else:
            print("Tie game!")
        
        ratio = get_ratio_value()
        if ratio is not None:
            print(f"Winner to Loser ratio: {ratio:.2f}")
            
            # Create the spline model and predict crystal distribution
            try:
                spline = create_spline_model()
                crystal_ratio = predict_crystal_ratio(ratio, spline)
                print(f"Predicted Crystal Distribution Ratio: {crystal_ratio:.3f}")
            except Exception as e:
                print(f"Error predicting crystal ratio: {e}")
        else:
            print("Cannot calculate ratio")
    else:
        print("Failed to read score files")


if __name__ == "__main__":
    main()