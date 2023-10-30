# Terraria Reinforcement Learning
Reinforcement learning for Terraria boss fights

This was my first time using reinforcement learning, and I decided to try and train a model to defeat bosses in Terraria. This is an ongoing personal project and have so far defeated the first two bosses (eye of cthulhu and king slime).

Input data for the model is given as a pair of coordinates for the pixel location of the middle of the enemy. This is found by first using a hunter potion in game that makes all enemies emit a red glow, then applying a large blur effect to remove any small enemies and projectiles, and removing the average blue and green pixel value from the red to help remove white.

This leaves what can be seen in the bottom right corner of [this demo video](https://www.youtube.com/watch?v=aU-cUUBQJ2g&ab_channel=BoopJoop). A centroid algorithm is used to find the middle of the enemy, and some simple trigonometry is used to move the cursor to a suitable pixel location around the player, given the angle of the boss from the player.

The health bars of both the boss and the player are found by using a similar thresholding strategy and finding the leftmost dark pixel to calculate a percentage health. Optical character recognition was initially going to be used, however, this was too slow to maintain a good framerate.

The reward function rewards the player for lowering the boss' health and punishes the player for taking damage, with a much larger reward if the boss is defeated and a very large punishment for running too far away from the boss and having it despawn, or for taking too much damage and the player dying.

As aiming is already calculated by the enemy location, the only game inputs provided by the reinforcement learning algorithm are directional, being left, right, down and jump.
The environment is reset by using an in-game mod to delete all enemies and clear all items, teleporting the player back to world spawn, and healing the player with a health potion.
