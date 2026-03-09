# Vedic Mathematical Algorithms

## 1. Urdhva Tiryagbhyam (Vertically and Crosswise)
**Application**: General Multiplication

### Mathematical Principle
This sutra allows for the multiplication of any two numbers by summing diagonal products of their digits. It naturally handles carries and is highly efficient for both small and large integers.

### Algorithmic Steps
1. Align the two numbers vertically.
2. Multiply the units digits vertically (Vertical).
3. Multiply the units of the first by the tens of the second and vice versa, then sum (Crosswise).
4. Continue the pattern for higher digits, expanding the crosswise sum.
5. Write down the result at each step, carrying over any tens to the next leftward position.

## 2. Paravartya Yojayet (Transpose and Apply)
**Application**: Specialized Division (Divisors near powers of 10)

### Mathematical Principle
Used when the divisor is slightly greater than a power of 10. It involves transposing the digits of the divisor (using negative numbers) and applying them to the dividend digits.

### Algorithmic Steps
1. Identify the base (power of 10) and the surplus (k).
2. Write the dividend digits and prepare a working buffer.
3. For each digit of the quotient, multiply it by the negative surplus (-k) and add it to the next digit of the dividend.
4. The final result yields the quotient and the remainder after adjusting for any negative values.

## 3. Nikhilam Navatashcaramam Dashatah (All from 9 and the Last from 10)
**Application**: Subtraction from Powers of 10

### Mathematical Principle
A specialized subtraction technique where every digit is subtracted from 9, except for the last non-zero digit, which is subtracted from 10.

### Algorithmic Steps
1. Identify the power of 10 and the subtrahend.
2. Pad the subtrahend with leading zeros to match the number of zeros in the power of 10.
3. Subtract each digit from 9 starting from the left.
4. Subtract the final units digit from 10.
5. Concatenate the results to find the final difference.
