const std = @import("std");
const Data = @import("data.zig");
const Timer = @import("timer.zig");

const print = std.debug.print;

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const alloc = gpa.allocator();
    var timer = Timer.start();

    const data = try readData(alloc);
    defer data.deinit();

    const p1 = data.calcPart1Value();
    print("p1: {d}\n", .{p1});

    const p2 = try data.calcPart2Value();
    print("p2: {d}\n", .{p2});

    timer.end();
    timer.printStats();
}

fn readData(alloc: std.mem.Allocator) !Data {
    var file = try std.fs.cwd().openFile("data.txt", .{});
    defer file.close();

    var buf_read = std.io.bufferedReader(file.reader());
    var in_stream = buf_read.reader();
    var buf: [4096]u8 = undefined;

    var data = try Data.init(alloc);
    errdefer data.deinit();

    var is_rules = true;
    while (try in_stream.readUntilDelimiterOrEof(&buf, '\n')) |line| {
        const trimmed = if (@import("builtin").os.tag == .windows)
            std.mem.trimRight(u8, line, "\r")
        else
            line;
        if (trimmed.len == 0) {
            is_rules = false;
            continue;
        }

        if (is_rules) {
            try data.addRule(trimmed);
        } else {
            try data.addPrintJob(trimmed);
        }
    }

    return data;
}

fn getExampleOneData(alloc: std.mem.Allocator) !Data {
    var data = try Data.init(alloc);
    try data.addRule("47|53");
    try data.addRule("97|13");
    try data.addRule("97|61");
    try data.addRule("97|47");
    try data.addRule("75|29");
    try data.addRule("61|13");
    try data.addRule("75|53");
    try data.addRule("29|13");
    try data.addRule("97|29");
    try data.addRule("53|29");
    try data.addRule("61|53");
    try data.addRule("97|53");
    try data.addRule("61|29");
    try data.addRule("47|13");
    try data.addRule("75|47");
    try data.addRule("97|75");
    try data.addRule("47|61");
    try data.addRule("75|61");
    try data.addRule("47|29");
    try data.addRule("75|13");
    try data.addRule("53|13");

    try data.addPrintJob("75,47,61,53,29");
    try data.addPrintJob("97,61,53,29,13");
    try data.addPrintJob("75,29,13");
    try data.addPrintJob("75,97,47,61,53");
    try data.addPrintJob("61,13,29");
    try data.addPrintJob("97,13,75,29,47");
    return data;
}

test "part 1 example" {
    const data = try getExampleOneData(std.testing.allocator);
    defer data.deinit();

    const p1 = data.calcPart1Value();
    try std.testing.expectEqual(143, p1);
}

test "part 2 example" {
    const data = try getExampleOneData(std.testing.allocator);
    defer data.deinit();

    const p2 = try data.calcPart2Value();
    try std.testing.expectEqual(123, p2);
}
