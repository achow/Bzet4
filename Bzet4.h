#ifndef BZET4_H_ 
#define BZET4_H_

#include <stdio.h>
#include <stdlib.h>

#define INITIAL_ALLOC 1024
#define BZET Bzet4

typedef long long int64_t;

enum OP { 
    OP_0000, OP_0001, OP_0010, OP_0011, OP_0100, OP_0101, OP_0110, OP_0111,
    OP_1000, OP_1001, OP_1010, OP_1011, OP_1100, OP_1101, OP_1110, OP_1111,
    AND = 1, XOR = 6, OR = 7, NOR = 8, NOT = 10, NAND = 14 };
enum ACTION { DA0, DA1, DB0, DB1, CA, CB, NA, NB };
enum NODETYPE { SATURATED, EMPTY, NORMAL };

class Bzet4 {
    public:
        Bzet4();
        Bzet4(const Bzet4& src);
        Bzet4(int64_t bit);
        Bzet4(int64_t startbit, int64_t len);
        //Bzet4(const char* filename);
        Bzet4(void* data, int size);
        ~Bzet4();

        Bzet4& operator=(const Bzet4& right);
        Bzet4 operator~() const;
        Bzet4 operator|(const Bzet4& right) const;
		Bzet4 operator&(const Bzet4& right) const;
		Bzet4 operator^(const Bzet4& right) const;
		bool operator==(const Bzet4& right) const;

        static Bzet4 binop(Bzet4& left, Bzet4& right, OP op);

        bool at(int64_t bit) const;
        void setRange(int64_t start, int64_t len);
        void set(int64_t bit);
        void unset(int64_t bit);

        int depth() const;
        size_t size() const;

        static void align(Bzet4& b1, Bzet4& b2);
        void normalize();

        void clear();

        void hex(void* str) const;
        void printBzet(int stdOffset = 0, FILE* target = stdout) const;

		int64_t firstBit() const;
        int64_t lastBit() const;
        int64_t count() const;
        int64_t getBits(int64_t* bits, int64_t limit = 0, int64_t start = 0);
		bool empty() const;

#if (defined _DEBUG || defined DEBUG)
        void printBytes(FILE* target = stdout) const;
        void validateBzet(size_t loc = 1, int lev = 0);
        void dump() const;
#endif

    private:
        void display_error(char* message, bool fatal = false, FILE* output = stderr) const;
        static size_t pow4(int x);
        static int buildDepth(int64_t size);
        static unsigned char dust(unsigned char x);
        int depthAt(size_t loc) const;
        size_t stepThrough(size_t loc) const;
        void subtreeNot(size_t loc, int depth = 0);
        void _printBzet(int stdOffset = 0, FILE* target = stdout, size_t loc = 1, int depth = 0, int offset = 0, bool pad = 0) const;
        void resize(size_t size);
        void loadBzet(void* bzet_literal, int size);

        NODETYPE _binop(const Bzet4& left, const Bzet4& right, OP op, int lev, size_t left_loc = 1, size_t right_loc = 1, size_t loc = 1);
        void appendSubtree(const Bzet4& src, size_t loc);
        static int do_data_op(OP op, int left_data_bit, int right_data_bit);
        void dropNodes(size_t loc, int n);

        void init();

        static const int powersof4[];
        static const ACTION optable[];

        size_t m_bufsize;
        size_t m_size; //actual size of m_bzet in bytes
        unsigned char* m_bzet; //points to the bzet
        unsigned char* m_step; //points to an array that holds stepThrough values
};

inline
void Bzet4::display_error(char* message, bool fatal, FILE* output) const {
    fprintf(output, "%s\n", message);
#if (defined _DEBUG || defined DEBUG)
    dump();
#endif
    if (fatal)
        exit(1);
}

/*****************************************************************************
 * 
 *  Function name: init
 *
 *  Purpose:       Common initialization upon object instantiation
 *
 *  Inputs:        None
 *  Return values: None
 * 
 *  Author:        Alex Chow
 *  Date:          12/14/2011
 *
 *****************************************************************************/
inline 
void Bzet4::init() {
    m_bzet = (unsigned char*) malloc(INITIAL_ALLOC * sizeof(unsigned char));
    m_step = (unsigned char*) malloc(INITIAL_ALLOC * sizeof(unsigned char));
    if (!m_bzet || !m_step) {
        fprintf(stderr, "Fatal error: Initial alloc failed attempting to allocate %d bytes\n", INITIAL_ALLOC);
        display_error("", true);
    }

    m_size = 0;
    m_bufsize = INITIAL_ALLOC;
}

#if (defined _DEBUG || defined DEBUG)
inline
void Bzet4::printBytes(FILE* target) const {
    for (int i = 0; i < m_size; ++i) {
        if (i % 10 == 0)
            printf("\n");
        fprintf(target, " 0x%.2X", m_bzet[i]); 
    } 
    fprintf(target, "\n");
}
#endif

#endif
