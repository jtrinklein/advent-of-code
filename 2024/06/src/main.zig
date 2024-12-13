const std = @import("std");
const Data = @import("data.zig");
const Timer = @import("timer.zig");
const Reader = @import("reader.zig");
const print = std.debug.print;

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();

    const alloc = gpa.allocator();
    var timer = Timer.start();
    var data = Data.init(alloc);
    defer data.deinit();
    try Reader.readData("data.txt", &data, Data.processInputLine);

    const p1 = try data.getPart1Value();
    print("part 1: {d}\n", .{p1});
    const p2 = data.getPart2Value();
    print("part 2: {d}\n", .{p2});
    timer.end();
    timer.printStats(print);
}

test "example part 1" {
    var data = Data.init(std.testing.allocator);
    defer data.deinit();
    try Reader.readData("example.txt", &data, Data.processInputLine);

    const v = try data.getPart1Value();
    try std.testing.expectEqual(41, v);
}

test "example part 2" {
    var data = Data.init(std.testing.allocator);
    defer data.deinit();
    try Reader.readData("example.txt", &data, Data.processInputLine);

    const v = try data.getPart1Value();
    try std.testing.expectEqual(41, v);

    const v2 = data.getPart2Value();
    try std.testing.expectEqual(6, v2);
}
