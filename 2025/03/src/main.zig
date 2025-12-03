const std = @import("std");
const State = @import("_03").State;

const Part = enum {
    one,
    two,
    test_one,
    test_two,
};

pub fn main() !void {
    var mode: Part = .one;
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const alloc = gpa.allocator();

    var argIt = try std.process.argsWithAllocator(alloc);
    defer argIt.deinit();

    while (argIt.next()) |arg| {
        if (arg[0] != '-') continue;

        if (std.mem.eql(u8, arg, "-t1")) {
            mode = .test_one;
        } else if (std.mem.eql(u8, arg, "-t2")) {
            mode = .test_two;
        } else if (std.mem.eql(u8, arg, "-2")) {
            mode = .two;
        } else if (std.mem.eql(u8, arg, "-1")) {
            mode = .one;
        }
    }
    try processDataStream(mode);
}

fn getFile(part: Part) [:0]const u8 {
    return switch (part) {
        .test_one => "src/test.txt",
        .test_two => "src/test.txt",
        .one => "src/data.txt",
        .two => "src/data.txt",
    };
}

const isWindows = @import("builtin").os.tag == .windows;
const newlineSize = if (isWindows) 2 else 1;
const newlineChar = if (isWindows) '\r' else '\n';

fn processDataStream(part: Part) !void {
    const filename = getFile(part);
    var file = try std.fs.cwd().openFile(filename, .{ .mode = .read_write });
    defer file.close();

    var buf: [4096]u8 = undefined;
    var file_reader = file.reader(&buf);
    if (file_reader.err) |e| {
        return e;
    }
    var reader = &file_reader.interface;

    var state = State.init();

    while (true) {
        const line = reader.takeDelimiterExclusive('\r') catch |e| {
            if (e == error.EndOfStream) break;
            return e;
        };
        // skip \n too because windows fun
        if (reader.seek != reader.end) {
            reader.toss(2);
        }
        if (part == .one or part == .test_one) {
            try state.part1(line);
        } else {
            try state.part2(line);
        }

        if (reader.seek == reader.end) {
            break;
        }
    }

    state.printResult();
}
