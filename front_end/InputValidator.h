#pragma once

#include <string>

class InputValidator {
public:
    static bool isValidUsername(std::string name);
    static bool isValidUserType(std::string type);
    static bool isValidGameName(std::string name);
    static bool isValidPrice(double price);
    static bool isValidCreditAmount(double amount);
    static bool parseNumber(std::string text, double& out);
};
