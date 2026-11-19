#pragma once

#include <string>

#include "FrontEndContext.h"

class Transaction {
protected:
    std::string code;

    bool requireLogin(FrontEndContext& ctx);
    bool requireAdmin(FrontEndContext& ctx);

public:
    virtual ~Transaction() = default;
    virtual bool execute(FrontEndContext& ctx) = 0;
    std::string getCode();
};
