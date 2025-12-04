import Bun from "bun";
import { debug } from "node:util";

const input_file = process.argv[2];

const input = await Bun.file(input_file).text();
console.log(`Input: ${input}`);

function partOne(input: string) {
  let invalidIds: number[] = [];

  for (const pair of input.split(",")) {
    const [start, end] = pair.split("-").map(Number);
    let currentId = start;
    while (currentId <= end) {
      let currentIdStr = currentId.toString();
      const firstHalf = currentIdStr.slice(0, currentIdStr.length / 2);
      const lastHalf = currentIdStr.slice(currentIdStr.length / 2);

      if (firstHalf === lastHalf) {
        invalidIds.push(currentId);
      }

      currentId++;
    }
  }

  const invalidSum = invalidIds.reduce((a, i) => a + i);
  console.log(invalidSum);
}

function divisors(num: number): number[] {
  var result: number[] = [];
  for (let i = 0; i < num; i++) {
    if (i !== num && num % i == 0) {
      result.push(i);
    }
  }
  return result;
}

function partTwo(input: string) {
  let invalidIds: number[] = [];

  for (const pair of input.trim().split(",")) {
    const [start, end] = pair.split("-").map(Number);
    let currentId = start;
    while (currentId <= end) {
      let currentIdStr = currentId.toString();
      for (let size of divisors(currentIdStr.length).reverse()) {
        const chunkCount = Math.floor(currentIdStr.length / size);
        const chunks = [...Array(chunkCount).keys()].map((chunkIdx) => {
          const chunkStart = chunkIdx * size;
          const chunkEnd = (chunkIdx + 1) * size;
          const chunk = currentIdStr.slice(chunkStart, chunkEnd);
          return chunk;
        });

        if (chunks.every((val) => val === chunks[0])) {
          invalidIds.push(currentId);
          break;
        }
      }

      currentId++;
    }
  }

  const invalidSum = invalidIds.reduce((a, i) => a + i);
  console.log(invalidSum);
}

partOne(input);
partTwo(input);
