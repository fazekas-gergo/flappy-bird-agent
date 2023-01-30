from agents import *
from game import Game


def main(agent: MlAgent, *args, **kwargs):
    game = Game(*args, **kwargs)
    points = 0
    while True:
        new_points = game.attempt(agent)
        print(f"points: {new_points}")
        agent.train(better=new_points > points, points=new_points)
        points = new_points


if __name__ == "__main__":
    main(
        agent=MlAgent(),
        background_img="images/background.png",
        bird_img="images/bird.png",
        pipe_img="images/pipe.png",
        frame_rate=50,
    )
