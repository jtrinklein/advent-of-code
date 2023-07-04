const std = @import("std");
const assert = std.debug.assert;

fn nextButtonMethod2(start: u8, path: []const u8) u8 {
    var n = start;

    for (path) |ch| {
        n = switch (ch) {
            'U' => switch (n) {
                5, 2, 1, 4, 9 => n,
                6...8, 10...12 => n - 4,
                else => n - 2,
            },
            'D' => switch (n) {
                5, 10, 13, 12, 9 => n,
                6...8, 2...4 => n + 4,
                else => n + 2,
            },
            'L' => switch (n) {
                1, 2, 5, 10, 13 => n,
                else => n - 1,
            },
            'R' => switch (n) {
                1, 4, 9, 12, 13 => n,
                else => n + 1,
            },
            else => n,
        };
    }

    return n;
}

fn nextButtonMethod1(start: u8, path: []const u8) u8 {
    var n = start;

    for (path) |ch| {
        n = switch (ch) {
            'U' => switch (n) {
                1...3 => n,
                else => n - 3,
            },
            'D' => switch (n) {
                7...9 => n,
                else => n + 3,
            },
            'L' => switch (n) {
                1, 4, 7 => n,
                else => n - 1,
            },
            'R' => switch (n) {
                3, 6, 9 => n,
                else => n + 1,
            },
            else => n,
        };
    }

    return n;
}

fn nextButton(start: u8, path: []const u8, method: u8) u8 {
    if (method == 1) {
        return nextButtonMethod1(start, path);
    }
    return nextButtonMethod2(start, path);
}

fn getButtons(alloc: std.mem.Allocator, method: u8) ![]const u8 {
    const file = try std.fs.cwd().openFile("data.txt", .{});
    defer file.close();

    var list = std.ArrayList(u8).init(alloc);
    defer list.deinit();

    var bufReader = std.io.bufferedReader(file.reader());
    var stream = bufReader.reader();

    var buf: [4096]u8 = undefined;
    var btn: u8 = 5;
    while (try stream.readUntilDelimiterOrEof(&buf, '\n')) |data_line| {
        btn = nextButton(btn, data_line, method);
        try list.append(btn);
    }
    return list.toOwnedSlice();
}

pub fn main() !void {
    const allocator = std.heap.page_allocator;

    var start = std.time.milliTimestamp();
    const buttons1 = try getButtons(allocator, 1);
    defer allocator.free(buttons1);
    var end = std.time.milliTimestamp();
    std.debug.print("part 1\n>", .{});
    for (buttons1) |button| {
        std.debug.print("{d}", .{button});
    }
    std.debug.print("<\n in {d} ms", .{end - start});

    start = std.time.milliTimestamp();
    const buttons2 = try getButtons(allocator, 2);
    defer allocator.free(buttons2);
    end = std.time.milliTimestamp();

    const alpha = [14]u8{ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D' };
    std.debug.print("part 2\n>", .{});
    for (buttons2) |button| {
        std.debug.print("{c}", .{alpha[button]});
    }
    std.debug.print("<\n in {d} ms", .{end - start});
}

test "gets correct button" {
    var b = nextButton(5, "URDD");
    assert(b == 9);

    b = nextButton(1, "LLLL");
    assert(b == 1);

    b = nextButton(1, "RRRR");
    assert(b == 3);

    b = nextButton(1, "DDDDD");
    assert(b == 7);

    b = nextButton(1, "RRDDDLLLLLUUUUUUUUDDUUDDU");
    assert(b == 4);
}
