import Bun from "bun";

const input_file = process.argv[2];

const input = (await Bun.file(input_file).text()).trim();
console.log(`Input: ${input}`);

function partOne(input: string) {
  return input;
}

function partTwo(input: string) {
  return input;
}

partOne(input);
// partTwo(input);
