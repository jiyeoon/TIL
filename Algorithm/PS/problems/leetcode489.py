class Solution:
    def cleanRoom(self, robot):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        cleaned = set()
        def dfs(robot, x, y, direction):
            if (x, y) in cleaned:
                return
            robot.clean()
            cleaned.add((x, y))
            for i, (dx, dy) in enumerate(directions[direction:] + directions[:direction]):
                nx = x + dx
                ny = y + dy
                if robot.move():
                    dfs(robot, nx, ny, (direction + i) % 4)
                    robot.turnLeft()
                    robot.turnLeft()
                    robot.move()
                    robot.turnLeft()
                else:
                    robot.turnRight()
        
        dfs(robot, 0, 0, 0)
        

        