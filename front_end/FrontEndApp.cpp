#include "FrontEndApp.h"

#include "Transaction.h"

int FrontEndApp::start(int argc, char** argv) {
    if (argc != 5) {
        context.console.showError(
            "usage: frontend <accounts_file> <games_file> "
            "<collection_file> <daily_output_file>.");
        return 1;
    }

    if (!loadFiles(argv[1], argv[2], argv[3], argv[4])) {
        context.console.showError("unable to load the required files.");
        shutdown();
        return 1;
    }

    run();
    shutdown();
    return 0;
}

void FrontEndApp::run() {
    std::string command;
    while (context.console.readLine(command)) {
        if (command.empty()) {
            context.console.showError("empty input ignored.");
            continue;
        }

        Transaction* transaction = factory.createTransaction(command);
        if (transaction == nullptr) {
            context.console.showError(
                "'" + command + "' is not a recognized transaction code.");
            continue;
        }

        transaction->execute(context);
        delete transaction;
    }
}

bool FrontEndApp::loadFiles(
    std::string accountsPath, std::string gamesPath,
    std::string collectionPath, std::string dailyOutputPath) {
    if (!context.accounts.load(accountsPath)) {
        return false;
    }
    if (!context.games.load(gamesPath)) {
        return false;
    }
    if (!context.collection.load(collectionPath)) {
        return false;
    }

    return context.writer.open(dailyOutputPath);
}

void FrontEndApp::shutdown() {
    context.writer.close();
}
