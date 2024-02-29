class Grid:
    def __init__(self, map_width, map_height, cell_size):
        self.cell_size = cell_size
        self.cols = int(map_width / cell_size)
        self.rows = int(map_height / cell_size)
        self.cells = {}

    def add_platform(self, platform):
        # 1. Calculate grid cell indices for the platform's top-left corner
        start_col = int(platform.x / self.cell_size)
        start_row = int(platform.y / self.cell_size)

        # 2. Calculate which cells the platform potentially overlaps
        end_col = int((platform.x + platform.width - 1) / self.cell_size)  # Note: -1 for right edge
        end_row = int((platform.y + platform.height - 1) / self.cell_size)  # Note: -1 for bottom edge

        # 3. Iterate over the cells and add the platform
        for row in range(start_row, end_row + 1):
            for col in range(start_col, end_col + 1):
                cell_key = (col, row)
                if cell_key not in self.cells:
                    self.cells[cell_key] = []  # Create an empty list for this cell if it doesn't exist
                self.cells[cell_key].append(platform)

    def get_platforms_near(self, x, y):
        col = int(x / self.cell_size)
        row = int(y / self.cell_size)
        platforms = []

        # Get platforms from the player's cell and neighboring cells
        for i in range(col - 1, col + 3):  # Check one cell in each direction
            for j in range(row - 1, row + 3):
                cell_key = (i, j)
                if cell_key in self.cells:
                    platforms += self.cells[cell_key]

        return platforms
