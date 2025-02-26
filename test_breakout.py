import unittest
import pygame
from Breakout import Ball, Paddle, Brick, SCREEN_WIDTH, SCREEN_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT

class TestBreakoutGame(unittest.TestCase):

    def test_ball_speed_constant(self):
        """Test that the ball maintains a constant speed."""
        initial_speed = 4
        ball = Ball(initial_speed)
        initial_velocity = (abs(ball.dx), abs(ball.dy))
        
        # Simulate movement for a few frames
        for _ in range(10):
            ball.move()
        
        final_velocity = (abs(ball.dx), abs(ball.dy))
        self.assertEqual(initial_velocity, final_velocity, "Ball speed changed unexpectedly!")

    def test_paddle_movement_boundaries(self):
        """Test that the paddle stays within screen boundaries."""
        paddle = Paddle()
        
        # Move left beyond the boundary
        paddle.rect.x = 0
        paddle.move("LEFT")
        self.assertGreaterEqual(paddle.rect.x, 0, "Paddle moved out of left boundary!")

        # Move right beyond the boundary
        paddle.rect.x = SCREEN_WIDTH - PADDLE_WIDTH
        paddle.move("RIGHT")
        self.assertLessEqual(paddle.rect.x, SCREEN_WIDTH - PADDLE_WIDTH, "Paddle moved out of right boundary!")

    def test_brick_destruction_on_collision(self):
        """Test that bricks are destroyed when the ball collides with them."""
        ball = Ball(4)
        brick = Brick(100, 100)  # Create a brick
        ball.rect.x, ball.rect.y = 100, 100  # Position ball to collide with brick
        bricks = [brick]  # Create a list with one brick

        # Simulate collision
        for brick in bricks[:]:
            if ball.rect.colliderect(brick.rect):
                bricks.remove(brick)

        self.assertNotIn(brick, bricks, "Brick was not destroyed on collision!")

if __name__ == '__main__':
    unittest.main()
