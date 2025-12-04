import Bun from "bun";

const input_file = process.argv[2];

const input = await Bun.file(input_file).text();
console.log(`Input: ${input}`);

function partOne(input) {
  return input;
}

function partTwo(input) {
  return input;
}

partOne(input);
// partTwo(input);
