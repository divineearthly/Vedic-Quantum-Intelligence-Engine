#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
#include <climits> // For LLONG_MAX

// Mathematical Description of Urdhva Tiryagbhyam (Vertically and Crosswise):
// This sutra provides a general method for multiplying any two numbers, regardless of their size.
// The core idea is to compute the digits of the product from right to left by summing diagonal products of digits from the two numbers.
// This method naturally handles carries at each step.
//
// Example: Multiply 12 by 34
// Represent numbers as digits: num1 = {1, 2}, num2 = {3, 4}
//
// Step 1 (Units Place): Multiply vertically the rightmost digits.
//   2 * 4 = 8. Write down 8. Carry = 0.
//
// Step 2 (Tens Place): Multiply crosswise and add any carry.
//   (1 * 4) + (2 * 3) + Carry (0) = 4 + 6 = 10. Write down 0. Carry = 1.
//
// Step 3 (Hundreds Place): Multiply vertically the leftmost digits and add any carry.
//   (1 * 3) + Carry (1) = 3 + 1 = 4. Write down 4.
//
// Result: 408.
//
// For larger numbers, the pattern extends, involving sums of more diagonal products for each position.

// Formal Algorithm for Urdhva Tiryagbhyam:
// Input: Two positive integers, num1 and num2.
// Output: Their product.
//
// 1. Convert num1 and num2 into vectors of their digits, stored in reverse order (least significant digit first).
//    e.g., 123 -> {3, 2, 1}
// 2. Determine the maximum possible length of the product, which is `len(digits1) + len(digits2)`.
// 3. Initialize a result_digits vector of this maximum length with zeros.
// 4. Initialize `carry = 0`.
// 5. Iterate from `k = 0` to `len(digits1) + len(digits2) - 2` (representing each column position of the product, from right to left).
//    a. For each `k`, initialize `column_sum = carry`.
//    b. Iterate through the digits of `digits1` at index `i`.
//       i. Calculate the corresponding index `j = k - i` for `digits2`.
//       ii. If `j` is a valid index for `digits2`, add `digits1[i] * digits2[j]` to `column_sum`.
//    c. Set `result_digits[k] = column_sum % 10`.
//    d. Update `carry = column_sum / 10`.
// 6. After the loop, if `carry > 0`, add it to the last relevant position in `result_digits`.
// 7. Remove any leading zeros from `result_digits`.
// 8. Convert the `result_digits` (which is in reverse order) back into a `long long` integer.
// 9. Include overflow checks during the conversion back to `long long`.

// Helper function to convert an integer to a vector of its digits (in reverse order)
std::vector<int> to_digits(long long n) {
    std::vector<int> digits;
    if (n == 0) {
        digits.push_back(0);
        return digits;
    }
    while (n > 0) {
        digits.push_back(n % 10);
        n /= 10;
    }
    return digits;
}

// Urdhva Tiryagbhyam (Vertically and Crosswise) multiplication function
long long urdhva_tiryagbhyam_multiply(long long num1, long long num2) {
    if (num1 == 0 || num2 == 0) return 0;
    if (num1 < 0 || num2 < 0) {
        std::cerr << "Error: Urdhva Tiryagbhyam as implemented here is for positive integers. Received: " << num1 << ", " << num2 << std::endl;
        return -1; // Indicate error for negative inputs
    }

    std::vector<int> d1 = to_digits(num1); // e.g., 123 -> {3, 2, 1}
    std::vector<int> d2 = to_digits(num2); // e.g., 45 -> {5, 4}

    int len1 = d1.size();
    int len2 = d2.size();

    // The maximum possible length of the product is len1 + len2
    std::vector<int> result_digits(len1 + len2, 0);
    int carry = 0;

    // Iterate through each 'column' position of the result, from right to left
    // The number of columns will be (len1 + len2 - 1)
    for (int k = 0; k < len1 + len2 - 1; ++k) {
        int column_sum = carry;
        // Sum products of digits d1[i] * d2[j] where i+j = k
        for (int i = 0; i < len1; ++i) {
            int j = k - i; // Calculate corresponding index for d2

            // Ensure j is within bounds for d2
            if (j >= 0 && j < len2) {
                column_sum += d1[i] * d2[j];
            }
        }
        result_digits[k] = column_sum % 10;
        carry = column_sum / 10;
    }

    // Handle any final carry
    if (carry > 0) {
        // If there's a final carry, it means the product is longer than len1+len2-1
        // The result_digits vector was initialized to len1+len2, so the last element is result_digits[len1 + len2 - 1]
        result_digits[len1 + len2 - 1] += carry;
    }

    // Remove leading zeros from the result (if any, like 00123 -> 123)
    int actual_len = result_digits.size();
    while (actual_len > 1 && result_digits[actual_len - 1] == 0) {
        actual_len--;
    }
    result_digits.resize(actual_len);

    // Convert the vector of digits (which are in reverse order) back to a long long
    long long final_result = 0;
    long long power_of_10 = 1;

    for (size_t i = 0; i < result_digits.size(); ++i) {
        // Check for potential overflow before adding next digit
        // This check guards against final_result exceeding LLONG_MAX.
        // It's an approximate check; for true arbitrary precision, a BigInt library is needed.
        if (result_digits[i] != 0 && power_of_10 > LLONG_MAX / result_digits[i]) {
             std::cerr << "Warning: Urdhva Tiryagbhyam intermediate product exceeds 'long long' capacity." << std::endl;
             return -2; // Indicate overflow
        }
        // Check for overflow on final sum
        if (final_result > LLONG_MAX - (long long)result_digits[i] * power_of_10) {
            std::cerr << "Warning: Urdhva Tiryagbhyam final result exceeds 'long long' capacity." << std::endl;
            return -2; // Indicate overflow
        }

        final_result += (long long)result_digits[i] * power_of_10;

        // Check for power_of_10 overflow before next iteration
        if (i < result_digits.size() - 1 && power_of_10 > LLONG_MAX / 10) {
            std::cerr << "Warning: Power of 10 exceeds 'long long' capacity during reconstruction." << std::endl;
            return -2; // Indicate error due to exceeding capacity
        }
        power_of_10 *= 10;
    }
    return final_result;
}
