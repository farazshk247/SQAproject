#pragma once

#include <string>
#include <vector>

#include "Game.h"

class GameFile {
private:
    std::vector<Game> available;
    std::vector<Game> pendingListings;

public:
    bool load(std::string path);
    Game* findAvailable(std::string name);
    bool nameInUse(std::string name);
    void addPending(Game game);
    void commitPending();
    void removeBySeller(std::string seller);
    std::vector<Game> getAvailable();
};
