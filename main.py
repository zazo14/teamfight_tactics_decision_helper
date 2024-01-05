import json
import time

from ultralytics import YOLO

# TODO: check use for from models.yolov8.yolov8_model import YoloV8Model
from utils.image_processing import process_image, grab_image
from utils.logger import setup_logger
from utils.overlay import create_overlay
from utils.probability_calculator import calculate_probability
from utils.score_calculator import calculate_score
from utils.actions import Game

import threading

import keyboard

def main():
    logger = setup_logger()
    game = Game()

    threading.Thread(target=create_overlay, args=(game, ), daemon=True).start()
    # Now you can use logger to log messages
    game.status = ('Starting TFT DecisionMaker')
    # Load YoloV8 model
    model = YOLO('models/yolov8/v4_large_1280_300.pt')
    game.status = ("Loaded YOLO model")

    game.status = ("Initialized game")


    # Load unit and composition data
    with open('data/units.json', 'r') as f:
        game.units = json.load(f)
    with open('data/compositions.json', 'r') as f:
        compositions = json.load(f)

    while game:
        #TODO: implement check for scouting
        if True:
            for i in range(len(game.players)):
                # Request user confirmation

                game.status = (f"Press Enter when screen {i + 1} is ready to be captured")
                keyboard.wait('enter')

                # Grab image
                #image = grab_image()

                # Save image to screenshots directory
                #image.save(f'screenshots/screen_{i + 1}.png')

                # Optional: wait between screenshots
                #time.sleep(1)
            # Process image
            game.status = ("Processing images")
            game.board = process_image(model)
            game.status = ("Images processed")
        game.status = ("Thinking ...")
        # Calculate probabilities and scores
        probabilities = calculate_probability(game.board, game.units, compositions)
        scores = calculate_score(probabilities, game.units, compositions, game.items)
        for composition_name, scores in scores.items():
            unit_score, comp_item_score = scores
            game.status = (
                f"For composition {composition_name}, unit score is {unit_score} and comp item score is {comp_item_score}")

        # Find the composition with the highest combined unit and item score
        game.best_composition = max(scores, key=lambda x: sum(scores[x]))
        game.status = game.best_composition
        # Decision logic

        game.decide_action()

if __name__ == "__main__":
    main()
