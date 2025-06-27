import os
import numpy as np

def read_text_files():
    """
    Read all text files and return their contents.
    Returns a dictionary with file names as keys and their contents as values.
    """
    files_to_read = [
        'blue_scoreboard.txt',
        'red_scoreboard.txt', 
        'blue_score.txt',
        'red_score.txt',
        'battle_fund.txt',
        'ratio.txt'
    ]
    
    data = {}
    
    for filename in files_to_read:
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read().strip()
                
                # Process different file types
                if 'scoreboard' in filename:
                    # Scoreboard files contain multiple lines with numbers
                    lines = content.split('\n')
                    data[filename] = [line.strip() for line in lines if line.strip()]
                elif 'score' in filename:
                    # Score files contain either "N/A" or a number
                    data[filename] = content if content == "N/A" else content
                elif filename == 'battle_fund.txt':
                    # Battle fund contains a single number
                    data[filename] = content
                elif filename == 'ratio.txt':
                    # Ratio contains a single float
                    data[filename] = content
                else:
                    # Default: store as string
                    data[filename] = content
                    
        except FileNotFoundError:
            print(f"Warning: {filename} not found")
            data[filename] = None
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            data[filename] = None
    
    return data

def get_numeric_values():
    """
    Read files and convert numeric values to appropriate types.
    Returns a dictionary with processed numeric values.
    """
    data = read_text_files()
    processed_data = {}
    
    # Process blue scoreboard
    if data['blue_scoreboard.txt']:
        try:
            processed_data['blue_scoreboard'] = [int(x) for x in data['blue_scoreboard.txt'] if x.isdigit()]
        except ValueError:
            processed_data['blue_scoreboard'] = data['blue_scoreboard.txt']
    
    # Process red scoreboard  
    if data['red_scoreboard.txt']:
        try:
            processed_data['red_scoreboard'] = [int(x) for x in data['red_scoreboard.txt'] if x.isdigit()]
        except ValueError:
            processed_data['red_scoreboard'] = data['red_scoreboard.txt']
    
    # Process blue score
    if data['blue_score.txt']:
        if data['blue_score.txt'] == "N/A":
            processed_data['blue_score'] = None
        else:
            try:
                processed_data['blue_score'] = int(data['blue_score.txt'])
            except ValueError:
                processed_data['blue_score'] = data['blue_score.txt']
    
    # Process red score
    if data['red_score.txt']:
        if data['red_score.txt'] == "N/A":
            processed_data['red_score'] = None
        else:
            try:
                processed_data['red_score'] = int(data['red_score.txt'])
            except ValueError:
                processed_data['red_score'] = data['red_score.txt']
    
    # Process battle fund
    if data['battle_fund.txt']:
        try:
            processed_data['battle_fund'] = int(data['battle_fund.txt'])
        except ValueError:
            processed_data['battle_fund'] = data['battle_fund.txt']
    
    # Process ratio
    if data['ratio.txt']:
        try:
            processed_data['ratio'] = float(data['ratio.txt'])
        except ValueError:
            processed_data['ratio'] = data['ratio.txt']
    
    return processed_data

def calculate_crystal_distribution():
    """
    Calculate crystal distribution based on the data from text files.
    Returns winning and losing team crystal distributions.
    """
    # Get the data from files
    data = get_numeric_values()
    
    # Extract values with validation
    BattleFund = data.get('battle_fund')
    PredictionRatio = data.get('ratio')
    BlueScoreboard = data.get('blue_scoreboard', [])
    RedScoreboard = data.get('red_scoreboard', [])
    
    # Check if we have valid data
    if (BattleFund is None or PredictionRatio is None or 
        not BlueScoreboard or not RedScoreboard):
        print("Error: Missing or invalid data in files")
        print(f"BattleFund: {BattleFund}")
        print(f"PredictionRatio: {PredictionRatio}")
        print(f"BlueScoreboard: {BlueScoreboard}")
        print(f"RedScoreboard: {RedScoreboard}")
        return None
    
    # Convert to numpy arrays
    BlueScoreboard = np.array(BlueScoreboard)
    RedScoreboard = np.array(RedScoreboard)
    
    # Determine winning and losing teams based on total scores
    blue_total = np.sum(BlueScoreboard)
    red_total = np.sum(RedScoreboard)
    
    if blue_total > red_total:
        WinningScore = BlueScoreboard
        LossingScore = RedScoreboard
        winning_team = "Blue"
        losing_team = "Red"
    else:
        WinningScore = RedScoreboard
        LossingScore = BlueScoreboard
        winning_team = "Red"
        losing_team = "Blue"
    
    # Calculate crystal distribution
    LossingTeamCrystals = BattleFund * (1 / (PredictionRatio + 1))
    WinningTeamCrystals = BattleFund - LossingTeamCrystals

    WinningCrystal = WinningTeamCrystals / sum(WinningScore)
    LossingCrystal = LossingTeamCrystals / sum(LossingScore)

    WinningIndividualCrystals = np.round(np.multiply(WinningScore, WinningCrystal), 0)
    LossingIndividualCrystals = np.round(np.multiply(LossingScore, LossingCrystal), 0)

    # Return results as dictionary
    results = {
        'winning_team': winning_team,
        'losing_team': losing_team,
        'winning_crystals': WinningIndividualCrystals.astype(int),
        'losing_crystals': LossingIndividualCrystals.astype(int),
        'winning_total_crystals': float(WinningTeamCrystals),
        'losing_total_crystals': float(LossingTeamCrystals),
        'battle_fund': BattleFund,
        'prediction_ratio': PredictionRatio
    }
    
    return results

def print_crystal_distribution():
    """
    Print the crystal distribution in a readable format.
    """
    results = calculate_crystal_distribution()
    
    if results is None:
        print("Could not calculate crystal distribution due to missing data.")
        return
    
    print("=== Crystal Distribution ===")
    print(f"Battle Fund: {results['battle_fund']}")
    print(f"Prediction Ratio: {results['prediction_ratio']:.3f}")
    print(f"Winning Team: {results['winning_team']}")
    print(f"Losing Team: {results['losing_team']}")
    print(f"\nIndividual Crystal Distribution:")
    print(f"{results['winning_team']} Team: {results['winning_crystals']}")
    print(f"{results['losing_team']} Team: {results['losing_crystals']}")

def get_crystal_data():
    """
    Simple function to get crystal distribution data.
    Returns the results dictionary or None if calculation fails.
    """
    return calculate_crystal_distribution()

def get_team_crystals(team='winning'):
    """
    Get crystals for a specific team.
    
    Args:
        team (str): 'winning', 'losing', 'blue', or 'red'
    
    Returns:
        numpy array of individual crystal amounts
    """
    results = calculate_crystal_distribution()
    if results is None:
        return None
    
    if team.lower() == 'winning':
        return results['winning_crystals']
    elif team.lower() == 'losing':
        return results['losing_crystals']
    elif team.lower() == 'blue':
        if results['winning_team'] == 'Blue':
            return results['winning_crystals']
        else:
            return results['losing_crystals']
    elif team.lower() == 'red':
        if results['winning_team'] == 'Red':
            return results['winning_crystals']
        else:
            return results['losing_crystals']
    else:
        return None

def save_results_to_file(filename='crystal_results.txt'):
    """
    Save crystal distribution results to a text file.
    
    Args:
        filename (str): Name of the output file
    """
    results = calculate_crystal_distribution()
    if results is None:
        print("Cannot save results - calculation failed")
        return False
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=== Crystal Distribution Results ===\n")
            f.write(f"Battle Fund: {results['battle_fund']}\n")
            f.write(f"Prediction Ratio: {results['prediction_ratio']:.3f}\n")
            f.write(f"Winning Team: {results['winning_team']}\n")
            f.write(f"Losing Team: {results['losing_team']}\n")
            f.write(f"Winning Team Total Crystals: {results['winning_total_crystals']:.0f}\n")
            f.write(f"Losing Team Total Crystals: {results['losing_total_crystals']:.0f}\n")
            f.write(f"\nIndividual Crystal Distribution:\n")
            f.write(f"{results['winning_team']} Team: {list(results['winning_crystals'])}\n")
            f.write(f"{results['losing_team']} Team: {list(results['losing_crystals'])}\n")
        
        print(f"Results saved to {filename}")
        return True
    except Exception as e:
        print(f"Error saving results: {e}")
        return False

def save_team_crystals_to_files():
    """
    Save individual crystal distributions to separate files for red and blue teams.
    Creates red_diamonds.txt and blue_diamonds.txt files.
    """
    results = calculate_crystal_distribution()
    if results is None:
        print("Cannot save team crystals - calculation failed")
        return False
    
    try:
        # Determine which team is which
        if results['winning_team'] == 'Red':
            red_crystals = results['winning_crystals']
            blue_crystals = results['losing_crystals']
        else:
            red_crystals = results['losing_crystals']
            blue_crystals = results['winning_crystals']
        
        # Save red team crystals
        with open('red_diamonds.txt', 'w', encoding='utf-8') as f:
            for crystal in red_crystals:
                f.write(f"{crystal}\n")
        
        # Save blue team crystals
        with open('blue_diamonds.txt', 'w', encoding='utf-8') as f:
            for crystal in blue_crystals:
                f.write(f"{crystal}\n")
        
        print("Individual crystal distributions saved:")
        print(f"Red team crystals saved to red_diamonds.txt: {list(red_crystals)}")
        print(f"Blue team crystals saved to blue_diamonds.txt: {list(blue_crystals)}")
        return True
        
    except Exception as e:
        print(f"Error saving team crystal files: {e}")
        return False

# Example usage
if __name__ == "__main__":
    # Read and display raw data
    raw_data = read_text_files()
    print("Raw file data:")
    for filename, content in raw_data.items():
        print(f"{filename}: {content}")
    
    print("\n" + "="*50 + "\n")
    
    # Calculate and display crystal distribution
    print_crystal_distribution()
    
    print("\n" + "="*50 + "\n")
    
    # Save individual crystal distributions to files
    save_team_crystals_to_files()