#pragma once
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <chrono>
#include <ratio>
#include <ctime>

typedef uint8_t u8;
typedef int32_t i32;
typedef int32_t u64;
typedef std::ratio<1, 1000000> us;
typedef std::chrono::duration<u64, us> usDuration;
typedef std::chrono::high_resolution_clock::time_point time_point;
#define to_us_duration(x) std::chrono::duration_cast<usDuration>(x).count()
#define now() std::chrono::high_resolution_clock::now()