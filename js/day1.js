import "process";
import fs from 'fs'

let data = fs.readFileSync(process.argv[2], "utf8")
console.log(data)
