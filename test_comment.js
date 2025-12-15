import { makeParentingComment } from "./makeComment.js";

// Test Case 1: User's example (mixed/random)
// 0..4 scale
const answers = [
    3, 4, // Q1, Q2 (Domain I) -> 4, 5 -> High
    1, 0, // Q3, Q4 (Domain II) -> 2, 1 -> Low (SOS)
    2, 2, // Q5, Q6 (Domain III) -> 3, 3 -> Low (SOS <= 3.0)
    4, 4, // Q7, Q8 (Domain IV) -> 5, 5 -> High
    3, 3, // Q9, Q10 (Domain V) -> 4, 4 -> High
    1, 2, // Q11, Q12 (Domain VI) -> 2, 3 -> Low (SOS)
    3, 3, 3 // Q13, Q14, Q15 (Domain VII) -> 4, 4, 4 -> High
];

console.log("--- Test Case 1 ---");
const result = makeParentingComment(answers);
console.log(result.text);

// Test Case 2: All High (Perfect)
const perfect = Array(15).fill(4); // All 5s
console.log("\n--- Test Case 2 (Perfect) ---");
console.log(makeParentingComment(perfect).text);

// Test Case 3: All Low
const low = Array(15).fill(0); // All 1s
console.log("\n--- Test Case 3 (All Low) ---");
console.log(makeParentingComment(low).text);
