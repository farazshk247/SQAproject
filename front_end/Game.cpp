#include "Game.h"

Game::Game(std::string name, std::string seller, double price)
    : name(name), sellerName(seller), price(price) {
}

std::string Game::getName() {
    return name;
}

std::string Game::getSeller() {
    return sellerName;
}

double Game::getPrice() {
    return price;
}
