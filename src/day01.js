import Bun from "bun";

const input_file = process.argv[2];

const input = await Bun.file(input_file).text();
console.log(`Input: ${input}`);

async function partOne(input) {
  const MAX_POS = 100;
  const TARGET_POS = 0;

  let pos = 50;
  let target_pos_count = 0;

  for (const line of input.split("\n")) {
    const turn = line[0];
    const dist = parseInt(line.slice(1), 10);

    if (turn === "L") {
      pos = (MAX_POS + pos - dist) % MAX_POS;
    } else if (turn === "R") {
      pos = (pos + dist) % MAX_POS;
    }

    if (pos === TARGET_POS) {
      target_pos_count += 1;
    }
  }

  console.log(`Times at target position (${TARGET_POS}): ${target_pos_count}`);
  return target_pos_count;
}

async function partTwo(input) {
  const MAX_POS = 100;
  const TARGET_POS = 0;

  let pos = 50;
  let target_pos_count = 0;

  for (const line of input.split("\n")) {
    const turn = line[0];
    let dist = parseInt(line.slice(1), 10);

    if (dist >= 100) {
      const full_turns = Math.floor(dist / 100);
      target_pos_count += full_turns;
      console.log(`[${line}]: ${target_pos_count} (full turn)`);
      dist = dist % 100;
    }

    if (turn === "L") {
      if (pos - dist < 0 && pos != 0) {
        target_pos_count += 1;
        console.log(`[${line}]: ${target_pos_count}`);
      }
      pos = (MAX_POS + pos - dist) % MAX_POS;
    } else if (turn === "R") {
      if (pos + dist > MAX_POS) {
        target_pos_count += 1;
        console.log(`[${line}]: ${target_pos_count}`);
      }

      pos = (pos + dist) % MAX_POS;
    }

    if (pos === TARGET_POS) {
      target_pos_count += 1;
      console.log(`[${line}]: ${target_pos_count}`);
    }
  }

  console.log(
    `Times passed by target position (${TARGET_POS}): ${target_pos_count}`,
  );
  return target_pos_count;
}

await partOne(input);
await partTwo(input);
