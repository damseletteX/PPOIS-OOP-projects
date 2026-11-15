#include <string>

class Seller{
    std::string name;
    long double salary;
    int experience;
    public:
        Librarian() = default;
        ~Librarian();
        Book sell();
};