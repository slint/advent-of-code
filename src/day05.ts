import Bun from "bun";

const input_file = process.argv[2];
const input = (await Bun.file(input_file).text()).trim();

function parseInput(input: string) {
  const [rangesSection, ingredientsSection] = input.split("\n\n");

  const ranges: Array<[number, number]> = rangesSection
    .split("\n")
    .map((line) => line.split("-").map(Number));
  const ingredients: Array<number> = ingredientsSection.split("\n").map(Number);
  return { ingredients, ranges };
}

function partOne(input: string) {
  const { ingredients, ranges } = parseInput(input);

  const freshIngredients = ingredients.filter((ingredient) => {
    return ranges.some(
      ([start, end]) => ingredient >= start && ingredient <= end,
    );
  });

  console.log(`Part one: ${freshIngredients.length}`);
}

function mergeRanges(ranges: [number, number][]) {
  return ranges.reduce(
    (mergedRanges, [start, end]) => {
      if (mergedRanges.length == 0) {
        mergedRanges.push([start, end]);
        return mergedRanges;
      }

      // Check all previous ranges for overlap
      let newStart = start;
      let newEnd = end;
      const indicesToRemove: number[] = [];

      for (let i = 0; i < mergedRanges.length; i++) {
        const [prevStart, prevEnd] = mergedRanges[i];
        // Check if ranges overlap (or are adjacent)
        if (newStart <= prevEnd + 1 && newEnd >= prevStart - 1) {
          newStart = Math.min(prevStart, newStart);
          newEnd = Math.max(prevEnd, newEnd);
          indicesToRemove.push(i);
        }
      }

      if (indicesToRemove.length === 0) {
        mergedRanges.push([newStart, newEnd]);
      } else {
        // Remove overlapping ranges, starting from the end though
        for (let i = indicesToRemove.length - 1; i >= 0; i--) {
          mergedRanges.splice(indicesToRemove[i], 1);
        }
        mergedRanges.push([newStart, newEnd]);
      }

      return mergedRanges;
    },
    [] as Array<[number, number]>,
  );
}

function partTwo(input: string) {
  const { ranges } = parseInput(input);

  let oldRangesLength = ranges.length;
  let mergedRanges = mergeRanges(ranges);
  let newRangesLength = mergedRanges.length;

  while (oldRangesLength != newRangesLength) {
    oldRangesLength = newRangesLength;
    mergedRanges = mergeRanges(mergedRanges);
    newRangesLength = mergedRanges.length;
  }

  const totalRange = mergedRanges.reduce(
    (acc, [start, end]) => acc + (end - start) + 1,
    0,
  );

  console.log(`Part two: ${totalRange}`);
}

partOne(input);
partTwo(input);
