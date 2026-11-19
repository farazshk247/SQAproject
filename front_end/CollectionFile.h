#pragma once

#include <string>
#include <vector>

#include "CollectionEntry.h"

class CollectionFile {
private:
    std::vector<CollectionEntry> entries;

public:
    bool load(std::string path);
    bool ownsGame(std::string owner, std::string game);
    void addEntry(std::string owner, std::string game);
};
