#include "Bzet4.h"

#define DLLEXPORT extern "C" _declspec(dllexport)

DLLEXPORT Bzet4* Bzet4_newEmpty() {
    return new Bzet4();
}

DLLEXPORT Bzet4* Bzet4_new(int64_t bit) {
    return new Bzet4(bit);
}

DLLEXPORT Bzet4* Bzet4_newRange(int64_t startbit, int64_t len) {
    return new Bzet4(startbit, len);
}

DLLEXPORT void Bzet4_destroy(Bzet4* b) {
    delete b;
}

DLLEXPORT Bzet4* Bzet4_clone(Bzet4* b) {
    return new Bzet4(*b);
}

DLLEXPORT Bzet4* Bzet4_NOT(Bzet4* b) {
    return new Bzet4(~(*b));
}

DLLEXPORT void Bzet4_INVERT(Bzet4* b) {
    *b = ~(*b);
}

DLLEXPORT bool Bzet4_COMPARE(Bzet4* left, Bzet4* right) {
    return *left == *right;
}

DLLEXPORT Bzet4* Bzet4_AND(Bzet4* b, Bzet4* right) {
    return new Bzet4(*b & *right);
}

DLLEXPORT Bzet4* Bzet4_OR(Bzet4* b, Bzet4* right) {
    return new Bzet4(*b | *right);
}

DLLEXPORT Bzet4* Bzet4_XOR(Bzet4* b, Bzet4* right) {
    return new Bzet4(*b ^ *right);
}

DLLEXPORT void Bzet4_RANGE(Bzet4* b, int64_t start, int64_t len) {
    b->setRange(start, len);
}

DLLEXPORT void Bzet4_SET(Bzet4* b, int64_t bit) {
    b->set(bit);
}

DLLEXPORT void Bzet4_UNSET(Bzet4* b, int64_t bit) {
    b->unset(bit);
}

DLLEXPORT bool Bzet4_TEST(Bzet4* b, int64_t bit) {
    return b->at(bit);
}

DLLEXPORT void Bzet4_FLIP(Bzet4* b, int64_t bit) {
    if (b->at(bit))
        b->unset(bit);
    else
        b->set(bit);
}

DLLEXPORT int Bzet4_LEV(Bzet4* b) {
    return b->depth();
}

DLLEXPORT int64_t Bzet4_size(Bzet4* b) {
    return b->size();
}

DLLEXPORT void Bzet4_CLEAN(Bzet4* b) {
    b->clear();
}

DLLEXPORT void Bzet4_repr(Bzet4* b, void* target) {
    b->hex(target);
}

DLLEXPORT void Bzet4_HEX(Bzet4* b, int stdOffset) {
    b->printBzet(stdOffset);
}

DLLEXPORT int64_t Bzet4_FIRST(Bzet4* b) {
    return b->firstBit();
}

DLLEXPORT int64_t Bzet4_LAST(Bzet4* b) {
    return b->lastBit();
}

DLLEXPORT int64_t Bzet4_COUNT(Bzet4* b) {
    return b->count();
}

DLLEXPORT bool Bzet4_EMPTY(Bzet4* b) {
    return b->empty();
}