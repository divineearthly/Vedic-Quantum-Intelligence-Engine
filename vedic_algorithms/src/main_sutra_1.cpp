#include <iostream>
#include <string>
#include <algorithm>
#include <vector>
#include <cmath>

long long subtract_from_power_of_10(long long power_of_10, long long subtrahend) {
    if (power_of_10 <= subtrahend || power_of_10 % 10 != 0) {
        std::cerr << "Error: Sutra applicable only for subtracting from powers of 10." << std::endl;
        return -1;
    }
    std::string s_subtrahend = std::to_string(subtrahend);
    std::string s_power_of_10 = std::to_string(power_of_10);
    int num_zeros = s_power_of_10.length() - 1;
    int subtrahend_len = s_subtrahend.length();
    if (subtrahend_len > num_zeros) return -1;
    std::string padded_subtrahend = std::string(num_zeros - subtrahend_len, '0') + s_subtrahend;
    std::string result_str = "";
    for (int i = 0; i < (int)padded_subtrahend.length(); ++i) {
        int digit = padded_subtrahend[i] - '0';
        if (i == (int)padded_subtrahend.length() - 1) {
            result_str += std::to_string(10 - digit);
        } else {
            result_str += std::to_string(9 - digit);
        }
    }
    return std::stoll(result_str);
}
