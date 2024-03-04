

# Report Overview

In the realm of game development, creativity often intertwines with technical prowess, presenting unique challenges while crafting new opportunities. This documentation aims at presenting our group's journey and experience in developing a 2D platformer game, highlighting the significant challenges and hurdles we had to overcome. The project is developed using the Python-based Pygame library, which facilitates the process by providing a wide array of built-in methods and imports at our disposal.

Central to our project's identity is its server-client logic, a component that proved to be both challenging and crucial for the successful outcome of our project. This intricate architecture serves as the backbone of our game, enabling multiple players to interact within a shared digital universe seamlessly. The implementation of this feature required a deep understanding of network programming and synchronization principles. As we navigated the complexities of ensuring fluid gameplay over networked environments, we realized that this was not just about coding efficiency but about creating a harmonious interconnected experience for the players.

Beyond the technicalities of networked play, our game introduces novel elements in player movement and collision mechanics. These are not mere programming features; they are the embodiment of our vision to elevate the gaming experience. By engineering unique movement dynamics and collision responses, we crafted a gameplay environment which is both challenging and engaging. These elements compel players to think strategically, making every jump and every interaction a deliberate and meaningful decision.

One of the most distinctive features of our game is the rope logic, integrated with robust physics coding. This aspect of the game opens up a plethora of gameplay possibilities. The rope becomes an extension of the player's will, a tool that is as versatile as it is fun.

In this documentation, we will delve deeper into the intricacies of our project, shedding light on the various components that build up our game and make it unique. The journey has been as much about overcoming technical hurdles as it has been about crafting an experience that resonates with players.

## Server-Client Logic for Multiplayer Implementation

Rope Runner's core engine is written in Python, totaling around 2000 lines. The code's server architecture is designed to manage multiple client connections, player interactions, game state updates, and real-time communication. Key components include the `Server` class and the `ClientHandler` class, which handle various game object classes such as Player, Rope, Lava, and more. 

The `Server` class forms the core of the application, initializing a TCP socket server to manage incoming connections and maintaining a list of `ClientHandler` instances, each dedicated to a specific client. It's responsible for managing game elements like players, platforms, lava blocks, and flags, along with broadcasting game updates and synchronizing the game state across all clients.

On the other hand, the `ClientHandler` class focuses on individual client management, ensuring player readiness, and handling the game loop for state updates and client disconnections.

Gameplay dynamics are enriched through various interactive objects and real-time updates based on client inputs, like movement and jumping. This architecture guarantees a synchronized, real-time gaming experience, making it ideal for fast-paced, multiplayer games requiring consistent state management across different clients.

The `GameLogicScreen` class in this Python script is a key component for a Pygame-based multiplayer game, handling visual rendering and game state updates. It initializes game elements like players, a rope, and lava blocks, and manages screen settings. The class processes player inputs (directional keys), updating the list of pressed keys or defaulting to 'idle'. It receives and integrates data updates, including player positions, game status, and game objects like the rope and flag. The `render` method dynamically displays these elements, adjusting their positions based on the camera's view, centered between players. The rope is rendered with a realistic Bezier curve for elasticity, and a "GAME OVER" message is displayed with a fade-in effect when the game ends. This class ensures a responsive and visually engaging gaming experience.

<br>

## Issues Encountered
Throughout the journey of our group project, we navigated through various complexities underscored by a demanding learning curve. A critical juncture was our decision to entirely revamp the server script. This strategic move was essential to decrease the lag between two machines running the client script, while simultaneously cultivating a codebase which exemplified modularity and efficiency. This improvement was vital, bearing in mind that other peers might scrutinize our code at a later stage, necessitating clarity and optimization.

## Challenge
A primary concern in our project was the architecture of server and client logic, particularly the server class which underwent multiple revisions. This posed a significant challenge for our team.

## Initial Approach
Initially, our server client model was structured such that all objects were passed and created within the client class, resulting in inefficiency and diminished game performance.

## Revised Approach
To address this, we later transferred all object passing, collision detection, and movement functionalities to the server class. This modification significantly reduced latency, enhanced performance, and simplified the creation of new Objects.

However, this approach led to an unwieldy client class, inflating to almost 600 lines, primarily due to rendering requirements.

## Solution
Consequently, we opted to restructure the server and client classes in order to enhance modularity, creating separate classes for rendering and thus alleviating the complexity of the client codebase. This restructuring improved code readability and facilitated future peer review and code augmentation.
