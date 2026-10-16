#include "GameFile.h"

#include <algorithm>
#include <fstream>
#include <utility>

namespace {
std::string trimField(const std::string& field) {
    const std::size_t first = field.find_first_not_of(' ');
    if (first == std::string::npos) {
        return "";
    }

    const std::size_t last = field.find_last_not_of(' ');
    return field.substr(first, last - first + 1);
}

bool parseNumber(const std::string& text, double& value) {
    try {
        std::size_t parsedCharacters = 0;
        value = std::stod(text, &parsedCharacters);
        return parsedCharacters == text.size();
    } catch (...) {
        return false;
    }
}
}

bool GameFile::load(std::string path) {
    std::ifstream input(path);
    if (!input) {
        return false;
    }

    std::vector<Game> loadedGames;
    std::string line;
    bool foundEnd = false;

    while (std::getline(input, line)) {
        if (trimField(line.substr(0, 25)) == "END") {
            foundEnd = true;
            break;
        }

        if (line.size() < 48) {
            return false;
        }

        const std::string name = trimField(line.substr(0, 25));
        const std::string seller = trimField(line.substr(26, 15));
        const std::string priceText = trimField(line.substr(42, 6));

        double price = 0.0;
        if (name.empty() || seller.empty() || !parseNumber(priceText, price)) {
            return false;
        }

        loadedGames.emplace_back(name, seller, price);
    }

    if (!foundEnd) {
        return false;
    }

    available = std::move(loadedGames);
    pendingListings.clear();
    return true;
}

Game* GameFile::findAvailable(std::string name) {
    for (Game& game : available) {
        if (game.getName() == name) {
            return &game;
        }
    }

    return nullptr;
}

bool GameFile::nameInUse(std::string name) {
    if (findAvailable(name) != nullptr) {
        return true;
    }

    for (Game& game : pendingListings) {
        if (game.getName() == name) {
            return true;
        }
    }

    return false;
}

void GameFile::addPending(Game game) {
    pendingListings.push_back(game);
}

void GameFile::commitPending() {
    available.insert(available.end(), pendingListings.begin(), pendingListings.end());
    pendingListings.clear();
}

void GameFile::removeBySeller(std::string seller) {
    const auto belongsToSeller = [&seller](Game& game) {
        return game.getSeller() == seller;
    };

    available.erase(
        std::remove_if(available.begin(), available.end(), belongsToSeller),
        available.end());
    pendingListings.erase(
        std::remove_if(pendingListings.begin(), pendingListings.end(), belongsToSeller),
        pendingListings.end());
}

std::vector<Game> GameFile::getAvailable() {
    return available;
}
