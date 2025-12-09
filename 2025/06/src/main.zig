const std = @import("std");
const r = @import("./root.zig");

const State = r.State;
const Part = r.Part;

pub fn main() !void {
    var mode: Part = .one;
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const alloc = gpa.allocator();

    var argIt = try std.process.argsWithAllocator(alloc);
    defer argIt.deinit();

    while (argIt.next()) |arg| {
        if (arg[0] != '-') continue;

        if (std.mem.eql(u8, arg, "-2")) {
            mode = .two;
        } else if (std.mem.eql(u8, arg, "-1")) {
            mode = .one;
        }
    }
    try processDataStream(alloc, mode);
}

const isWindows = @import("builtin").os.tag == .windows;
const newlineSize = if (isWindows) 2 else 1;

fn processDataStream(alloc: std.mem.Allocator, part: Part) !void {
    var file = try std.fs.cwd().openFile("src/data.txt", .{ .mode = .read_write });
    defer file.close();

    var buf: [4096]u8 = undefined;
    var file_reader = file.reader(&buf);
    var reader = &file_reader.interface;

    var state = State.init(alloc, part);

    while (true) {
        const line = reader.takeDelimiterExclusive('\n') catch |e| switch (e) {
            error.EndOfStream => break,
            else => return e,
        };

        const new_len = if (isWindows and line.len > 0 and line[line.len - 1] == '\r') line.len - 1 else line.len;
        try state.processLine(line[0..new_len]);

        // peek after processing in case of EOS
        const next_c = reader.peek(1) catch |e| switch (e) {
            error.EndOfStream => break,
            else => return e,
        };
        if (next_c[0] == '\n') {
            reader.toss(1);
        }
    }

    state.computeResult();

    state.printResult();
    state.deinit();
}
