#!/usr/bin/env python3
"""
ProTanki Crystal Prediction - Main Program Runner

This program runs the complete workflow for crystal prediction:
1. Takes a screenshot of the battle fund area
2. Takes a screenshot of the score area  
3. Calculates the ratio and predicts crystal distribution
"""

import sys
import os
import time
import keyboard  # Added for key press detection

# Add the current directory to the Python path to ensure imports work
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

def run_battle_fund_screenshot():
    """Run the take_screenshot function from get_battle_fund_image.py"""
    try:
        print("="*60)
        print("STEP 1: Taking Battle Fund Screenshot")
        print("="*60)
        
        from get_battle_fund_image import take_screenshot as battle_fund_screenshot
        result = battle_fund_screenshot()
        
        if result:
            print(f"✓ Battle fund screenshot completed successfully: {result}")
            return True
        else:
            print("✗ Battle fund screenshot failed")
            return False
            
    except Exception as e:
        print(f"✗ Error in battle fund screenshot: {e}")
        return False

def run_score_screenshot():
    """Run the take_screenshot function from get_score_image.py"""
    try:
        print("\n" + "="*60)
        print("STEP 2: Taking Score Screenshot")
        print("="*60)
        
        from get_score_image import take_screenshot as score_screenshot
        result = score_screenshot()
        
        if result:
            print(f"✓ Score screenshot completed successfully: {result}")
            return True
        else:
            print("✗ Score screenshot failed")
            return False
            
    except Exception as e:
        print(f"✗ Error in score screenshot: {e}")
        return False

def run_scoreboard_screenshot():
    """Run the take_screenshot function from get_scoreboard_image.py"""
    try:
        print("\n" + "="*60)
        print("STEP 3: Taking Scoreboard Screenshot")
        print("="*60)
        
        from get_scoreboard_image import take_screenshot as scoreboard_screenshot
        result = scoreboard_screenshot()
        
        if result:
            print(f"✓ Scoreboard screenshot completed successfully: {result}")
            return True
        else:
            print("✗ Scoreboard screenshot failed")
            return False
            
    except Exception as e:
        print(f"✗ Error in scoreboard screenshot: {e}")
        return False

def run_ratio_calculation():
    """Run the main function from get_ratio_value.py"""
    try:
        print("\n" + "="*60)
        print("STEP 4: Calculating Ratio and Crystal Prediction")
        print("="*60)
        
        from get_ratio_value import main as ratio_main
        ratio_main()
        
        print("✓ Ratio calculation and crystal prediction completed")
        return True
        
    except Exception as e:
        print(f"✗ Error in ratio calculation: {e}")
        return False

def main():
    """Main function that orchestrates the entire workflow"""
    print("ProTanki Crystal Prediction - Starting Full Workflow")
    print("=" * 80)
    
    start_time = time.time()
    
    # Step 1: Battle Fund Screenshot
    if not run_battle_fund_screenshot():
        print("\n❌ Workflow stopped due to battle fund screenshot failure")
        return False
    
    # Add a small delay between steps
    # time.sleep(1)
    
    # Step 2: Score Screenshot  
    if not run_score_screenshot():
        print("\n❌ Workflow stopped due to score screenshot failure")
        return False
    
    # Add a small delay between steps
    # time.sleep(1)
    
    # Step 3: Scoreboard Screenshot
    if not run_scoreboard_screenshot():
        print("\n❌ Workflow stopped due to scoreboard screenshot failure")
        return False
    
    # Add a small delay between steps
    # time.sleep(1)
    
    # Step 4: Ratio Calculation and Crystal Prediction
    if not run_ratio_calculation():
        print("\n❌ Workflow stopped due to ratio calculation failure")
        return False
    
    # Calculate total execution time
    end_time = time.time()
    execution_time = end_time - start_time
    
    print("\n" + "="*80)
    print("🎉 WORKFLOW COMPLETED SUCCESSFULLY!")
    print(f"⏱️  Total execution time: {execution_time:.2f} seconds")
    print("="*80)
    
    return True

if __name__ == "__main__":
    try:
        # Play ready sound when program loads
        print("Program loaded. Playing ready notification...")
        try:
            import pygame
            pygame.mixer.init()
            # Get the directory where this script is located
            script_dir = os.path.dirname(os.path.abspath(__file__))
            ready_sound_path = os.path.join(script_dir, "sounds\\ready.mp3")
            pygame.mixer.music.load(ready_sound_path)
            pygame.mixer.music.play()
            # Wait for the sound to finish playing
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            pygame.mixer.quit()
        except Exception as sound_error:
            print(f"Could not play ready sound: {sound_error}")
        
        # Wait for TAB key press
        print("Press TAB key when you're ready to start the crystal prediction workflow...")
        keyboard.wait('tab')
        
        print("Starting workflow in 0.2 seconds...")
        time.sleep(0.2)  # Give user time to switch to the game window if needed
        
        success = main()
        if success:
            sys.exit(0)  # Success
        else:
            sys.exit(1)  # Failure
    except KeyboardInterrupt:
        print("\n\n⚠️  Workflow interrupted by user (Ctrl+C)")
        sys.exit(130)  # Standard exit code for Ctrl+C
    except Exception as e:
        print(f"\n\n💥 Unexpected error in main workflow: {e}")
        sys.exit(1)  # General error