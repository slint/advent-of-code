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

    const joltage = Number(leftMax.toString() + rightMax.toString());
    allJoltages.push(joltage);
  }

  const joltageSum = allJoltages.reduce((a, i) => a + i);
  console.log(`Total joltage sum: ${joltageSum}`);
}

function partTwo(input: string) {
  console.log("Part two");
  const allJoltages: number[] = [];
  for (const bankStr of input.split("\n")) {
    const bankNums = Array.from(bankStr).map(Number);
    const joltageDigits: string[] = [];
    let idx: number = 0;

    while (joltageDigits.length < 12 && idx < bankNums.length) {
      const bankSlice = bankNums
        .slice(idx, bankNums.length - (11 - joltageDigits.length))
        .sort((a, b) => b - a);
      joltageDigits.push(bankSlice[0].toString());
      idx = bankNums.indexOf(bankSlice[0], idx) + 1;
    }

    allJoltages.push(Number(joltageDigits.join("")));
  }

  const joltageSum = allJoltages.reduce((a, i) => a + i);
  console.log(`Total joltage sum (out of 12): ${joltageSum}`);
}

partOne(input);
partTwo(input);
