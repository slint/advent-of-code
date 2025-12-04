import Bun from "bun";

const input_file = process.argv[2];

const input = (await Bun.file(input_file).text()).trim();

function partOne(input: string) {
  console.log("Part one");
  const allJoltages: number[] = [];
  for (const bankStr of input.split("\n")) {
    const bankNums = Array.from(bankStr).map(Number);
    let leftMax = bankNums[0];
    let leftMaxIdx = 0;

    bankNums.slice(0, bankNums.length - 1).forEach((i, idx) => {
      if (i > leftMax) {
        leftMax = i;
        leftMaxIdx = idx;
      }
    });

    let rightMax = bankNums[leftMaxIdx + 1];
    let rightMaxIdx = leftMaxIdx + 1;
    bankNums.slice(rightMaxIdx + 1).forEach((num, idx) => {
      if (num > rightMax) {
        rightMax = num;
        rightMaxIdx = rightMaxIdx + 1 + idx;
      }
    });

    let joltage = Number(leftMax.toString() + rightMax.toString());
    allJoltages.push(joltage);
  }

  console.log(allJoltages);
  console.log(allJoltages.reduce((a, i) => a + i));
  console.log("");
}

function partTwo(input: string) {
  console.log("Part two");
  const allJoltages: number[] = [];
  for (const bankStr of input.split("\n")) {
    const bankNums = Array.from(bankStr).map(Number);
  }

  console.log(allJoltages);
  console.log(allJoltages.reduce((a, i) => a + i));
  console.log("");

  return input;
}

partOne(input);
partTwo(input);
