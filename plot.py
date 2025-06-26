import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator

def create_dataset(data):
    X = data[:, 0].reshape(-1, 1)
    y = data[:, 1].reshape(-1, 1)
    return X, y

def predict_crystal_ratio(flag_ratio, spline):
    """
    Predict crystal ratio based on flag ratio using the fitted spline.
    
    Args:
        flag_ratio: The ratio of flags between winning and losing team
        spline: Fitted PchipInterpolator spline
    
    Returns:
        Predicted crystal ratio
    """
    # Ensure input is within the valid range of the spline
    min_x = spline.x.min()
    max_x = spline.x.max()
    
    if flag_ratio < min_x:
        print(f"Warning: Flag ratio {flag_ratio} is below minimum value {min_x}. Returning 1.")
        return 1
    elif flag_ratio > max_x:
        print(f"Warning: Flag ratio {flag_ratio} is above maximum value {max_x}. Returning 4.")
        return 4

    # Predict using the spline
    crystal_ratio = spline(flag_ratio)
    return crystal_ratio

def plot_crystal_distribution():
    # Define the dataset
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

    X, y = create_dataset(dataset1)
    
    # Sort the data by x-values
    sorted_indices = np.argsort(X.flatten())
    X_sorted = X.flatten()[sorted_indices]
    y_sorted = y.flatten()[sorted_indices]
    
    # Handle duplicate x-values by averaging their y-values
    unique_x = []
    unique_y = []
    current_x = None
    y_sum = 0
    count = 0
    
    for i in range(len(X_sorted)):
        if i > 0 and abs(X_sorted[i] - current_x) < 1e-10:  # Same x-value (with floating point tolerance)
            # Accumulate y values
            y_sum += y_sorted[i]
            count += 1
        else:
            # Store previous group if it exists
            if current_x is not None:
                unique_x.append(current_x)
                unique_y.append(y_sum / count)
            
            # Start new group
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
    
    # Create the monotone cubic spline with unique values
    spline = PchipInterpolator(unique_x, unique_y)

    # Create a figure
    plt.figure(figsize=(12, 8))
    
    # Plot data points and spline
    plt.scatter(X, y, color='red', label='Data Points')
    
    # Create smooth line for prediction
    X_grid = np.linspace(min(X_sorted), max(X_sorted), 1000)
    plt.plot(X_grid, spline(X_grid), color='blue', label='Monotone Cubic Spline')
    
    plt.title('ProTanki Crystal Distribution')
    plt.xlabel('Flag Ratio (Winning Team / Losing Team)')
    plt.ylabel('Crystal Distribution Ratio')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('crystal_distribution.png', dpi=300)
    plt.show()
    
    return spline

def main():
    # Generate and display the plot, get the spline model
    spline = plot_crystal_distribution()
    
    # Allow user to predict crystal ratios
    while True:
        try:
            user_input = input("\nEnter flag ratio (or 'q' to quit): ")
            
            if user_input.lower() == 'q':
                break
                
            flag_ratio = float(user_input)
            crystal_ratio = predict_crystal_ratio(flag_ratio, spline)
            
            print(f"Flag Ratio: {flag_ratio}")
            print(f"Predicted Crystal Ratio: {crystal_ratio:.3f}")
            
        except ValueError:
            print("Please enter a valid number or 'q' to quit.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()