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
    try Reader.readData("data.txt", &data, Data.processInputLine);

    const p1 = try data.getPart1Value();
    print("p1: {d}\n", .{p1});
    timer.printStats(print);
    
    const p2 = try data.getPart2Value();
    print("p2: {d}\n", .{p2});
    
    timer.end();
    timer.printStats(print);
}

test "example 1" {
    var data = Data.init(std.testing.allocator);
    defer data.deinit();
    try Reader.readData("example.txt", &data, Data.processInputLine);

    const v = try data.getPart1Value();
    try std.testing.expectEqual(3749, v);
}
test "example 2" {
    var data = Data.init(std.testing.allocator);
    defer data.deinit();
    try Reader.readData("example.txt", &data, Data.processInputLine);

    const v = try data.getPart2Value();
    try std.testing.expectEqual(11387, v);
}
