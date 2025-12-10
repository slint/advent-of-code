import Bun from "bun";

const input_file = process.argv[2];

const input = (await Bun.file(input_file).text()).trim();

function partOne(input: string) {
  let grid: string[][] = [];
  for (const row of input.trim().split("\n")) {
    grid.push(row.split(""));
  }

  const accessibleCells = getAccessibleCells(grid);
  console.log(`[Part one] Accessible cells: ${accessibleCells.length}`);
}

function getAccessibleCells(grid: string[][]): Array<[number, number]> {
  const ret: Array<[number, number]> = [];
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
        ret.push([y, x]);
      }
    }
  }

  return ret;
}

function partTwo(input: string) {
  let grid: string[][] = [];
  for (const row of input.trim().split("\n")) {
    grid.push(row.split(""));
  }

  let accessibleCellsCount = 0;
  let accessibleCells: Array<[number, number]> = [];

  do {
    accessibleCells = getAccessibleCells(grid);
    // add to count
    accessibleCellsCount += accessibleCells.length;

    // mark collected cells
    for (const [y, x] of accessibleCells) {
      grid[y][x] = ".";
    }
  } while (accessibleCells.length > 0);

  console.log(`[Part two] Accessible cells: ${accessibleCellsCount}`);
}

partOne(input);
partTwo(input);
