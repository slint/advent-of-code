import Bun from "bun";

const input_file = process.argv[2];

const input = await Bun.file(input_file).text();

function partOne(input: string) {
  const lines = input.trim().split("\n");
  const numbers = lines.slice(0, lines.length - 1).map((line) =>
    line
      .split(" ")
      .filter((value) => value !== "")
      .map(Number),
  );
  const operations = lines[lines.length - 1]
    .split(" ")
    .filter((operation) => operation !== "");

  let total = 0;

  for (let i = 0; i < numbers[0].length; i++) {
    if (operations[i] === "+") {
      let sum = 0;
      for (let j = 0; j < numbers.length; j++) {
        sum += numbers[j][i];
      }
      total += sum;
    } else if (operations[i] === "*") {
      let product = 1;
      for (let j = 0; j < numbers.length; j++) {
        product *= numbers[j][i];
      }
      total += product;
    }
  }

  console.log(`Part one: ${total}`);
}

function partTwo(input: string) {
  const lines = input.split("\n").filter((line) => line !== "");

  // Parse each column length, based on the operands
  const operationsLine = lines[lines.length - 1];
  const operations: string[] = [];
  const columnLengths: number[] = [];
  let currentColumn: string | null = null;
  for (let ch of operationsLine) {
    if (ch === "+" || ch === "*") {
      if (currentColumn === null) {
        // first iteration
        currentColumn = ch;
        operations.push(ch);
      } else {
        // new column
        columnLengths.push(currentColumn.length - 1);
        currentColumn = ch;
        operations.push(ch);
      }
    } else {
      currentColumn += ch;
    }
  }
  columnLengths.push(currentColumn!.length);

  const columnValues: number[][] = [];
  const numberLines = lines.slice(0, lines.length - 1);
  let colIdx = 0;
  for (const colSize of columnLengths) {
    const values = Array.from({ length: colSize }, () => 0);
    values.forEach((_, idx) => {
      let numString = "";
      for (let lineIdx = 0; lineIdx < numberLines.length; lineIdx++) {
        const digit = numberLines[lineIdx][colIdx + colSize - idx - 1];
        if (digit !== undefined) {
          numString += digit;
        }
      }
      values[idx] = Number(numString);
    });
    columnValues.push(values);
    colIdx += colSize + 1;
  }

  let total = 0;
  operations.forEach((operation, i) => {
    switch (operation) {
      case "+":
        total += columnValues[i].reduce((acc, val) => acc + val, 0);
        break;
      case "*":
        total += columnValues[i].reduce((acc, val) => acc * val, 1);
        break;
    }
  });

  console.log(`Part two: ${total}`);
}

partOne(input);
partTwo(input);
