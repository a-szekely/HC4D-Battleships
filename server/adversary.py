import numpy as np
import GPy

GAME_BOARD_SIZE = 600
BOMB_RADIUS = 20


def pick_bomb_location(guess_history, success_history):
    # Generate new valid attempt
    if len(success_history) == 0:
        new_guess = np.random.random_sample(2) * GAME_BOARD_SIZE
    else:

        # Set up GP model using game history
        ker = GPy.kern.RBF(input_dim=2, variance=1, lengthscale=1)
        m = GPy.models.GPClassification(np.vstack(guess_history), np.vstack(success_history), ker)

        new_guess = None
        higher_than_gpmean = True
        while higher_than_gpmean:

            # Ensure that bombing locations are far enough away from each other
            too_close = True
            while too_close:
                too_close = False
                # Generate a new guess
                new_guess = np.random.random_sample(2) * GAME_BOARD_SIZE

                for guess in guess_history:
                    # If the new guess is too close to any previously generated point, reject it
                    if np.linalg.norm(guess - new_guess) < 2 * BOMB_RADIUS:
                        too_close = True

            # Once found a valid solution, predict mean of the categorical GP at that location
            new_guess = np.expand_dims(new_guess, 0)
            guess_mean = m.predict(new_guess)[0]

            # Sample a uniform distribution, if the value is lower than the GP mean, accept this guess
            if np.random.rand(1) < guess_mean:
                higher_than_gpmean = False

    return new_guess
