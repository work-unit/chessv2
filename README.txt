Welcome to Chess Engine 230!

When you unzip the submitted file, you will see the following:
    1. "Chess_Engine_Network.ipynb" - This preprocesses the data and
        trains the model used for the chess engine.
    2. "ChessFunctions.py" - This includes some proprietary chess
        helper functions brought to you by the Chess Engine 230 
        team. Read included docstrings for additional details.
    3. "environment.yml" - This contains all the dependencies needed
        to create the conda environment for this project.
    4. "FinalModel.joblib" - The best MLP model we created. This will
        be used when we play against the computer.
    5. "lichess_elite_2020-06.pgn" - The dataset. Contains thousands
        of chess games, from which we used 4,000.
    6. "PlayEngine.ipynb" - This notebook is interactive. It allows
        a user to play the computer which makes moves based on our 
        model predictions.
    7. "README.txt" - Read me for more details.


To run this project please perform the following steps:

Prepare Environment
    1. Execute "conda env create -f environment.yml" in a terminal to install 
       the environment.

    2. Execute "conda activate grand_master" in a terminal to activate the 
       grand_master environment.

    3. Execute "jupyter lab" in a terminal to open jupyter lab.

Preparing Data, Training the Model, and Analysis
    1. Run the "Chess_Engine_Network.ipynb".
       NOTE: The modeling portion of this notebook takes a long 
       time to run. In the second cell, you can change GAME_COUNT
       to something on the order of 10-100 to execute faster than 
       what was done to generate the final model. The final model
       we ended up with was trained on 4,000 chess games and took
       over 17 hours to train.

We also prepared a chess game. If you would like to run this:
    1. Run the "PlayEngine.ipynb" notebook.

    2. Follow the progression of the notebook to play along.
       NOTE: This is not a polished game so it is possible to break it
       if you enter a wrong move. To enter a move, specify which square 
       you move from, and which square you move to. For example, 
       to move the king's pawn to e4 (the most common chess opening), 
       type 'e2e4' when prompted. We hope you enjoy!

When you are finished with Chess Engine 230, you may remove
the environment by doing the following:
    1. Execute "./remove_environment.sh" in a terminal. Once again,
       this works on MacOS, and probably on Linux as well.

Thank you for an excellent quarter.

The Chess Engine 230 Team,

Jonah Breslow and Jeff Kagan

This Document was last modified 6/4/2021
