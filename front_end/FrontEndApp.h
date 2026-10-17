#pragma once

#include <string>

#include "FrontEndContext.h"
#include "TransactionFactory.h"

class FrontEndApp {
private:
    FrontEndContext context;
    TransactionFactory factory;

    bool loadFiles(
        std::string accountsPath, std::string gamesPath,
        std::string collectionPath, std::string dailyOutputPath);
    void shutdown();

public:
    int start(int argc, char** argv);
    void run();
};
