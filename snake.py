import random
import curses

def main(stdscr):
    # Initialize screen settings
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    # Get window dimensions
    sh, sw = stdscr.getmaxyx()

    # Create window
    w = curses.newwin(sh, sw, 0, 0)
    w.keypad(1)
    w.timeout(100)

    # Draw border
    w.border(0)

    # Initial position of the snake
    snk_y, snk_x = sh // 2, sw // 4
    snake = [
        [snk_y, snk_x],
        [snk_y, snk_x - 1],
        [snk_y, snk_x - 2]
    ]

    # Initial food position
    food = [sh // 2, sw // 2]
    w.addch(food[0], food[1], '*')

    # Initial snake direction
    key = curses.KEY_RIGHT

    score = 0
    valid_keys = [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]

    while True:
        # Show score
        w.addstr(0, 2, f' Score: {score} ')

        next_key = w.getch()

        # Handle key press
        if next_key in valid_keys:
            # Prevent moving in the opposite direction
            if key == curses.KEY_UP and next_key != curses.KEY_DOWN:
                key = next_key
            elif key == curses.KEY_DOWN and next_key != curses.KEY_UP:
                key = next_key
            elif key == curses.KEY_LEFT and next_key != curses.KEY_RIGHT:
                key = next_key
            elif key == curses.KEY_RIGHT and next_key != curses.KEY_LEFT:
                key = next_key

        # Calculate new head position
        new_head = [snake[0][0], snake[0][1]]

        if key == curses.KEY_DOWN:
            new_head[0] += 1
        elif key == curses.KEY_UP:
            new_head[0] -= 1
        elif key == curses.KEY_LEFT:
            new_head[1] -= 1
        elif key == curses.KEY_RIGHT:
            new_head[1] += 1

        # Check for collision with walls or self
        if (new_head[0] in [0, sh - 1] or
            new_head[1] in [0, sw - 1] or
            new_head in snake):
            # Game Over
            msg = f"Game Over! Final Score: {score}"
            w.addstr(sh // 2, (sw - len(msg)) // 2, msg)
            w.refresh()
            curses.napms(3000)
            break

        # Move snake
        snake.insert(0, new_head)

        # Check if snake eats food
        if snake[0] == food:
            score += 1
            food = None
            while food is None:
                # Generate new food coordinates
                nf = [
                    random.randint(1, sh - 2),
                    random.randint(1, sw - 2)
                ]
                # Ensure food doesn't spawn on the snake
                food = nf if nf not in snake else None
            w.addch(food[0], food[1], '*')
        else:
            # Remove tail if no food eaten
            tail = snake.pop()
            w.addch(tail[0], tail[1], ' ')

        # Draw new head
        w.addch(snake[0][0], snake[0][1], '#')

if __name__ == "__main__":
    curses.wrapper(main)
