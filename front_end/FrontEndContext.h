#pragma once

#include "AccountFile.h"
#include "CollectionFile.h"
#include "Console.h"
#include "DailyTransactionWriter.h"
#include "GameFile.h"
#include "Session.h"

class FrontEndContext {
public:
    Session session;
    AccountFile accounts;
    GameFile games;
    CollectionFile collection;
    Console console;
    DailyTransactionWriter writer;
};
