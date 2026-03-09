#include <iostream>
#include <pybind11/pybind11.h>
#include <string>
#include "vedic_logic.h"

// Forward declarations for functions defined in other .cpp files, which are compiled separately.
// This is necessary because kernel.cpp exposes these functions via pybind11 but doesn't implement them directly.
long long urdhva_tiryagbhyam_multiply(long long num1, long long num2);
std::pair<long long, long long> paravartya_yojayet_divide_by_10_plus_k(long long dividend, int k);
long long subtract_from_power_of_10(long long power_of_10, long long subtrahend);

namespace py = pybind11;

// This is where functions will be exposed to Python. No main function is needed for a pybind11 module.
// The original kernel.cpp likely contained a main for standalone testing, which is removed here.

// Example function to be exposed
int add(int i, int j) {
    return i + j;
}

// pybind11 module definition
PYBIND11_MODULE(vedic_engine, m) {
    m.doc() = "pybind11 vedic_engine plugin"; // Optional module docstring

    m.def("add", &add, "A function that adds two numbers");

    // Expose vedic_logic functions
    m.def("load_rules", &loadRules, "Load rules from a JSON file");
    m.def("process_sutra", &processVedicSutra, "Process input data against loaded rules for a given sutra");

    // Expose Urdhva Tiryagbhyam multiplication
    m.def("urdhva_tiryagbhyam_multiply", &urdhva_tiryagbhyam_multiply,
          "Performs multiplication using Urdhva Tiryagbhyam (Vertically and Crosswise)");

    // Expose Paravartya Yojayet division
    m.def("paravartya_yojayet_divide", &paravartya_yojayet_divide_by_10_plus_k,
          "Performs division using Paravartya Yojayet (Transpose and Apply) for divisors like 10+k");

    // Expose Ekadhikena Purvena subtraction
    m.def("subtract_from_power_of_10", &subtract_from_power_of_10,
          "Performs subtraction from powers of 10 using Ekadhikena Purvena");

    // Bind the Rule struct for advanced usage if needed (optional for basic exposure)
    // py::class_<Rule>(m, "Rule")
    //     .def(py::init__())
    //     .def_readwrite("id", &Rule::id)
    //     .def_readwrite("name", &Rule::name)
    //     .def_readwrite("description", &Rule::description)
    //     .def_readwrite("priority", &Rule::priority);
}
