import Bun from "bun";

const input_file = process.argv[2];

const input = (await Bun.file(input_file).text()).trim();
console.log(`Input:\n${input}`);

function partOne(input: string) {
  let grid: string[][] = [];
  for (const row of input.trim().split("\n")) {
    grid.push(row.split(""));
  }

  let beamSplitCount = 0;
  let beams: number[] = [grid[0].indexOf("S")];

  for (const row of grid) {
    const newBeams: number[] = [];

    for (const beam of beams) {
      const beamMaterial = row[beam];
      if (beamMaterial === "^") {
        // Split the beam
        beamSplitCount++;
        newBeams.push(beam - 1);
        newBeams.push(beam + 1);
      } else if (beamMaterial === "." || beamMaterial === "S") {
        newBeams.push(beam);
      }
    }

    // Remove duplicate beams
    beams = Array.from(new Set(newBeams));
  }

  console.log(`Part one: ${beamSplitCount}`);
}

function partTwo(input: string) {
  return input;
}

partOne(input);
// partTwo(input);
