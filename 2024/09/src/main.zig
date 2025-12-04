const std = @import("std");
const Timer = @import("timer.zig");
const Data = @import("data.zig");
const Reader = @import("reader.zig");

const print = std.debug.print;

pub fn main() !void {
    var timer = Timer.start();
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const alloc = gpa.allocator();
    var data = Data.init(alloc);
    defer data.deinit();
    try Reader.readData(alloc, "data.txt", &data, Data.processInputLine);

    const p1 = try data.getPart1Value();
    std.debug.print("p1: {d}", .{p1});
    timer.printStats(print);

    const p2 = try data.getPart2Value();
    std.debug.print("p2: {d}", .{p2});
    timer.end();
    timer.printStats(print);
}

test "example 1" {
    var data = Data.init(std.testing.allocator);
    defer data.deinit();
    try Reader.readData(std.testing.allocator, "example.txt", &data, Data.processInputLine);
    const v = try data.getPart1Value();
    try std.testing.expectEqual(60, v);
}

test "example 1.5" {
    var data = Data.init(std.testing.allocator);
    defer data.deinit();

    try data.processInputLine("2333133121414131402");
    const v = try data.getPart1Value();
    try std.testing.expectEqual(1928, v);
}

test "example 1.5 - part 2" {
    var data = Data.init(std.testing.allocator);
    defer data.deinit();

    try data.processInputLine("2333133121414131402");
    const v = try data.getPart2Value();
    try std.testing.expectEqual(2858, v);
}
