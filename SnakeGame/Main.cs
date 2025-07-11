Canvas.Write(0, 0, "Welcome to the snake game!");
while (true)
{
    Canvas.Write(0, 1, "Press [ENTER] to start...");
    ConsoleKeyInfo keyInfo;
    do
    {
        keyInfo = Console.ReadKey();
    } while (keyInfo.Key != ConsoleKey.Enter);
    Canvas.Clear();

    int score = Game();

    Canvas.Write(0, 0, $"GAME OVER! Score: {score}");
}

// Run the game and return the score when the game is over.
int Game()
{
    Snake snake = new();
    GameObject food = SpawnFood();

    while (true)
    {
        while (Console.KeyAvailable)
        {
            Direction d = Console.ReadKey().Key switch
            {
                ConsoleKey.LeftArrow => Direction.Left,
                ConsoleKey.UpArrow => Direction.Up,
                ConsoleKey.RightArrow => Direction.Right,
                ConsoleKey.DownArrow => Direction.Down,
                _ => snake.Direction
            };
            if (d != snake.Direction)
            {
                snake.Direction = d;
                break;
            }
        }
        (int x, int y) = snake.GetFrontPos();
        bool collided = snake.BodyParts.Any(part => part.X == x && part.Y == y)
                       || x < 0 || y < 0 || x >= Canvas.Width || y >= Canvas.Height;
        if (collided)
        {
            food.Dispose();
            snake.Dispose();
            return snake.BodyParts.Count - 3;
        }
        else if (x == food.X && y == food.Y)
        {
            snake.Eat(food);
            food = SpawnFood();
        }
        else
        {
            snake.Move();
        }
        Thread.Sleep(150);
    }

    // Spawn a food and return.
    GameObject SpawnFood()
    {
        int x, y;
        do
        {
            x = Random.Shared.Next(0, Canvas.Width);
            y = Random.Shared.Next(0, Canvas.Height);
        }
        while (snake.BodyParts.Any(p => x == p.X && y == p.Y));
        return new GameObject(x, y);
    }
}
