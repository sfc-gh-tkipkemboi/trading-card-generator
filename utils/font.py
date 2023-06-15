"""
font.py

This module contains utility functions for handling fonts in the trading card generator application.
"""

from fontTools.ttLib import TTFont

def make_font(font_path, axis_value, output_path):
    """
    Adjust the weight of a variable font and save the new font to a file.

    Parameters:
    font_path (str): The path to the variable font file.
    axis_value (int): The new weight value for the font. 
                      A value of 700 is typically considered "bold".
    output_path (str): The path where the new font file will be saved.
    """
    font = TTFont(font_path)
    # Set the weight axis value
    font['fvar'].axes[0].defaultValue = axis_value
    font.save(output_path)

make_font('assets/RobotoMono-VariableFont_wght.ttf', 700, 'assets/RobotoMono-Bold.ttf')