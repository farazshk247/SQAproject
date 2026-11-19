#include "CollectionFile.h"

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
}

bool CollectionFile::load(std::string path) {
    std::ifstream input(path);
    if (!input) {
        return false;
    }

    std::vector<CollectionEntry> loadedEntries;
    std::string line;
    bool foundEnd = false;

    while (std::getline(input, line)) {
        if (trimField(line.substr(0, 25)) == "END") {
            foundEnd = true;
            break;
        }

        if (line.size() < 41) {
            return false;
        }

        const std::string game = trimField(line.substr(0, 25));
        const std::string owner = trimField(line.substr(26, 15));
        if (game.empty() || owner.empty()) {
            return false;
        }

        loadedEntries.emplace_back(owner, game);
    }

    if (!foundEnd) {
        return false;
    }

    entries = std::move(loadedEntries);
    return true;
}

bool CollectionFile::ownsGame(std::string owner, std::string game) {
    for (CollectionEntry& entry : entries) {
        if (entry.getOwner() == owner && entry.getGameName() == game) {
            return true;
        }
    }

    return false;
}

void CollectionFile::addEntry(std::string owner, std::string game) {
    entries.emplace_back(owner, game);
}
