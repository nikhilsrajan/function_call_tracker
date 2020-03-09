#ifndef TRACKER_H
#define TRACKER_H

#include <string>
#include <fstream>
#include <mutex>
#include <vector>
#include <sstream>

std::mutex m;

class Logger {
public:
    Logger(std::string filename)
        : filename_(filename) {
        Log("---------- START NEW SESSION ----------");
    }

    ~Logger() {
        Log("------------- END SESSION -------------");
    }

    void Log(const std::string& msg) {
        m.lock();
        std::ofstream out(filename_, std::ofstream::out | std::ofstream::app);
        out << msg << std::endl;
        out.close();
        m.unlock();
    }

private:
    std::string filename_;
};

class Tracker {
public:
    Tracker(std::string function_name)
        : function_name_(function_name) {
        std::stringstream msg;
        msg << "START : " << function_name_;
        logger_.Log(msg.str());
    }

    ~Tracker() {
        std::stringstream msg;
        msg << "END   : " << function_name_;
        logger_.Log(msg.str());
    }

private:
    static Logger logger_;
    std::string function_name_;
    std::mutex m_;
};

#endif // TRACKER_H
