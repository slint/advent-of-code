import Bun from "bun";

const input_file = process.argv[2];

const input = (await Bun.file(input_file).text()).trim();
console.log(`Input: ${input}`);

function partOne(input: string) {
  console.log("Part one");
  let grid: string[][] = [];
  let accessibleCells = 0;

  for (const row of input.trim().split("\n")) {
    grid.push(row.split(""));
  }

  // Make a copy of the grid
  const gridCopy = grid.map((row) => [...row]);

  console.log("Grid:");

  for (let y = 0; y < grid.length; y++) {
    for (let x = 0; x < grid[y].length; x++) {
      if (grid[y][x] !== "@") {
        continue;
      }

      let count = 0;
      for (let northSouth = -1; northSouth <= 1; northSouth++) {
        for (let westEast = -1; westEast <= 1; westEast++) {
          if (northSouth === 0 && westEast === 0) continue;
          const neighborY = y + northSouth;
          const neighborX = x + westEast;
          if (
            neighborY >= 0 &&
            neighborY < grid.length &&
            neighborX >= 0 &&
            neighborX < grid[neighborY].length &&
            grid[neighborY][neighborX] === "@"
          ) {
            count++;
          }
        }
      }
      if (count < 4) {
        accessibleCells++;
        gridCopy[y][x] = "x";
      }
    }
  }

  console.log(`Accessible cells: ${accessibleCells}`);
}

function partTwo(input: string) {
  return input;
}

partOne(input);
// partTwo(input);
