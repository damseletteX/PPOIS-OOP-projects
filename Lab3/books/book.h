#include <string>

class Book{
    std::string title;
    int pageAmount;
    Author author;
    public:
        bool findByAuthor(Author);
};