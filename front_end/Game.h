#pragma once

#include <string>

class Game {
private:
    std::string name;
    std::string sellerName;
    double price = 0.0;

public:
    Game(std::string name, std::string seller, double price);
    std::string getName();
    std::string getSeller();
    double getPrice();
};
