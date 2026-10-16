#include "InputValidator.h"

#include <cmath>

namespace {
std::string trim(const std::string& text) {
    const std::size_t first = text.find_first_not_of(" \t\r\n");
    if (first == std::string::npos) {
        return "";
    }

    const std::size_t last = text.find_last_not_of(" \t\r\n");
    return text.substr(first, last - first + 1);
}
}

bool InputValidator::isValidUsername(std::string name) {
    return !name.empty() && name.size() <= 15;
}

bool InputValidator::isValidUserType(std::string type) {
    return type == "AA" || type == "FS" || type == "BS" || type == "SS";
}

bool InputValidator::isValidGameName(std::string name) {
    return !name.empty() && name.size() <= 25;
}

bool InputValidator::isValidPrice(double price) {
    return std::isfinite(price) && price >= 0.0 && price <= 999.99;
}

bool InputValidator::isValidCreditAmount(double amount) {
    return std::isfinite(amount) && amount > 0.0 && amount <= 1000.0;
}

bool InputValidator::parseNumber(std::string text, double& out) {
    const std::string trimmedText = trim(text);
    if (trimmedText.empty()) {
        return false;
    }

    try {
        std::size_t parsedCharacters = 0;
        const double value = std::stod(trimmedText, &parsedCharacters);
        if (parsedCharacters != trimmedText.size() || !std::isfinite(value)) {
            return false;
        }

        out = value;
        return true;
    } catch (...) {
        return false;
    }
}
