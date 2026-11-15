#include <map>
#include <string>
#include <../books/literary.h>

class Author{
    std::string name;
    int birthYear;
    std::map<Literary, int> writings; // proizvedenia na eng
    public:
        Author searchByName(std::string);
        Author searchByWriting(Literary);
        Author searchByBirthYear(int);

};