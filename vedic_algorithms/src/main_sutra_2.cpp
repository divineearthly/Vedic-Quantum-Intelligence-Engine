#include <iostream>
#include <string>
#include <vector>

std::pair<long long, long long> paravartya_yojayet_divide_by_10_plus_k(long long dividend, int k) {
    long long divisor = 10 + k;
    if (k <= 0 || k >= 10 || dividend < 0) return {-1, -1};
    if (dividend == 0) return {0, 0};
    std::string s_dividend = std::to_string(dividend);
    int dividend_len = s_dividend.length();
    std::vector<int> work_array(dividend_len + 1, 0);
    for (int i = 0; i < dividend_len; ++i) work_array[i] = s_dividend[i] - '0';
    std::vector<int> quotient_digits_buffer;
    for (int i = 0; i < dividend_len; ++i) {
        int current_quotient_digit = work_array[i];
        if (i < dividend_len - 1) {
            quotient_digits_buffer.push_back(current_quotient_digit);
            if (i + 1 < (int)work_array.size()) work_array[i + 1] += current_quotient_digit * (-k);
        }
    }
    long long final_quotient_ll = 0;
    long long power_of_10 = 1;
    for (int i = (int)quotient_digits_buffer.size() - 1; i >= 0; --i) {
        final_quotient_ll += quotient_digits_buffer[i] * power_of_10;
        power_of_10 *= 10;
    }
    long long final_remainder_ll = work_array[dividend_len - 1];
    while (final_remainder_ll < 0) { final_remainder_ll += divisor; final_quotient_ll--; }
    while (final_remainder_ll >= divisor) { final_remainder_ll -= divisor; final_quotient_ll++; }
    return {final_quotient_ll, final_remainder_ll};
}
